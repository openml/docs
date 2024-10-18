# Random Forest Baseline

Let's try evaluating the `RandomForest` baseline, which uses [scikit-learn](https://scikit-learn.org/stable/)'s random forest:
## Running the Benchmark
### Linux

```bash
python runbenchmark.py randomforest 
```

### MacOS

```bash
python runbenchmark.py randomforest 
```

### Windows
As noted above, we need to install the AutoML frameworks (and baselines) in
a container. Add `-m docker` to the command as shown:
```bash
python runbenchmark.py randomforest -m docker
```

!!! warning "Important"
    Future example usages will only show invocations without `-m docker` mode,
    but Windows users will need to run in some non-local mode.

## Results
After running the command, there will be a lot of output to the screen that reports
on what is currently happening. After a few minutes final results are shown and should 
look similar to this:

```
Summing up scores for current run:
               id        task  fold    framework constraint     result      metric  duration      seed
openml.org/t/3913         kc2     0 RandomForest       test   0.865801         auc      11.1 851722466
openml.org/t/3913         kc2     1 RandomForest       test   0.857143         auc       9.1 851722467
  openml.org/t/59        iris     0 RandomForest       test  -0.120755 neg_logloss       8.7 851722466
  openml.org/t/59        iris     1 RandomForest       test  -0.027781 neg_logloss       8.5 851722467
openml.org/t/2295 cholesterol     0 RandomForest       test -44.220800    neg_rmse       8.7 851722466
openml.org/t/2295 cholesterol     1 RandomForest       test -55.216500    neg_rmse       8.7 851722467
```

The result denotes the performance of the framework on the test data as measured by
the metric listed in the metric column. The result column always denotes performance 
in a way where higher is better (metrics which normally observe "lower is better" are
converted, which can be observed from the `neg_` prefix).

While running the command, the AutoML benchmark performed the following steps:

 1. Create a new virtual environment for the Random Forest experiment. 
    This environment can be found in `frameworks/randomforest/venv` and will be re-used 
    when you perform other experiments with `RandomForest`.
 2. It downloaded datasets from [OpenML](https://www.openml.org) complete with a 
    "task definition" which specifies [cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) folds.
 3. It evaluated `RandomForest` on each (task, fold)-combination in a separate subprocess, where:
    1. The framework (`RandomForest`) is initialized.
    2. The training data is passed to the framework for training.
    3. The test data is passed to the framework to make predictions on.
    4. It passes the predictions back to the main process
 4. The predictions are evaluated and reported on. They are printed to the console and 
    are stored in the `results` directory. There you will find:
    1. `results/results.csv`: a file with all results from all benchmarks conducted on your machine.
    2. `results/randomforest.test.test.local.TIMESTAMP`: a directory with more information about the run,
        such as logs, predictions, and possibly other artifacts.

!!! info "Docker Mode" 

    When using docker mode (with `-m docker`) a docker image will be made that contains
    the virtual environment. Otherwise, it functions much the same way.

## Important Parameters

As you can see from the results above, the  default behavior is to execute a short test
benchmark. However, we can specify a different benchmark, provide different constraints,
and even run the experiment in a container or on AWS. There are many parameters
for the `runbenchmark.py` script, but the most important ones are:

### Framework (required)

- The AutoML framework or baseline to evaluate and is not case-sensitive. See
  [integrated frameworks](https://openml.github.io/automlbenchmark/frameworks.html) for a list of supported frameworks. 
  In the above example, this benchmarked framework `randomforest`.

### Benchmark (optional, default='test')

- The benchmark suite is the dataset or set of datasets to evaluate the framework on.
  These can be defined as on [OpenML](https://www.openml.org) as a [study or task](https://openml.github.io/automlbenchmark/docs/extending/benchmark.md#defining-a-benchmark-on-openml) 
  (formatted as `openml/s/X` or `openml/t/Y` respectively) or in a [local file](https://openml.github.io/automlbenchmark/docs/extending//benchmark.md#defining-a-benchmark-with-a-file).
  The default is a short evaluation on two folds of `iris`, `kc2`, and `cholesterol`.

### Constraints (optional, default='test')

- The constraints applied to the benchmark as defined by default in [constraints.yaml](https://github.com/openml/automlbenchmark/blob/master/resources/constraints.yaml).
  These include time constraints, memory constrains, the number of available cpu cores, and more.
  Default constraint is `test` (2 folds for 10 min each). 

    !!! warning "Constraints are not enforced!"
        These constraints are forwarded to the AutoML framework if possible but, except for
        runtime constraints, are generally not enforced. It is advised when benchmarking
        to use an environment that mimics the given constraints.

    ??? info "Constraints can be overriden by `benchmark`"
        A benchmark definition can override constraints on a task level.
        This is useful if you want to define a benchmark which has different constraints
        for different tasks. The default "test" benchmark does this to limit runtime to
        60 seconds instead of 600 seconds, which is useful to get quick results for its
        small datasets. For more information, see [defining a benchmark](#ADD-link-to-adding-benchmark).

### Mode (optional, default='local')

-  The benchmark can be run in four modes:

     * `local`: install a local virtual environment and run the benchmark on your machine.
     * `docker`: create a docker image with the virtual environment and run the benchmark in a container on your machine. 
                 If a local or remote image already exists, that will be used instead. Requires [Docker](https://docs.docker.com/desktop/).
     * `singularity`: create a singularity image with the virtual environment and run the benchmark in a container on your machine. Requires [Singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html).
     * `aws`: run the benchmark on [AWS EC2](https://aws.amazon.com/free/?trk=b3f93e34-c1e0-4aa9-95f8-6d2c36891d8a&sc_channel=ps&ef_id=CjwKCAjw-7OlBhB8EiwAnoOEk0li05IUgU9Ok2uCdejP22Yr7ZuqtMeJZAdxgL5KZFaeOVskCAsknhoCSjUQAvD_BwE:G:s&s_kwcid=AL!4422!3!649687387631!e!!g!!aws%20ec2!19738730094!148084749082&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all) instances.
              It is possible to run directly on the instance or have the EC2 instance run in `docker` mode.
              Requires valid AWS credentials to be configured, for more information see [Running on AWS](#ADD-link-to-aws-guide).


For a full list of parameters available, run:

```
python runbenchmark.py --help
```
