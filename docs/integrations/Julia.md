# OpenML.jl (Julia) Documentation

This is the reference documentation of
[`OpenML.jl`](https://github.com/JuliaAI/OpenML.jl).

The [OpenML platform](https://www.openml.org) provides an integration
platform for carrying out and comparing machine learning solutions
across a broad collection of public datasets and software platforms.

Summary of OpenML.jl functionality:

- [`OpenML.list_tags`](@ref)`()`: for listing all dataset tags
        
- [`OpenML.list_datasets`](@ref)`(; tag=nothing, filter=nothing, output_format=...)`: for listing available datasets

- [`OpenML.describe_dataset`](@ref)`(id)`: to describe a particular dataset

- [`OpenML.load`](@ref)`(id; parser=:arff)`: to download a dataset


## Installation

```julia
using Pkg
Pkg.add("OpenML")
```

If running the demonstration below:

```julia
Pkg.add("DataFrames") 
Pkg.add("ScientificTypes")
```

## Sample usage

```
using OpenML # or using MLJ
using DataFrames

OpenML.list_tags()
```

Listing all datasets with the "OpenML100" tag which also have `n`
instances and `p` features, where `100 < n < 1000` and `1 < p < 10`:

```
ds = OpenML.list_datasets(
          tag = "OpenML100",
          filter = "number_instances/100..1000/number_features/1..10",
          output_format = DataFrame)
```

Describing and loading one of these datasets:

```
OpenML.describe_dataset(15)
table = OpenML.load(15)
```

Converting to a data frame:

```
df = DataFrame(table)
```

Inspecting it's schema:

```
using ScientificTypes
schema(table)
```

## Public API

```@docs
OpenML.list_tags
OpenML.list_datasets
OpenML.describe_dataset
OpenML.load
```

