# scikit-learn

OpenML is readily integrated with scikit-learn through the [Python API](https://github.com/openml/openml-python).
This page provides a brief overview of the key features and installation instructions. For more detailed API documentation, please refer to the [official documentation](https://openml.github.io/openml-python/main/api.html).

## Key features:

- Query and download OpenML datasets and use them however you like
- Build any sklearn estimator or pipeline and convert to OpenML flows
- Run any flow on any task and save the experiment as run objects
- Upload your runs for collaboration or publishing
- Query, download and reuse all shared runs

## Installation

```bash
pip install openml
```

## Query and download data
```python
import openml

# List all datasets and their properties
openml.datasets.list_datasets(output_format="dataframe")

# Get dataset by ID
dataset = openml.datasets.get_dataset(61)

# Get dataset by name
dataset = openml.datasets.get_dataset('Fashion-MNIST')

# Get the data itself as a dataframe (or otherwise)
X, y, _, _ = dataset.get_data(dataset_format="dataframe")
```

## Download tasks, run models locally, publish results (with scikit-learn)
```python
from sklearn import ensemble
from openml import tasks, runs

# Build any model you like
clf = ensemble.RandomForestClassifier()

# Download any OpenML task
task = tasks.get_task(3954)

# Run and evaluate your model on the task
run = runs.run_model_on_task(clf, task)

# Share the results on OpenML. Your API key can be found in your account.
# openml.config.apikey = 'YOUR_KEY'
run.publish()
```

## OpenML Benchmarks
```python
# List all tasks in a benchmark
benchmark = openml.study.get_suite('OpenML-CC18')
tasks.list_tasks(output_format="dataframe", task_id=benchmark.tasks)

# Return benchmark results
openml.evaluations.list_evaluations(
    function="area_under_roc_curve",
    tasks=benchmark.tasks,
    output_format="dataframe"
)
```
