# Flows

Flows are machine learning pipelines, models, or scripts that can transform data into a model.
They often have a number of hyperparameters which may be configured (e.g., a Random Forest's "number of trees" hyperparameter).
Flows are, for example, scikit-learn's `RandomForestClassifier`, mlr3's `"classif.rpart"`, or WEKA's `J48`, but can also be "AutoML Benchmark's autosklearn integration" or any other script.
The metadata of a flow describes, if provided, the configurable hyperparameters, their default values, and recommended ranges.
They _do not_ describe a specific configuration ([setups](./runs.md#setups) log the configuration of a flow used in a [run](./runs.md)).

They are typically uploaded directly from machine learning libraries (e.g. scikit-learn, pyTorch, TensorFlow, MLR, WEKA,...) via the corresponding [APIs](https://www.openml.org/apis), but is possible to define them manually too (see also [this example of openml-python](http://openml.github.io/openml-python/latest/examples/Basics/simple_flows_and_runs_tutorial/) or the REST API documentation). Associated code (e.g., on GitHub) can be referenced by URL.


!!! note "Versions"

    It is convention to distinguish between software versions through the Flow's `external_version` property.
    This is because both internal and external changes can be made to code the Flow references, which would affect people using them.
    For example, hyperparameters may be introduced or deprecated across different versions of the same algorithm, or their internal behavior may change (and result in different models).
    Automatically generated flows from e.g. `openml-python` or `mlr3oml` automatically populated the `external_version` property.

## Analysing algorithm performance

Every flow gets a dedicated page with information about the flow, such as its dependencies, hyperparameters, and which runs used it. The Analysis tab shows an automated interactive analysis of all collected results. For instance, below are the results of a <a href="https://www.openml.org/f/17691" target="_blank">scikit-learn pipeline</a> including missing value imputation, feature encoding, and a RandomForest model. It shows the results across multiple tasks and configurations, and how the AUC score is affected by certain hyperparameters.

<!-- <img src="img/flow_top.png" style="width:100%; max-width:800px;"/> -->
![](../img/flow_top.png)

This helps to better understand specific models, as well as their strengths and weaknesses.

## Automated sharing

When you evaluate algorithms and share the results using `openml-python` or `mlr3oml` details of the algorithm (dependencies, structure, and all hyperparameters) are automatically extracted and can easily be shared. When the Flow is used in a Run, the specific hyperparameter configuration used in the experiment is also saved separately in a Setup. The code snippet below creates a Flow description for the RandomForestClassifier, and also runs the experiment. The resulting Run contains information about the used configuration of the Flow in the experiment (Setup).

``` python
    from sklearn import ensemble
    from openml import tasks, runs

    # Build any model you like.
    clf = ensemble.RandomForestClassifier()

    # Evaluate the model on a task
    run = runs.run_model_on_task(clf, task)

    # Share the results, including the flow and all its details.
    run.publish()
```

## Reproducing algorithms and experiments

Given an OpenML run, the exact same algorithm or model, with exactly the same hyperparameters, can be reconstructed within the same machine learning library to easily reproduce earlier results. 

``` python
    from openml import runs

    # Rebuild the (scikit-learn) pipeline from run 9864498
    model = openml.runs.initialize_model_from_run(9864498)
```

!!! note
    You may need the exact same library version to reconstruct flows. The API will always state the required version.
