## Data Formats

OpenML aims to achieve full data interoperability, meaning that you can load all datasets in a uniform way (a 'universal dataloader'). This requires
that all datasets are stored in the same dataformat (or a set of interoperable formats), or at least have a version of it stored in that format. After
an intensive study, [which you can read on our blog](https://blog.openml.org/openml/data/2020/03/23/Finding-a-standard-dataset-format-for-machine-learning.html),
we settled on the [Parquet format](https://parquet.apache.org/#:~:text=Apache%20Parquet%20is%20an%20open,programming%20language%20and%20analytics%20tools).

This means that all OpenML datasets can be retrieved in the Parquet format. They are also stored on our servers in this format. Oftentimes, you will not notice this, as the OpenML clients can automatically convert data into your preferred data structures, and be fed directly into machine learning workflows. For example:

```python
import openml
dataset = openml.datasets.get_dataset("Fashion-MNIST")     # Returns the dataset meta-data 
X, y, _, _ = dataset.get_data(dataset_format="dataframe",  # Downloads the data and returns a Pandas dataframe
                target=dataset.default_target_attribute)

from sklearn.ensemble import GradientBoostingClassifier         # Using a sklearn model as an example
model = GradientBoostingClassifier(n_estimators=10).fit(X, y)   # Set hyperparameters and train the model 
```

To guarantee interoperability, we focus on a limited set of data formats.

### Tabular data
OpenML has historically focussed on tabular data, and has extensive support for all kinds of tabular data. As explained above, we store all data in the [Parquet format](https://parquet.apache.org/#:~:text=Apache%20Parquet%20is%20an%20open,programming%20language%20and%20analytics%20tools). You can upload data from many different data structures, such as Pandas dataframes and R dataframes, after which they will be converted and stored in Parquet. You can also upload datasets as CSV files or [ARFF files](https://www.cs.waikato.ac.nz/ml/weka/arff.html), and we aim to allow direct Parquet uploads soon.

!!! tip "ARFF legacy"
    At the moment, some aspects of OpenML still has a dependency on the ARFF format. This will be fully phased out in favor of Parquet.

### Image data
OpenML generally supports other data types by requiring a 'header table', a table (stored in Parquet) listing all data instances with additional meta-data (e.g. classes, bounding boxes,...) and references to data files, such as images (e.g. JPGs), stored in seperate folders. [See our blog post for details](https://blog.openml.org/openml/data/2020/03/23/Finding-a-standard-dataset-format-for-machine-learning.html). We will provide more detailed guidelines here as soon as possible.

## Data repositories

This is a list of public dataset repositories that offer additional useful machine learning datasets.
These have widely varying data formats, so they require manual selection, parsing and meta-data extraction.

A collection of sources made by different users

- https://github.com/caesar0301/awesome-public-datasets
- https://dreamtolearn.com/ryan/1001_datasets
- https://en.wikipedia.org/wiki/List_of_datasets_for_machine-learning_research
- https://pathmind.com/wiki/open-datasets
- https://paperswithcode.com/
- https://medium.com/towards-artificial-intelligence/best-datasets-for-machine-learning-data-science-computer-vision-nlp-ai-c9541058cf4f
- https://lionbridge.ai/datasets/the-50-best-free-datasets-for-machine-learning/
- https://www.v7labs.com/open-datasets?utm_source=v7&utm_medium=email&utm_campaign=edu_outreach

Machine learning dataset repositories (mostly already in OpenML)

- UCI: https://archive.ics.uci.edu/ml/index.html
- KEEL: http://sci2s.ugr.es/keel/datasets.php
- LIBSVM: http://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/
- AutoWEKA datasets: http://www.cs.ubc.ca/labs/beta/Projects/autoweka/datasets/
- skData package: https://github.com/jaberg/skdata/tree/master/skdata
- Rdatasets: http://vincentarelbundock.github.io/Rdatasets/datasets.html
- DataBrewer: https://github.com/rmax/databrewer
- liac-arff: https://github.com/renatopp/arff-datasets

MS Open datasets:

- https://azure.microsoft.com/en-us/services/open-datasets/catalog/

APIs (mostly defunct):

- databrewer (Python): https://pypi.org/project/databrewer/
- PyDataset (Python): https://github.com/iamaziz/PyDataset (wrapper for Rdatasets?)
- RDatasets (R): https://github.com/vincentarelbundock/Rdatasets

Time series / Geo data:

- Data commons: https://datacommons.org/
- UCR: http://timeseriesclassification.com/
- Older version: http://www.cs.ucr.edu/~eamonn/time_series_data/

Deep learning datasets (mostly image data)

- https://www.tensorflow.org/datasets/catalog/overview
- http://deeplearning.net/datasets/
- https://deeplearning4j.org/opendata
- http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html
- https://paperswithcode.com/datasets

Extreme classification:

- http://manikvarma.org/downloads/XC/XMLRepository.html

MLData (down)

- http://mldata.org/

AutoWEKA datasets:

- http://www.cs.ubc.ca/labs/beta/Projects/autoweka/datasets/

Kaggle public datasets

- https://www.kaggle.com/datasets

RAMP Challenge datasets

- http://www.ramp.studio/data_domains

Wolfram data repository

- http://datarepository.wolframcloud.com/

Data.world

- https://data.world/

Figshare (needs digging, lots of Excel files)

- https://figshare.com/search?q=dataset&quick=1

KDNuggets list of data sets (meta-list, lots of stuff here):

- http://www.kdnuggets.com/datasets/index.html

Benchmark Data Sets for Highly Imbalanced Binary Classification

- http://www.cs.gsu.edu/~zding/research/imbalance-data/x19data.txt

Feature Selection Challenge Datasets

- http://www.nipsfsc.ecs.soton.ac.uk/datasets/
- http://featureselection.asu.edu/datasets.php

BigML's list of 1000+ data sources

- http://blog.bigml.com/2013/02/28/data-data-data-thousands-of-public-data-sources/

Massive list from Data Science Central.

- http://www.datasciencecentral.com/profiles/blogs/data-sources-for-cool-data-science-projects

R packages (also see https://github.com/openml/openml-r/issues/185)

- http://stat.ethz.ch/R-manual/R-patched/library/datasets/html/00Index.html
- mlbench
- Stata datasets: http://www.stata-press.com/data/r13/r.html

UTwente Activity recognition datasets:

- http://ps.ewi.utwente.nl/Datasets.php

Vanderbilt:

- http://biostat.mc.vanderbilt.edu/wiki/Main/DataSets

Quandl

- https://www.quandl.com

Microarray data:

- http://genomics-pubs.princeton.edu/oncology/
- http://svitsrv25.epfl.ch/R-doc/library/multtest/html/golub.html

Medical data:

- http://www.healthdata.gov/
- http://homepages.inf.ed.ac.uk/rbf/IAPR/researchers/PPRPAGES/pprdat.htm
- http://hcup-us.ahrq.gov/
- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Physician-and-Other-Supplier.html
- https://nsduhweb.rti.org/respweb/homepage.cfm
- http://orwh.od.nih.gov/resources/policyreports/womenofcolor.asp

Nature.com Scientific data repositories list

- https://www.nature.com/sdata/policies/repositories
