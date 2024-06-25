# Example: Benchmarks on OpenML

In the previous examples, we used benchmarks which were defined in a local file
([test.yaml](GITHUB/resources/benchmarks/test.yaml) and 
[validation.yaml](GITHUB/resources/benchmarks/validation.yaml), respectively). 
However, we can also use tasks and
benchmarking suites defined on OpenML directly from the command line. When referencing
an OpenML task or suite, we can use `openml/t/ID` or `openml/s/ID` respectively as 
argument for the benchmark parameter. Running on the [iris task](https://openml.org/t/59):

```
python runbenchmark.py randomforest openml/t/59
```

or on the entire [AutoML benchmark classification suite](https://openml.org/s/271) (this will take hours!):

```
python runbenchmark.py randomforest openml/s/271
```

!!! info "Large-scale Benchmarking"

    For large scale benchmarking it is advised to parallelize your experiments,
    as otherwise it may take months to run the experiments.
    The benchmark currently only supports native parallelization in `aws` mode
    (by using the `--parallel` parameter), but using the `--task` and `--fold` parameters 
    it is easy to generate scripts that invoke individual jobs on e.g., a SLURM cluster.
    When you run in any parallelized fashion, it is advised to run each process on
    separate hardware to ensure experiments can not interfere with each other.