## Building clients ##
You can access OpenML datasets, pipelines, benchmarks, and much more, through a range of client APIs.
Well-developed clients exist in Python, R, Java, and several other languages. Please see their documentation (in the other tabs)
for more guidance of how to contribute to them.

If you want to develop your own client (e.g. for a new language), please check out the following resources:  

* [REST API](./Rest.md): all endpoints to GET, POST, or DELETE resources
* [Metadata Standard](./metadata_definition.md): how we describe datasets and all other OpenML resources
* Minimal standards (below) for uniform client configuration and caching mechanisms, to make the client behavior more uniform across languages.

!!! info "Integrating tools"
    If you want to integrate OpenML into machine learning and data science tools, it's often easier to build on one of the existing clients, 
    which often can be used as is or extended. For instance, see how to [extend the Python API](./creating_extensions.md) to integrate OpenML into Python tools. 


## Minimal standards

### Configuration file

The configuration file resides in a directory `.openml` in the home directory of the user and is called config. It consists of `key = value` pairs which are seperated by newlines. The following keys are defined:

  * apikey:
    * required to access the server
  * server:
    * default: `http://www.openml.org`
  * verbosity:
    * 0: normal output
    * 1: info output
    * 2: debug output
  * cachedir:
    * if not given, will default to `file.path(tempdir(), "cache")`.

### Caching

#### Cache invalidation

All parts of the entities which affect experiments are immutable. The entities dataset and task have a flag `status` which tells the user whether they can be used safely.

#### File structure

Caching should be implemented for

  * datasets
  * tasks
  * splits
  * predictions

and further entities might follow in the future. The cache directory `$cache` should be specified by the user when invoking the API. The structure in the cache directory should be as following:

  * One directory for the following entities:
    * `$cache/datasets`
    * `$cache/tasks`
    * `$cache/runs`
  * For every dataset there is an extra directory for which the name is the dataset ID, e.g. `$cache/datasets/2` for the dataset with OpenML ID 2.
    * The dataset should be called `dataset.pq` or `dataset.arff`
    * Every other file should be named by the API call which was used to obtain it. The XML returned by invoking `openml.data.qualities` should therefore be called qualities.xml.
  * For every task there is an extra directory for which the name is the task ID, e.g. `$cache/tasks/1`
    * The task file should be called `task.xml`.
    * The splits accompanying a task are stored in a file `datasplits.arff`.
  * For every run there is an extra directory for which the name is the run ID, e.g. `$cache/run/1`
    * The predictions should be called `predictions.arff`.