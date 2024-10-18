"""
This module defines the Pytorch extension for OpenML-python.
"""
from collections import OrderedDict  # noqa: F401
import copy
from distutils.version import LooseVersion
import importlib
import inspect
import json
import logging
import re
import sys
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import warnings

import numpy as np
import pandas as pd

import scipy.sparse
import scipy.special
from . import config
from openml_pytorch.trainer import OpenMLTrainerModule

import torch
import torch.nn
import torch.optim
import torch.utils.data
import torch.autograd
import torch.cuda

import openml
from openml.exceptions import PyOpenMLError
from openml.extensions import Extension, register_extension
from openml.flows import OpenMLFlow
from openml.runs.trace import OpenMLRunTrace, OpenMLTraceIteration
from openml.tasks import (
    OpenMLTask,
    OpenMLSupervisedTask,
    OpenMLClassificationTask,
    OpenMLRegressionTask,
)
from types import SimpleNamespace
import os 


from sklearn import preprocessing

import io
import onnx

if sys.version_info >= (3, 5):
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError


DEPENDENCIES_PATTERN = re.compile(
    r'^(?P<name>[\w\-]+)((?P<operation>==|>=|>)'
    r'(?P<version>(\d+\.)?(\d+\.)?(\d+)?(dev)?[0-9]*))?$'
)


SIMPLE_NUMPY_TYPES = [nptype for type_cat, nptypes in np.sctypes.items()
                      for nptype in nptypes if type_cat != 'others']
SIMPLE_TYPES = tuple([bool, int, float, str] + SIMPLE_NUMPY_TYPES)

## Variable to support a hack to add ONNX to runs without modifying openml-python
last_models = None
sample_input = None




class PytorchExtension(Extension):
    """Connect Pytorch to OpenML-Python."""

    ################################################################################################
    # General setup

    @classmethod
    def can_handle_flow(cls, flow: 'OpenMLFlow') -> bool:
        """Check whether a given describes a Pytorch estimator.

        This is done by parsing the ``external_version`` field.

        Parameters
        ----------
        flow : OpenMLFlow

        Returns
        -------
        bool
        """
        return cls._is_pytorch_flow(flow)

    @classmethod
    def can_handle_model(cls, model: Any) -> bool:
        """Check whether a model is an instance of ``torch.nn.Module``.

        Parameters
        ----------
        model : Any

        Returns
        -------
        bool
        """
        from torch.nn import Module
        return isinstance(model, Module)
    
    ################################################################################################
    # Method for dataloader 
    
    
 
    ################################################################################################
    # Methods for flow serialization and de-serialization

    def flow_to_model(self, flow: 'OpenMLFlow', initialize_with_defaults: bool = False) -> Any:
        """Initializes a Pytorch model based on a flow.

        Parameters
        ----------
        flow : mixed
            the object to deserialize (can be flow object, or any serialized
            parameter value that is accepted by)

        initialize_with_defaults : bool, optional (default=False)
            If this flag is set, the hyperparameter values of flows will be
            ignored and a flow with its defaults is returned.

        Returns
        -------
        mixed
        """
        return self._deserialize_pytorch(flow, initialize_with_defaults=initialize_with_defaults)

    def _deserialize_pytorch(
        self,
        o: Any,
        components: Optional[Dict] = None,
        initialize_with_defaults: bool = False,
        recursion_depth: int = 0,
    ) -> Any:
        """Recursive function to deserialize a Pytorch flow.

        This function delegates all work to the respective functions to deserialize special data
        structures etc.

        Parameters
        ----------
        o : mixed
            the object to deserialize (can be flow object, or any serialized
            parameter value that is accepted by)

        components : dict


        initialize_with_defaults : bool, optional (default=False)
            If this flag is set, the hyperparameter values of flows will be
            ignored and a flow with its defaults is returned.

        recursion_depth : int
            The depth at which this flow is called, mostly for debugging
            purposes

        Returns
        -------
        mixed
        """

        logging.info('-%s flow_to_pytorch START o=%s, components=%s, '
                     'init_defaults=%s' % ('-' * recursion_depth, o, components,
                                           initialize_with_defaults))
        depth_pp = recursion_depth + 1  # shortcut var, depth plus plus

        # First, we need to check whether the presented object is a json string.
        # JSON strings are used to encoder parameter values. By passing around
        # json strings for parameters, we make sure that we can flow_to_pytorch
        # the parameter values to the correct type.

        if isinstance(o, str):
            try:
                o = json.loads(o)
            except JSONDecodeError:
                pass

        if isinstance(o, dict):
            # Check if the dict encodes a 'special' object, which could not
            # easily converted into a string, but rather the information to
            # re-create the object were stored in a dictionary.
            if 'oml-python:serialized_object' in o:
                serialized_type = o['oml-python:serialized_object']
                value = o['value']
                if serialized_type == 'type':
                    rval = self._deserialize_type(value)
                elif serialized_type == 'function':
                    rval = self._deserialize_function(value)
                elif serialized_type == 'methoddescriptor':
                    rval = self._deserialize_methoddescriptor(value)
                elif serialized_type == 'component_reference':
                    assert components is not None  # Necessary for mypy
                    value = self._deserialize_pytorch(value, recursion_depth=depth_pp)
                    step_name = value['step_name']
                    key = value['key']
                    if key not in components:
                        key = str(key)
                    component = self._deserialize_pytorch(
                        components[key],
                        initialize_with_defaults=initialize_with_defaults,
                        recursion_depth=depth_pp
                    )
                    # The component is now added to where it should be used
                    # later. It should not be passed to the constructor of the
                    # main flow object.
                    del components[key]
                    if step_name is None:
                        rval = component
                    elif 'argument_1' not in value:
                        rval = (step_name, component)
                    else:
                        rval = (step_name, component, value['argument_1'])
                else:
                    raise ValueError('Cannot flow_to_pytorch %s' % serialized_type)

            else:
                rval = OrderedDict(
                    (
                        self._deserialize_pytorch(
                            o=key,
                            components=components,
                            initialize_with_defaults=initialize_with_defaults,
                            recursion_depth=depth_pp,
                        ),
                        self._deserialize_pytorch(
                            o=value,
                            components=components,
                            initialize_with_defaults=initialize_with_defaults,
                            recursion_depth=depth_pp,
                        )
                    )
                    for key, value in sorted(o.items())
                )
        elif isinstance(o, (list, tuple)):
            rval = [
                self._deserialize_pytorch(
                    o=element,
                    components=components,
                    initialize_with_defaults=initialize_with_defaults,
                    recursion_depth=depth_pp,
                )
                for element in o
            ]
            if isinstance(o, tuple):
                rval = tuple(rval)
        elif isinstance(o, (bool, int, float, str)) or o is None:
            rval = o
        elif isinstance(o, OpenMLFlow):
            if not self._is_pytorch_flow(o):
                raise ValueError('Only pytorch flows can be reinstantiated')
            rval = self._deserialize_model(
                flow=o,
                keep_defaults=initialize_with_defaults,
                recursion_depth=recursion_depth,
            )
        else:
            raise TypeError(o)
        logging.info('-%s flow_to_pytorch END   o=%s, rval=%s'
                     % ('-' * recursion_depth, o, rval))
        return rval

    def model_to_flow(self, model: Any, custom_name: Optional[str] = None) -> 'OpenMLFlow':
        """Transform a Pytorch model to a flow for uploading it to OpenML.

        Parameters
        ----------
        model : Any

        Returns
        -------
        OpenMLFlow
        """
        # Necessary to make pypy not complain about all the different possible return types
        return self._serialize_pytorch(model, custom_name)

    def _serialize_pytorch(self, o: Any, parent_model: Optional[Any] = None, custom_name: Optional[str] = None) -> Any:
        rval = None  # type: Any
        if self.is_estimator(o):
            # is the main model or a submodel
            rval = self._serialize_model(o, custom_name)
        elif isinstance(o, (list, tuple)):
            rval = [self._serialize_pytorch(element, parent_model) for element in o]
            if isinstance(o, tuple):
                rval = tuple(rval)
        elif isinstance(o, SIMPLE_TYPES) or o is None:
            if isinstance(o, tuple(SIMPLE_NUMPY_TYPES)):
                o = o.item()
            # base parameter values
            rval = o
        elif isinstance(o, dict):
            if not isinstance(o, OrderedDict):
                o = OrderedDict([(key, value) for key, value in sorted(o.items())])

            rval = OrderedDict()
            for key, value in o.items():
                if not isinstance(key, str):
                    raise TypeError('Can only use string as keys, you passed '
                                    'type %s for value %s.' %
                                    (type(key), str(key)))
                key = self._serialize_pytorch(key, parent_model)
                value = self._serialize_pytorch(value, parent_model)
                rval[key] = value
            rval = rval
        elif isinstance(o, type):
            rval = self._serialize_type(o)
        # This only works for user-defined functions (and not even partial).
        # I think this is exactly what we want here as there shouldn't be any
        # built-in or functool.partials in a pipeline
        elif inspect.isfunction(o):
            rval = self._serialize_function(o)
        elif inspect.ismethoddescriptor(o):
            rval = self._serialize_methoddescriptor(o)
        else:
            raise TypeError(o, type(o))
        return rval

    def get_version_information(self) -> List[str]:
        """List versions of libraries required by the flow.

        Libraries listed are ``Python``, ``pytorch``, ``numpy`` and ``scipy``.

        Returns
        -------
        List
        """

        # This can possibly be done by a package such as pyxb, but I could not get
        # it to work properly.
        import scipy
        import numpy

        major, minor, micro, _, _ = sys.version_info
        python_version = 'Python_{}.'.format(
            ".".join([str(major), str(minor), str(micro)]))
        pytorch_version = 'Torch_{}.'.format(torch.__version__)
        numpy_version = 'NumPy_{}.'.format(numpy.__version__)
        scipy_version = 'SciPy_{}.'.format(scipy.__version__)
        pytorch_version_formatted = pytorch_version.replace('+','_')
        return [python_version, pytorch_version_formatted, numpy_version, scipy_version]

    def create_setup_string(self, model: Any) -> str:
        """Create a string which can be used to reinstantiate the given model.

        Parameters
        ----------
        model : Any

        Returns
        -------
        str
        """
        run_environment = " ".join(self.get_version_information())
        return run_environment + " " + str(model)

    @classmethod
    def _is_pytorch_flow(cls, flow: OpenMLFlow) -> bool:
        return (
            flow.external_version.startswith('torch==')
            or ',torch==' in flow.external_version
        )

    def _serialize_model(self, model: Any, custom_name: Optional[str] = None) -> OpenMLFlow:
        """Create an OpenMLFlow.

        Calls `pytorch_to_flow` recursively to properly serialize the
        parameters to strings and the components (other models) to OpenMLFlows.

        Parameters
        ----------
        model : pytorch estimator

        Returns
        -------
        OpenMLFlow

        """
        
        # Get all necessary information about the model objects itself
        parameters, parameters_meta_info, subcomponents, subcomponents_explicit = \
            self._extract_information_from_model(model)

        # Check that a component does not occur multiple times in a flow as this
        # is not supported by OpenML
        self._check_multiple_occurence_of_component_in_flow(model, subcomponents)

        import zlib
        import os

        # class_name = model.__module__ + "." + model.__class__.__name__
        class_name = 'torch.nn' + "." + model.__class__.__name__
        class_name += '.'
        class_name += format(zlib.crc32(bytearray(os.urandom(32))), 'x')
        class_name += format(zlib.crc32(bytearray(os.urandom(32))), 'x')

        name = class_name

        # Get the external versions of all sub-components
        external_version = self._get_external_version_string(model, subcomponents)

        dependencies = '\n'.join([
            self._format_external_version(
                'torch',
                torch.__version__,
            ),
            'numpy>=1.6.1',
            'scipy>=0.9',
        ])

        torch_version = self._format_external_version('torch', torch.__version__)
        torch_version_formatted = torch_version.replace('==', '_')
        torch_version_formatted = torch_version_formatted.replace('+', '_')

        flow = OpenMLFlow(name=name,
                          class_name=class_name,
                          description='Automatically created pytorch flow.',
                          model=model,
                          components=subcomponents,
                          parameters=parameters,
                          parameters_meta_info=parameters_meta_info,
                          external_version=external_version,
                          tags=['openml-python', 'pytorch',
                                'python', torch_version_formatted],
                          language='English',
                          dependencies=dependencies, 
                          custom_name=custom_name)

        return flow

    def _get_external_version_string(
        self,
        model: Any,
        sub_components: Dict[str, OpenMLFlow],
    ) -> str:
        # Create external version string for a flow, given the model and the
        # already parsed dictionary of sub_components. Retrieves the external
        # version of all subcomponents, which themselves already contain all
        # requirements for their subcomponents. The external version string is a
        # sorted concatenation of all modules which are present in this run.
        model_package_name = model.__module__.split('.')[0]
        module = importlib.import_module(model_package_name)
        model_package_version_number = 'module.__version__'  # type: ignore
        external_version = self._format_external_version(
            model_package_name, model_package_version_number,
        )
        openml_version = self._format_external_version('openml', openml.__version__)
        torch_version = self._format_external_version('torch', torch.__version__)
        external_versions = set()
        external_versions.add(external_version)
        external_versions.add(openml_version)
        external_versions.add(torch_version)
        for visitee in sub_components.values():
            for external_version in visitee.external_version.split(','):
                external_versions.add(external_version)
        return ','.join(list(sorted(external_versions)))

    def _check_multiple_occurence_of_component_in_flow(
        self,
        model: Any,
        sub_components: Dict[str, OpenMLFlow],
    ) -> None:
        to_visit_stack = []  # type: List[OpenMLFlow]
        to_visit_stack.extend(sub_components.values())
        known_sub_components = set()  # type: Set[str]
        while len(to_visit_stack) > 0:
            visitee = to_visit_stack.pop()
            if visitee.name in known_sub_components:
                raise ValueError('Found a second occurence of component %s when '
                                 'trying to serialize %s.' % (visitee.name, model))
            else:
                known_sub_components.add(visitee.name)
                to_visit_stack.extend(visitee.components.values())

    def _is_container_module(self, module: torch.nn.Module) -> bool:
        if isinstance(module,
                      (torch.nn.Sequential,
                       torch.nn.ModuleDict,
                       torch.nn.ModuleList)):
            return True
        if module in (torch.nn.modules.container.Sequential,
                      torch.nn.modules.container.ModuleDict,
                      torch.nn.modules.container.ModuleList):
            return True
        return False

    def _get_module_hyperparameters(self, module: torch.nn.Module,
                                    parameters: Dict[str, torch.nn.Parameter]) -> Dict[str, Any]:
        # Extract the signature of the module constructor
        main_signature = inspect.signature(module.__init__)
        params = dict()  # type: Dict[str, Any]

        check_bases = False  # type: bool
        for param_name, param in main_signature.parameters.items():
            # Skip hyper-parameters which are actually parameters.
            if param_name in parameters.keys():
                continue

            # Skip *args and **kwargs, and check the base classes instead.
            if param.kind in (inspect.Parameter.VAR_POSITIONAL,
                              inspect.Parameter.VAR_KEYWORD):
                check_bases = True
                continue

            # Extract the hyperparameter from the module.
            if hasattr(module, param_name):
                params[param_name] = getattr(module, param_name)

        if check_bases:
            for base in module.__class__.__bases__:
                # Extract the signature  of the base constructor
                base_signature = inspect.signature(base.__init__)

                for param_name, param in base_signature.parameters.items():
                    # Skip hyper-parameters which are actually parameters.
                    if param_name in parameters.keys():
                        continue

                    # Skip *args and **kwargs since they are not relevant.
                    if param.kind in (inspect.Parameter.VAR_POSITIONAL,
                                      inspect.Parameter.VAR_KEYWORD):
                        continue

                    # Extract the hyperparameter from the module.
                    if hasattr(module, param_name):
                        params[param_name] = getattr(module, param_name)

        from .layers import Functional
        if isinstance(module, Functional):
            params['args'] = getattr(module, 'args')
            params['kwargs'] = getattr(module, 'kwargs')
        
        return params

    def _get_module_descriptors(self, model: torch.nn.Module, deep=True) -> Dict[str, Any]:
        # The named children (modules) of the given module.
        named_children = list((k, v) for (k, v) in model.named_children())
        # The parameters of the given module and its submodules.
        model_parameters = dict((k, v) for (k, v) in model.named_parameters())

        parameters = dict()  # type: Dict[str, Any]
        
        if not self._is_container_module(model):
            # For non-containers, we simply extract the hyperparameters.
            parameters = self._get_module_hyperparameters(model, model_parameters)
        else:
            # Otherwise we serialize their children as lists of pairs in order
            # to maintain the order of the sub modules.
            parameters['children'] = named_children

        # If a deep description is required, append the children to the dictionary of
        # returned parameters.
        if deep:
            named_children_dict = dict(named_children)
            parameters = {**parameters, **named_children_dict}

        return parameters

    def _extract_information_from_model(
        self,
        model: Any,
    ) -> Tuple[
        'OrderedDict[str, Optional[str]]',
        'OrderedDict[str, Optional[Dict]]',
        'OrderedDict[str, OpenMLFlow]',
        Set,
    ]:
        # This function contains four "global" states and is quite long and
        # complicated. If it gets to complicated to ensure it's correctness,
        # it would be best to make it a class with the four "global" states being
        # the class attributes and the if/elif/else in the for-loop calls to
        # separate class methods

        # stores all entities that should become subcomponents
        sub_components = OrderedDict()  # type: OrderedDict[str, OpenMLFlow]
        # stores the keys of all subcomponents that should become
        sub_components_explicit = set()
        parameters = OrderedDict()  # type: OrderedDict[str, Optional[str]]
        parameters_meta_info = OrderedDict()  # type: OrderedDict[str, Optional[Dict]]
        
        model_parameters = self._get_module_descriptors(model, deep=True)
        for k, v in sorted(model_parameters.items(), key=lambda t: t[0]):
            rval = self._serialize_pytorch(v, model)

            def flatten_all(list_):
                """ Flattens arbitrary depth lists of lists (e.g. [[1,2],[3,[1]]] -> [1,2,3,1]). """
                for el in list_:
                    if isinstance(el, (list, tuple)):
                        yield from flatten_all(el)
                    else:
                        yield el

            is_non_empty_list_of_lists_with_same_type = (
                isinstance(rval, (list, tuple))
                and len(rval) > 0
                and isinstance(rval[0], (list, tuple))
                and all([isinstance(rval_i, type(rval[0])) for rval_i in rval])
            )

            # Check that all list elements are of simple types.
            nested_list_of_simple_types = (
                is_non_empty_list_of_lists_with_same_type
                and all([isinstance(el, SIMPLE_TYPES) for el in flatten_all(rval)])
            )

            if is_non_empty_list_of_lists_with_same_type and not nested_list_of_simple_types:
                # If a list of lists is identified that include 'non-simple' types (e.g. objects),
                # we assume they are steps in a pipeline, feature union, or base classifiers in
                # a voting classifier.
                parameter_value = list()  # type: List
                reserved_keywords = set(self._get_module_descriptors(model, deep=False).keys())

                for sub_component_tuple in rval:
                    identifier = sub_component_tuple[0]
                    sub_component = sub_component_tuple[1]
                    sub_component_type = type(sub_component_tuple)
                    if not 2 <= len(sub_component_tuple) <= 3:
                        msg = 'Length of tuple does not match assumptions'
                        raise ValueError(msg)
                    if not isinstance(sub_component, (OpenMLFlow, type(None))):
                        msg = 'Second item of tuple does not match assumptions. ' \
                              'Expected OpenMLFlow, got %s' % type(sub_component)
                        raise TypeError(msg)

                    if identifier in reserved_keywords:
                        parent_model = "{}.{}".format(model.__module__,
                                                      model.__class__.__name__)
                        msg = 'Found element shadowing official ' \
                              'parameter for %s: %s' % (parent_model,
                                                        identifier)
                        raise PyOpenMLError(msg)

                    if sub_component is None:
                        # In a FeatureUnion it is legal to have a None step

                        pv = [identifier, None]
                        if sub_component_type is tuple:
                            parameter_value.append(tuple(pv))
                        else:
                            parameter_value.append(pv)

                    else:
                        # Add the component to the list of components, add a
                        # component reference as a placeholder to the list of
                        # parameters, which will be replaced by the real component
                        # when deserializing the parameter
                        sub_components_explicit.add(identifier)
                        sub_components[identifier] = sub_component
                        component_reference = OrderedDict()  # type: Dict[str, Union[str, Dict]]
                        component_reference['oml-python:serialized_object'] = 'component_reference'
                        cr_value = OrderedDict()  # type: Dict[str, Any]
                        cr_value['key'] = identifier
                        cr_value['step_name'] = identifier
                        if len(sub_component_tuple) == 3:
                            cr_value['argument_1'] = sub_component_tuple[2]
                        component_reference['value'] = cr_value
                        parameter_value.append(component_reference)

                # Here (and in the elif and else branch below) are the only
                # places where we encode a value as json to make sure that all
                # parameter values still have the same type after
                # deserialization
                
                if isinstance(rval, tuple):
                    parameter_json = json.dumps(tuple(parameter_value))
                else:
                    parameter_json = json.dumps(parameter_value)
                parameters[k] = parameter_json

            elif isinstance(rval, OpenMLFlow):

                # A subcomponent, for example the layers in a sequential model
                sub_components[k] = rval
                sub_components_explicit.add(k)
                component_reference = OrderedDict()
                component_reference['oml-python:serialized_object'] = 'component_reference'
                cr_value = OrderedDict()
                cr_value['key'] = k
                cr_value['step_name'] = None
                component_reference['value'] = cr_value
                cr = self._serialize_pytorch(component_reference, model)
                parameters[k] = json.dumps(cr)

            else:
                # a regular hyperparameter
                rval = json.dumps(rval)
                parameters[k] = rval

            parameters_meta_info[k] = OrderedDict((('description', None), ('data_type', None)))

        return parameters, parameters_meta_info, sub_components, sub_components_explicit

    def _get_fn_arguments_with_defaults(self, fn_name: Callable) -> Tuple[Dict, Set]:
        """
        Returns:
            i) a dict with all parameter names that have a default value, and
            ii) a set with all parameter names that do not have a default

        Parameters
        ----------
        fn_name : callable
            The function of which we want to obtain the defaults

        Returns
        -------
        params_with_defaults: dict
            a dict mapping parameter name to the default value
        params_without_defaults: set
            a set with all parameters that do not have a default value
        """
        # parameters with defaults are optional, all others are required.
        signature = inspect.getfullargspec(fn_name)
        if signature.defaults:
            optional_params = dict(zip(reversed(signature.args), reversed(signature.defaults)))
        else:
            optional_params = dict()
        required_params = {arg for arg in signature.args if arg not in optional_params}
        return optional_params, required_params

    def _deserialize_model(
        self,
        flow: OpenMLFlow,
        keep_defaults: bool,
        recursion_depth: int,
    ) -> Any:
        logging.info('-%s deserialize %s' % ('-' * recursion_depth, flow.name))
        model_name = flow.class_name
        self._check_dependencies(flow.dependencies)

        parameters = flow.parameters
        components = flow.components
        parameter_dict = OrderedDict()  # type: Dict[str, Any]

        # Do a shallow copy of the components dictionary so we can remove the
        # components from this copy once we added them into the pipeline. This
        # allows us to not consider them any more when looping over the
        # components, but keeping the dictionary of components untouched in the
        # original components dictionary.
        components_ = copy.copy(components)

        for name in parameters:
            value = parameters.get(name)
            logging.info('--%s flow_parameter=%s, value=%s' %
                         ('-' * recursion_depth, name, value))
            rval = self._deserialize_pytorch(
                value,
                components=components_,
                initialize_with_defaults=keep_defaults,
                recursion_depth=recursion_depth + 1,
            )
            parameter_dict[name] = rval

        for name in components:
            if name in parameter_dict:
                continue
            if name not in components_:
                continue
            value = components[name]
            logging.info('--%s flow_component=%s, value=%s'
                         % ('-' * recursion_depth, name, value))
            rval = self._deserialize_pytorch(
                value,
                recursion_depth=recursion_depth + 1,
            )
            parameter_dict[name] = rval

        # Remove the unique identifier
        model_name = model_name.rsplit('.', 1)[0]

        module_name = model_name.rsplit('.', 1)
        model_class = getattr(importlib.import_module(module_name[0]),
                              module_name[1])

        if keep_defaults:
            # obtain all params with a default
            param_defaults, _ = \
                self._get_fn_arguments_with_defaults(model_class.__init__)

            # delete the params that have a default from the dict,
            # so they get initialized with their default value
            # except [...]
            for param in param_defaults:
                # [...] the ones that also have a key in the components dict.
                # As OpenML stores different flows for ensembles with different
                # (base-)components, in OpenML terms, these are not considered
                # hyperparameters but rather constants (i.e., changing them would
                # result in a different flow)
                if param not in components.keys() and param in parameter_dict:
                    del parameter_dict[param]

        if self._is_container_module(model_class):
            children = parameter_dict['children']
            children = list((str(k), v) for (k, v) in children)
            children = OrderedDict(children)
            return model_class(children)

        from .layers import Functional
        if model_class is Functional:
            return model_class(function=parameter_dict['function'],
                               *parameter_dict['args'],
                               **parameter_dict['kwargs'])

        return model_class(**parameter_dict)

    def _check_dependencies(self, dependencies: str) -> None:
        if not dependencies:
            return

        dependencies_list = dependencies.split('\n')
        for dependency_string in dependencies_list:
            match = DEPENDENCIES_PATTERN.match(dependency_string)
            if not match:
                raise ValueError('Cannot parse dependency %s' % dependency_string)

            dependency_name = match.group('name')
            operation = match.group('operation')
            version = match.group('version')

            module = importlib.import_module(dependency_name)
            required_version = LooseVersion(version)
            installed_version = LooseVersion(module.__version__)  # type: ignore

            if operation == '==':
                check = required_version == installed_version
            elif operation == '>':
                check = installed_version > required_version
            elif operation == '>=':
                check = (installed_version > required_version
                         or installed_version == required_version)
            else:
                raise NotImplementedError(
                    'operation \'%s\' is not supported' % operation)
            if not check:
                raise ValueError('Trying to deserialize a model with dependency '
                                 '%s not satisfied.' % dependency_string)

    def _serialize_type(self, o: Any) -> 'OrderedDict[str, str]':
        mapping = {float: 'float',
                   np.float: 'np.float',
                   np.float32: 'np.float32',
                   np.float64: 'np.float64',
                   int: 'int',
                   np.int: 'np.int',
                   np.int32: 'np.int32',
                   np.int64: 'np.int64'}
        ret = OrderedDict()  # type: 'OrderedDict[str, str]'
        ret['oml-python:serialized_object'] = 'type'
        ret['value'] = mapping[o]
        return ret

    def _deserialize_type(self, o: str) -> Any:
        mapping = {'float': float,
                   'np.float': np.float,
                   'np.float32': np.float32,
                   'np.float64': np.float64,
                   'int': int,
                   'np.int': np.int,
                   'np.int32': np.int32,
                   'np.int64': np.int64}
        return mapping[o]

    def _serialize_function(self, o: Callable) -> 'OrderedDict[str, str]':
        name = o.__module__ + '.' + o.__name__
        ret = OrderedDict()  # type: 'OrderedDict[str, str]'
        ret['oml-python:serialized_object'] = 'function'
        ret['value'] = name
        return ret

    def _deserialize_function(self, name: str) -> Callable:
        module_name = name.rsplit('.', 1)
        function_handle = getattr(importlib.import_module(module_name[0]), module_name[1])
        return function_handle

    def _serialize_methoddescriptor(self, o: Any) -> 'OrderedDict[str, str]':
        name = o.__objclass__.__module__ \
            + '.' + o.__objclass__.__name__ \
            + '.' + o.__name__
        ret = OrderedDict()  # type: 'OrderedDict[str, str]'
        ret['oml-python:serialized_object'] = 'methoddescriptor'
        ret['value'] = name
        return ret

    def _deserialize_methoddescriptor(self, name: str) -> Any:
        module_name = name.rsplit('.', 2)
        object_handle = getattr(importlib.import_module(module_name[0]), module_name[1])
        function_handle = getattr(object_handle, module_name[2])
        return function_handle

    def _format_external_version(
        self,
        model_package_name: str,
        model_package_version_number: str,
    ) -> str:
        return '%s==%s' % (model_package_name, model_package_version_number)

    @staticmethod
    def _get_parameter_values_recursive(param_grid: Union[Dict, List[Dict]],
                                        parameter_name: str) -> List[Any]:
        """
        Returns a list of values for a given hyperparameter, encountered
        recursively throughout the flow. (e.g., n_jobs can be defined
        for various flows)

        Parameters
        ----------
        param_grid: Union[Dict, List[Dict]]
            Dict mapping from hyperparameter list to value, to a list of
            such dicts

        parameter_name: str
            The hyperparameter that needs to be inspected

        Returns
        -------
        List
            A list of all values of hyperparameters with this name
        """
        if isinstance(param_grid, dict):
            result = list()
            for param, value in param_grid.items():
                if param.split('__')[-1] == parameter_name:
                    result.append(value)
            return result
        elif isinstance(param_grid, list):
            result = list()
            for sub_grid in param_grid:
                result.extend(PytorchExtension._get_parameter_values_recursive(sub_grid,
                                                                               parameter_name))
            return result
        else:
            raise ValueError('Param_grid should either be a dict or list of dicts')

    ################################################################################################
    # Methods for performing runs with extension modules

    def is_estimator(self, model: Any) -> bool:
        """Check whether the given model is a pytorch estimator.

        This function is only required for backwards compatibility and will be removed in the
        near future.

        Parameters
        ----------
        model : Any

        Returns
        -------
        bool
        """
        return isinstance(model, torch.nn.Module)

    def seed_model(self, model: Any, seed: Optional[int] = None) -> Any:
        """Set the random state of all the unseeded components of a model and return the seeded
        model.

        Required so that all seed information can be uploaded to OpenML for reproducible results.

        Models that are already seeded will maintain the seed. In this case,
        only integer seeds are allowed (An exception is raised when a RandomState was used as
        seed).

        Parameters
        ----------
        model : pytorch model
            The model to be seeded
        seed : int
            The seed to initialize the RandomState with. Unseeded subcomponents
            will be seeded with a random number from the RandomState.

        Returns
        -------
        Any
        """

        return model
    
    def _run_model_on_fold(
        self,
        model: Any,
        task: 'OpenMLTask',
        X_train: Union[np.ndarray, scipy.sparse.spmatrix, pd.DataFrame],
        rep_no: int,
        fold_no: int,
        y_train: Optional[np.ndarray] = None,
        X_test: Optional[Union[np.ndarray, scipy.sparse.spmatrix, pd.DataFrame]] = None,
    ) -> Tuple[
        np.ndarray,
        np.ndarray,
        'OrderedDict[str, float]',
        Optional[OpenMLRunTrace],
        Optional[Any]
    ]:
        """Run a model on a repeat,fold,subsample triplet of the task and return prediction
        information.

        Furthermore, it will measure run time measures in case multi-core behaviour allows this.
        * exact user cpu time will be measured if the number of cores is set (recursive throughout
        the model) exactly to 1
        * wall clock time will be measured if the number of cores is set (recursive throughout the
        model) to any given number (but not when it is set to -1)

        Returns the data that is necessary to construct the OpenML Run object. Is used by
        run_task_get_arff_content. Do not use this function unless you know what you are doing.

        Parameters
        ----------
        model : Any
            The UNTRAINED model to run. The model instance will be copied and not altered.
        task : OpenMLTask
            The task to run the model on.
        X_train : array-like
            Training data for the given repetition and fold.
        rep_no : int
            The repeat of the experiment (0-based; in case of 1 time CV, always 0)
        fold_no : int
            The fold nr of the experiment (0-based; in case of holdout, always 0)
        y_train : Optional[np.ndarray] (default=None)
            Target attributes for supervised tasks. In case of classification, these are integer
            indices to the potential classes specified by dataset.
        X_test : Optional, array-like (default=None)
            Test attributes to test for generalization in supervised tasks.

        Returns
        -------
        predictions : np.ndarray
            Model predictions.
        probabilities :  Optional, np.ndarray
            Predicted probabilities (only applicable for supervised classification tasks).
        user_defined_measures : OrderedDict[str, float]
            User defined measures that were generated on this fold
        trace : Optional, OpenMLRunTrace
            Hyperparameter optimization trace (only applicable for supervised tasks with
            hyperparameter optimization).
        additional_information: Optional, Any
            Additional information provided by the extension to be converted into additional files.
        """

        try:
            trainer:OpenMLTrainerModule = config.trainer
            trainer.logger = config.logger
        except AttributeError:
            raise ValueError('Trainer not set to config. Please use openml_pytorch.config.trainer = trainer to set the trainer.')
        return trainer.run_model_on_fold(model, task, X_train, rep_no, fold_no, y_train, X_test)
    

    def compile_additional_information(
            self,
            task: 'OpenMLTask',
            additional_information: List[Tuple[int, int, Any]]
    ) -> Dict[str, Tuple[str, str]]:
        """Compiles additional information provided by the extension during the runs into a final
        set of files.

        Parameters
        ----------
        task : OpenMLTask
            The task the model was run on.
        additional_information: List[Tuple[int, int, Any]]
            A list of (fold, repetition, additional information) tuples obtained during training.

        Returns
        -------
        files : Dict[str, Tuple[str, str]]
            A dictionary of files with their file name and contents.
        """
        return dict()

    def obtain_parameter_values(
        self,
        flow: 'OpenMLFlow',
        model: Any = None,
    ) -> List[Dict[str, Any]]:
        """Extracts all parameter settings required for the flow from the model.

        If no explicit model is provided, the parameters will be extracted from `flow.model`
        instead.

        Parameters
        ----------
        flow : OpenMLFlow
            OpenMLFlow object (containing flow ids, i.e., it has to be downloaded from the server)

        model: Any, optional (default=None)
            The model from which to obtain the parameter values. Must match the flow signature.
            If None, use the model specified in ``OpenMLFlow.model``.

        Returns
        -------
        list
            A list of dicts, where each dict has the following entries:
            - ``oml:name`` : str: The OpenML parameter name
            - ``oml:value`` : mixed: A representation of the parameter value
            - ``oml:component`` : int: flow id to which the parameter belongs
        """
        openml.flows.functions._check_flow_for_server_id(flow)

        def get_flow_dict(_flow):
            flow_map = {_flow.name: _flow.flow_id}
            for subflow in _flow.components:
                flow_map.update(get_flow_dict(_flow.components[subflow]))
            return flow_map

        def extract_parameters(_flow, _flow_dict, component_model,
                               _main_call=False, main_id=None):
            def is_subcomponent_specification(values):
                # checks whether the current value can be a specification of
                # subcomponents, as for example the value for steps parameter
                # (in Pipeline) or transformers parameter (in
                # ColumnTransformer). These are always lists/tuples of lists/
                # tuples, size bigger than 2 and an OpenMLFlow item involved.
                if not isinstance(values, (tuple, list)):
                    return False
                for item in values:
                    if not isinstance(item, (tuple, list)):
                        return False
                    if len(item) < 2:
                        return False
                    if not isinstance(item[1], openml.flows.OpenMLFlow):
                        return False
                return True

            # _flow is openml flow object, _param dict maps from flow name to flow
            # id for the main call, the param dict can be overridden (useful for
            # unit tests / sentinels) this way, for flows without subflows we do
            # not have to rely on _flow_dict
            exp_parameters = set(_flow.parameters)
            exp_components = set(_flow.components)
            model_parameters = set([mp for mp in self._get_module_descriptors(component_model)
                                    if '__' not in mp])
            if len((exp_parameters | exp_components) ^ model_parameters) != 0:
                flow_params = sorted(exp_parameters | exp_components)
                model_params = sorted(model_parameters)
                raise ValueError('Parameters of the model do not match the '
                                 'parameters expected by the '
                                 'flow:\nexpected flow parameters: '
                                 '%s\nmodel parameters: %s' % (flow_params,
                                                               model_params))

            _params = []
            for _param_name in _flow.parameters:
                _current = OrderedDict()
                _current['oml:name'] = _param_name

                current_param_values = self.model_to_flow(
                    self._get_module_descriptors(component_model)[_param_name])

                # Try to filter out components (a.k.a. subflows) which are
                # handled further down in the code (by recursively calling
                # this function)!
                if isinstance(current_param_values, openml.flows.OpenMLFlow):
                    continue

                if is_subcomponent_specification(current_param_values):
                    # complex parameter value, with subcomponents
                    parsed_values = list()
                    for subcomponent in current_param_values:
                        if len(subcomponent) < 2 or len(subcomponent) > 3:
                            raise ValueError('Component reference should be '
                                             'size {2,3}. ')

                        subcomponent_identifier = subcomponent[0]
                        subcomponent_flow = subcomponent[1]
                        if not isinstance(subcomponent_identifier, str):
                            raise TypeError('Subcomponent identifier should be '
                                            'string')
                        if not isinstance(subcomponent_flow,
                                          openml.flows.OpenMLFlow):
                            raise TypeError('Subcomponent flow should be string')

                        current = {
                            "oml-python:serialized_object": "component_reference",
                            "value": {
                                "key": subcomponent_identifier,
                                "step_name": subcomponent_identifier
                            }
                        }
                        if len(subcomponent) == 3:
                            if not isinstance(subcomponent[2], list):
                                raise TypeError('Subcomponent argument should be'
                                                'list')
                            current['value']['argument_1'] = subcomponent[2]
                        parsed_values.append(current)
                    parsed_values = json.dumps(parsed_values)
                else:
                    # vanilla parameter value
                    parsed_values = json.dumps(current_param_values)

                _current['oml:value'] = parsed_values
                if _main_call:
                    _current['oml:component'] = main_id
                else:
                    _current['oml:component'] = _flow_dict[_flow.name]
                _params.append(_current)

            for _identifier in _flow.components:
                subcomponent_model = self._get_module_descriptors(component_model)[_identifier]
                _params.extend(extract_parameters(_flow.components[_identifier],
                                                  _flow_dict, subcomponent_model))
            return _params

        flow_dict = get_flow_dict(flow)
        model = model if model is not None else flow.model
        parameters = extract_parameters(flow, flow_dict, model, True, flow.flow_id)

        return parameters

    def _openml_param_name_to_pytorch(
        self,
        openml_parameter: openml.setups.OpenMLParameter,
        flow: OpenMLFlow,
    ) -> str:
        """
        Converts the name of an OpenMLParameter into the pytorch name, given a flow.

        Parameters
        ----------
        openml_parameter: OpenMLParameter
            The parameter under consideration

        flow: OpenMLFlow
            The flow that provides context.

        Returns
        -------
        pytorch_parameter_name: str
            The name the parameter will have once used in pytorch
        """
        if not isinstance(openml_parameter, openml.setups.OpenMLParameter):
            raise ValueError('openml_parameter should be an instance of OpenMLParameter')
        if not isinstance(flow, OpenMLFlow):
            raise ValueError('flow should be an instance of OpenMLFlow')

        flow_structure = flow.get_structure('name')
        if openml_parameter.flow_name not in flow_structure:
            raise ValueError('Obtained OpenMLParameter and OpenMLFlow do not correspond. ')
        name = openml_parameter.flow_name  # for PEP8
        return '__'.join(flow_structure[name] + [openml_parameter.parameter_name])

    ################################################################################################
    # Methods for hyperparameter optimization

    def instantiate_model_from_hpo_class(
        self,
        model: Any,
        trace_iteration: OpenMLTraceIteration,
    ) -> Any:
        """Instantiate a ``base_estimator`` which can be searched over by the hyperparameter
        optimization model (UNUSED)

        Parameters
        ----------
        model : Any
            A hyperparameter optimization model which defines the model to be instantiated.
        trace_iteration : OpenMLTraceIteration
            Describing the hyperparameter settings to instantiate.

        Returns
        -------
        Any
        """

        return model


    def check_if_model_fitted(self, model: Any) -> bool:
        """Returns True/False denoting if the model has already been fitted/trained
        Parameters
        ----------
        model : Any
        Returns
        -------
        bool
        """