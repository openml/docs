
<a id='OpenML.jl-Documentation'></a>

<a id='OpenML.jl-Documentation-1'></a>

# OpenML.jl Documentation


This is the reference documentation of [`OpenML.jl`](https://github.com/JuliaAI/OpenML.jl).


The [OpenML platform](https://www.openml.org) provides an integration platform for carrying out and comparing machine learning solutions across a broad collection of public datasets and software platforms.


Summary of OpenML.jl functionality:


  * [`OpenML.list_tags`](index.md#OpenML.list_tags)`()`: for listing all dataset tags
  * [`OpenML.list_datasets`](index.md#OpenML.list_datasets)`(; tag=nothing, filter=nothing, output_format=...)`: for listing available datasets
  * [`OpenML.describe_dataset`](index.md#OpenML.describe_dataset)`(id)`: to describe a particular dataset
  * [`OpenML.load`](index.md#OpenML.load)`(id; parser=:arff)`: to download a dataset


<a id='Installation'></a>

<a id='Installation-1'></a>

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


<a id='Sample-usage'></a>

<a id='Sample-usage-1'></a>

## Sample usage


```julia
julia> using OpenML # or using MLJ


julia> using DataFrames


julia> OpenML.list_tags()
300-element Vector{Any}:
 "study_41"
 "uci"
 "study_34"
 "study_37"
 "mythbusting_1"
 "OpenML-CC18"
 "study_99"
 "artificial"
 "BNG"
 "study_16"
 ⋮
 "Earth Science"
 "Social Media"
 "Meteorology"
 "Geography"
 "Language"
 "Computational Universe"
 "History"
 "Culture"
 "Sociology"
```


Listing all datasets with the "OpenML100" tag which also have `n` instances and `p` features, where `100 < n < 1000` and `1 < p < 10`:


```julia
julia> ds = OpenML.list_datasets(
                 tag = "OpenML100",
                 filter = "number_instances/100..1000/number_features/1..10",
                 output_format = DataFrame)
12×13 DataFrame
 Row │ id     name                              status  MajorityClassSize  Max ⋯
     │ Int64  String                            String  Int64?             Int ⋯
─────┼──────────────────────────────────────────────────────────────────────────
   1 │    11  balance-scale                     active                288      ⋯
   2 │    15  breast-w                          active                458
   3 │    37  diabetes                          active                500
   4 │    50  tic-tac-toe                       active                626
   5 │   333  monks-problems-1                  active                278      ⋯
   6 │   334  monks-problems-2                  active                395
   7 │   335  monks-problems-3                  active                288
   8 │   451  irish                             active                278
   9 │   469  analcatdata_dmft                  active                155      ⋯
  10 │   470  profb                             active                448
  11 │  1464  blood-transfusion-service-center  active                570
  12 │ 40496  LED-display-domain-7digit         active                 57
                                                               9 columns omitted
```


Describing and loading one of these datasets:


```julia
julia> OpenML.describe_dataset(15)
  Author: Dr. William H. Wolberg, University of Wisconsin Source: UCI
  (https://archive.ics.uci.edu/ml/datasets/breast+cancer+wisconsin+(original)),
  University of Wisconsin (http://pages.cs.wisc.edu/~olvi/uwmp/cancer.html) -
  1995 Please cite: See below, plus UCI
  (https://archive.ics.uci.edu/ml/citation_policy.html)

  Breast Cancer Wisconsin (Original) Data Set. Features are computed from a
  digitized image of a fine needle aspirate (FNA) of a breast mass. They
  describe characteristics of the cell nuclei present in the image. The target
  feature records the prognosis (malignant or benign). Original data available
  here (ftp://ftp.cs.wisc.edu/math-prog/cpo-dataset/machine-learn/cancer/)

  Current dataset was adapted to ARFF format from the UCI version. Sample code
  ID's were removed.

  ! Note that there is also a related Breast Cancer Wisconsin (Diagnosis) Data
  Set with a different set of features, better known as wdbc
  (https://www.openml.org/d/1510).

  Relevant Papers
  –––––––––––––––

  W.N. Street, W.H. Wolberg and O.L. Mangasarian. Nuclear feature extraction
  for breast tumor diagnosis. IS&T/SPIE 1993 International Symposium on
  Electronic Imaging: Science and Technology, volume 1905, pages 861-870, San
  Jose, CA, 1993.

  O.L. Mangasarian, W.N. Street and W.H. Wolberg. Breast cancer diagnosis and
  prognosis via linear programming. Operations Research, 43(4), pages 570-577,
  July-August 1995.

  Citation request
  ––––––––––––––––

  This breast cancer database was obtained from the University of Wisconsin
  Hospitals, Madison from Dr. William H. Wolberg. If you publish results when
  using this database, then please include this information in your
  acknowledgments. Also, please cite one or more of:

    1. O. L. Mangasarian and W. H. Wolberg: "Cancer diagnosis via linear
       programming", SIAM News, Volume 23, Number 5, September 1990, pp 1
       & 18.

    2. William H. Wolberg and O.L. Mangasarian: "Multisurface method of
       pattern separation for medical diagnosis applied to breast
       cytology", Proceedings of the National Academy of Sciences,
       U.S.A., Volume 87, December 1990, pp 9193-9196.

    3. O. L. Mangasarian, R. Setiono, and W.H. Wolberg: "Pattern
       recognition via linear programming: Theory and application to
       medical diagnosis", in: "Large-scale numerical optimization",
       Thomas F. Coleman and Yuying Li, editors, SIAM Publications,
       Philadelphia 1990, pp 22-30.

    4. K. P. Bennett & O. L. Mangasarian: "Robust linear programming
       discrimination of two linearly inseparable sets", Optimization
       Methods and Software 1, 1992, 23-34 (Gordon & Breach Science
       Publishers).

julia> table = OpenML.load(15)
Tables.DictColumnTable with 699 rows, 10 columns, and schema:
 :Clump_Thickness        Float64
 :Cell_Size_Uniformity   Float64
 :Cell_Shape_Uniformity  Float64
 :Marginal_Adhesion      Float64
 :Single_Epi_Cell_Size   Float64
 :Bare_Nuclei            Union{Missing, Float64}
 :Bland_Chromatin        Float64
 :Normal_Nucleoli        Float64
 :Mitoses                Float64
 :Class                  CategoricalArrays.CategoricalValue{String, UInt32}
```


Converting to a data frame:


```julia
julia> df = DataFrame(table)
699×10 DataFrame
 Row │ Clump_Thickness  Cell_Size_Uniformity  Cell_Shape_Uniformity  Marginal_ ⋯
     │ Float64          Float64               Float64                Float64   ⋯
─────┼──────────────────────────────────────────────────────────────────────────
   1 │             5.0                   1.0                    1.0            ⋯
   2 │             5.0                   4.0                    4.0
   3 │             3.0                   1.0                    1.0
   4 │             6.0                   8.0                    8.0
   5 │             4.0                   1.0                    1.0            ⋯
   6 │             8.0                  10.0                   10.0
   7 │             1.0                   1.0                    1.0
   8 │             2.0                   1.0                    2.0
  ⋮  │        ⋮                  ⋮                      ⋮                    ⋮ ⋱
 693 │             3.0                   1.0                    1.0            ⋯
 694 │             3.0                   1.0                    1.0
 695 │             3.0                   1.0                    1.0
 696 │             2.0                   1.0                    1.0
 697 │             5.0                  10.0                   10.0            ⋯
 698 │             4.0                   8.0                    6.0
 699 │             4.0                   8.0                    8.0
                                                  7 columns and 684 rows omitted
```


Inspecting it's schema:


```julia
julia> using ScientificTypes


julia> schema(table)
┌───────────────────────┬────────────────────────────┬──────────────────────────
│ names                 │ scitypes                   │ types                   ⋯
├───────────────────────┼────────────────────────────┼──────────────────────────
│ Clump_Thickness       │ Continuous                 │ Float64                 ⋯
│ Cell_Size_Uniformity  │ Continuous                 │ Float64                 ⋯
│ Cell_Shape_Uniformity │ Continuous                 │ Float64                 ⋯
│ Marginal_Adhesion     │ Continuous                 │ Float64                 ⋯
│ Single_Epi_Cell_Size  │ Continuous                 │ Float64                 ⋯
│ Bare_Nuclei           │ Union{Missing, Continuous} │ Union{Missing, Float64} ⋯
│ Bland_Chromatin       │ Continuous                 │ Float64                 ⋯
│ Normal_Nucleoli       │ Continuous                 │ Float64                 ⋯
│ Mitoses               │ Continuous                 │ Float64                 ⋯
│ Class                 │ Multiclass{2}              │ CategoricalValue{String ⋯
└───────────────────────┴────────────────────────────┴──────────────────────────
                                                                1 column omitted
```


<a id='Public-API'></a>

<a id='Public-API-1'></a>

## Public API

### <a id='OpenML.list_tags' href='#OpenML.list_tags'>**`OpenML.list_tags`**</a>




```julia
list_tags()
```

List all available tags.

### <a id='OpenML.list_datasets' href='#OpenML.list_datasets'>**`OpenML.list_datasets`**</a>

```julia
list_datasets(; tag = nothing, filters = "", output_format = NamedTuple)
```

Lists all active OpenML datasets, if `tag = nothing` (default). To list only datasets with a given tag, choose one of the tags in [`list_tags()`](index.md#OpenML.list_tags). An alternative `output_format` can be chosen, e.g. `DataFrame`, if the `DataFrames` package is loaded.

A filter is a string of `<data quality>/<range>` or `<data quality>/<value>` pairs, concatenated using `/`, such as

```julia
    filter = "number_features/10/number_instances/500..10000"
```

The allowed data qualities include `tag`, `status`, `limit`, `offset`, `data_id`, `data_name`, `data_version`, `uploader`, `number_instances`, `number_features`, `number_classes`, `number_missing_values`.

For more on the format and effect of `filters` refer to the [openml API](https://www.openml.org/api_docs#!/data/get_data_list_filters).

**Examples**

```julia
julia> using DataFrames

julia> ds = OpenML.list_datasets(
               tag = "OpenML100",
               filter = "number_instances/100..1000/number_features/1..10",
               output_format = DataFrame
)

julia> sort!(ds, :NumberOfFeatures)
```

### <a id='OpenML.describe_dataset' href='#OpenML.describe_dataset'>**`OpenML.describe_dataset`**</a>

```julia
describe_dataset(id)
```

Load and show the OpenML description of the data set `id`. Use [`list_datasets`](index.md#OpenML.list_datasets) to browse available data sets.

**Examples**

```julia
julia> OpenML.describe_dataset(6)
  Author: David J. Slate Source: UCI
  (https://archive.ics.uci.edu/ml/datasets/Letter+Recognition) - 01-01-1991 Please cite: P.
  W. Frey and D. J. Slate. "Letter Recognition Using Holland-style Adaptive Classifiers".
  Machine Learning 6(2), 1991

    1. TITLE:

  Letter Image Recognition Data

  The objective is to identify each of a large number of black-and-white
  rectangular pixel displays as one of the 26 capital letters in the English
  alphabet.  The character images were based on 20 different fonts and each
  letter within these 20 fonts was randomly distorted to produce a file of
  20,000 unique stimuli.  Each stimulus was converted into 16 primitive
  numerical attributes (statistical moments and edge counts) which were then
  scaled to fit into a range of integer values from 0 through 15.  We
  typically train on the first 16000 items and then use the resulting model
  to predict the letter category for the remaining 4000.  See the article
  cited above for more details.
```

### <a id='OpenML.load' href='#OpenML.load'>**`OpenML.load`**</a>



```julia
OpenML.load(id; maxbytes = nothing)
```

Load the OpenML dataset with specified `id`, from those listed by [`list_datasets`](index.md#OpenML.list_datasets) or on the [OpenML site](https://www.openml.org/search?type=data).

Datasets are saved as julia artifacts so that they persist locally once loaded.

Returns a table.

**Examples**

```julia
using DataFrames
table = OpenML.load(61)
df = DataFrame(table) # transform to a DataFrame
using ScientificTypes
df2 = coerce(df, autotype(df)) # corce to automatically detected scientific types

peek_table = OpenML.load(61, maxbytes = 1024) # load only the first 1024 bytes of the table
```

