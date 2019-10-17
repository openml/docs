OpenML is at its core a database, from which entities can be downloaded and to which entities can be uploaded. Although there are various interfaces for these, at the core all communication with the database goes through the API. In this document, we describe the standard how to upload entities to OpenML and what the resulting database state will be.

## Data

Data is uploaded through the function [post data](https://www.openml.org/api_docs#!/data/post_data). The following files are needed:

* description: An XML adhiring to the [XSD schema](https://www.openml.org/api_new/v1/xsd/openml.data.upload).
* dataset: An [ARFF file](https://www.cs.waikato.ac.nz/ml/weka/arff.html) containing the data (optional, if not set, there should be an URL in the description, pointing to this file). 

## Tasks
TODO.

## FLow

Flows are uploaded through the function [post flow](https://www.openml.org/api_docs#!/flow/post_flow). The following file is needed:

* description: An XML adhiring to the [XSD schema](https://www.openml.org/api_new/v1/xsd/openml.flow.upload).

## Runs

Runs are uploaded through the function [post run](https://www.openml.org/api_docs#!/run/post_run). The following files are needed:

* description: An XML adhiring to the [XSD schema](https://www.openml.org/api_new/v1/xsd/openml.run.upload).
* predictions: An [ARFF file](https://www.cs.waikato.ac.nz/ml/weka/arff.html) containing the predictions (optional, depending on the task).
* trace: An [ARFF file](https://www.cs.waikato.ac.nz/ml/weka/arff.html) containing the run trace (optional, depending on the flow).

### Predictions

The contents of the prediction file depends on the task type. 

#### Task type: Supervised classification

* repeat NUMERIC
* fold NUMERIC
* row_id NUMERIC
* confidence.{$classname}: optional. various columns, describing the confidence per class. The values of these columns should add to 1 (precision 1e-6). 
* (proposal) decision_function.{$classname}: optional. various columns, describing decision function per class. 
* prediction {$classname}
Runs that have a different set of columns will be rejected.

### Trace

* repeat numeric
* fold numeric
* iteration numeric
* setup_string string, contains hyperparameters and settings of the optimizee (should be json parsable)
* evaluation numeric
* selected {false,true}
(open question) what is in the same fold/repeat combination the same config is ran multiple times with same evaluation?