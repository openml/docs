---
icon: material/rocket-launch
---

## :computer: Installation

The OpenML package is available in many languages and has deep integration in many machine learning libraries.

=== "Python/sklearn"

    - [Python/sklearn repository](https://github.com/openml/openml-python)
    -  `pip install openml`

=== "Pytorch"

    -  [Pytorch repository](https://github.com/openml/openml-pytorch)
    -  `pip install openml-pytorch`

=== "TensorFlow"
    
    - [TensorFlow repository](https://github.com/openml/openml-tensorflow)
    - `pip install openml-tensorflow`
  
=== "R"
        
    - [R repository](https://github.com/openml/openml-R)
    - `install.packages("mlr3oml")`

=== "Julia"
        
    - [Julia repository](https://github.com/JuliaAI/OpenML.jl/tree/master)
    - `using Pkg;Pkg.add("OpenML")`

=== "RUST"
        
    - [RUST repository](https://github.com/mbillingr/openml-rust)
    - Install from source

=== ".Net"
        
    - [.Net repository](https://github.com/openml/openml-dotnet)
    - `Install-Package openMl`

You can find detailed guides for the different libraries in the top menu.


## :key: Authentication

OpenML is entirely open and you do not need an account to access data (rate limits apply). However, <a href="https://www.openml.org" target='blank_'>signing up via the OpenML website</a> is very easy (and free) and required to upload new resources to OpenML and to manage them online.

API authentication happens via an **API key**, which you can find in your profile after logging in to openml.org. 

```
openml.config.apikey = "YOUR KEY"
```

## :joystick: Minimal Example

:material-database: Use the following code to load the [credit-g](https://www.openml.org/search?type=data&sort=runs&status=active&id=31) [dataset](https://docs.openml.org/concepts/data/) directly into a pandas dataframe. Note that OpenML can automatically load all datasets, separate data X and labels y, and give you useful dataset metadata (e.g. feature names and which ones have categorical data).

```python
import openml

dataset = openml.datasets.get_dataset("credit-g") # or by ID get_dataset(31)
X, y, categorical_indicator, attribute_names = dataset.get_data(target="class")
```


:trophy: Get a [task](https://docs.openml.org/concepts/tasks/) for [supervised classification on credit-g](https://www.openml.org/search?type=task&id=31&source_data.data_id=31). 
Tasks specify how a dataset should be used, e.g. including train and test splits.

```python
task = openml.tasks.get_task(31)
dataset = task.get_dataset()
X, y, categorical_indicator, attribute_names = dataset.get_data(target=task.target_name)
# get splits for the first fold of 10-fold cross-validation
train_indices, test_indices = task.get_train_test_split_indices(fold=0)
```

:bar_chart: Use an [OpenML benchmarking suite](https://docs.openml.org/concepts/benchmarking/) to get a curated list of machine-learning tasks:
```python
suite = openml.study.get_suite("amlb-classification-all")  # Get a curated list of tasks for classification
for task_id in suite.tasks:
    task = openml.tasks.get_task(task_id)
```

:star2: You can now benchmark your models easily across many datasets at once. A model training is called a run:

```python
from sklearn import neighbors

task = openml.tasks.get_task(403)
clf = neighbors.KNeighborsClassifier(n_neighbors=5)
run = openml.runs.run_model_on_task(clf, task)
```

:raised_hands: You can now publish your experiment on OpenML so that others can build on it:

```python
myrun = run.publish()
print(f"kNN on {data.name}: {myrun.openml_url}")
```


## Learning more OpenML

Next, check out the :rocket: [10 minute tutorial](notebooks/getting_started.ipynb) and the :mortar_board: [short description of OpenML concepts](concepts/index.md). 