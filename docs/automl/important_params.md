# Important Parameters

As you can see from the results above, the  default behavior is to execute a short test
benchmark. However, we can specify a different benchmark, provide different constraints,
and even run the experiment in a container or on AWS. There are many parameters
for the `runbenchmark.py` script, but the most important ones are:

`Framework (required)`

- The AutoML framework or baseline to evaluate and is not case-sensitive. See
  [integrated frameworks](WEBSITE/frameworks.html) for a list of supported frameworks. 
  In the above example, this benchmarked framework `randomforest`.

`Benchmark (optional, default='test')`

- The benchmark suite is the dataset or set of datasets to evaluate the framework on.
  These can be defined as on [OpenML](https://www.openml.org) as a [study or task](extending/benchmark.md#defining-a-benchmark-on-openml) 
  (formatted as `openml/s/X` or `openml/t/Y` respectively) or in a [local file](extending/benchmark.md#defining-a-benchmark-with-a-file).
  The default is a short evaluation on two folds of `iris`, `kc2`, and `cholesterol`.

`Constraints (optional, default='test')`

- The constraints applied to the benchmark as defined by default in [constraints.yaml](GITHUB/resources/constraints.yaml).
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

`Mode (optional, default='local')`

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