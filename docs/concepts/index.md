# Concepts  

## OpenML concepts 
OpenML operates on a number of core concepts which are important to understand: 

**<span style="color:green">:fontawesome-solid-database: Datasets</span>**  
Datasets are pretty straight-forward. Tabular datasets are self-contained, consisting of a number of rows (_instances_) and columns (features), including their data types. Other 
modalities (e.g. images) are included via paths to files stored within the same folder.  
Datasets are uniformly formatted ([S3](https://min.io/product/s3-compatibility) buckets with [Parquet](https://parquet.apache.org/) tables, [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) metadata, and media files), and are auto-converted and auto-loaded in your desired format by the [APIs](https://www.openml.org/apis) (e.g. in [Python](https://openml.github.io/openml-python/main/)) in a single line of code.  
_Example: The <a href="https://www.openml.org/d/61" target="_blank">Iris dataset</a> or the <a href="https://www.openml.org/d/44282" target="_blank">Plankton dataset</a>_


**<span style="color:#f0ad4e">:fontawesome-solid-trophy: Tasks</span>**  
A task consists of a dataset, together with a machine learning task to perform, such as classification or clustering and an evaluation method. For
supervised tasks, this also specifies the target column in the data.  
_Example: <a href="https://www.openml.org/t/59" target="_blank">Classifying different iris species</a> from other attributes and evaluate using 10-fold cross-validation._

**<span style="color:#5488e8">:material-cogs: Flows</span>**  
A flow identifies a particular machine learning algorithm (a pipeline or untrained model) from a particular library or framework, such as scikit-learn, pyTorch, or MLR. It contains details about the structure of the model/pipeline, dependencies (e.g. the library and its version) and a list of settable hyperparameters. In short, it is a serialized description of the algorithm that in many cases can also be deserialized to reinstantiate the exact same algorithm in a particular library.   
_Example: <a href="https://www.openml.org/f/18998" target="_blank">scikit-learn's RandomForest</a> or a <a href="https://www.openml.org/f/18578" target="_blank">simple TensorFlow model</a>_

**<span style="color:red">:fontawesome-solid-star: Runs</span>**  
A run is an experiment - it evaluates a particular flow (pipeline/model) with particular hyperparameter settings, on a particular task. Depending on the task it will include certain results, such as model evaluations (e.g. accuracies), model predictions, and other output files (e.g. the trained model).  
_Example: <a href="https://www.openml.org/r/10591758" target="_blank">Classifying Gamma rays with scikit-learn's RandomForest</a>_