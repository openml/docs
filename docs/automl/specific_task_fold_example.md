# Example: AutoML on a specific task and fold

The defaults are very useful for performing a quick test, as the datasets are small
and cover different task types (binary classification, multiclass classification, and 
regression). We also have a ["validation" benchmark](GITHUB/resources/benchmarks/validation.yaml)
suite for more elaborate testing that also includes missing data, categorical data, 
wide data, and more. The benchmark defines 9 tasks, and evaluating two folds with a
10-minute time constraint would take roughly 3 hours (=9 tasks * 2 folds * 10 minutes,
plus overhead). Let's instead use the `--task` and `--fold` parameters to run only a
specific task and fold in the `benchmark` when evaluating the 
[flaml](https://microsoft.github.io/FLAML/) AutoML framework:

```
python runbenchmark.py flaml validation test -t eucalyptus -f 0
```

This should take about 10 minutes plus the time it takes to install `flaml`.
Results should look roughly like this:

```
Processing results for flaml.validation.test.local.20230711T122823
Summing up scores for current run:
               id       task  fold framework constraint    result      metric  duration       seed
openml.org/t/2079 eucalyptus     0     flaml       test -0.702976 neg_logloss     611.0 1385946458
```

Similarly to the test run, you will find additional files in the `results` directory.
