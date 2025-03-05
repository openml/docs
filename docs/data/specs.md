# Technical specifications

## Data formatting
OpenML converts datasets to a uniform format based on Parquet. Read [this blog post](https://blog.openml.org/openml/data/2020/03/23/Finding-a-standard-dataset-format-for-machine-learning.html) for a detailed explanation for this approach. You will usually never notice this since OpenML libraries will take care of transferring data from Parquet to your favorite data structures. See the [using datasets](use.md) page for details.

Datasets that depend on included files (e.g. a dataset of images) are defined by create a dataframe with all the dataset information, and columns with paths to local files, as well as a folder with all the local files (e.g. images, video, audio) according to the paths in main dataframe.

In the backend, datasets are stored in an S3 object store, with one bucket per dataset. We currently allow datasets to be up to 200GB in size.

## Dataset ID and versions
A dataset can be uniquely identified by its dataset ID, which is shown on the website and returned by the API. It's `1596` in the `covertype` example above. They can also be referenced by name and ID. OpenML assigns incremental version numbers per upload with the same name. You can also add a free-form `version_label` with every upload.

## Dataset status
When you upload a dataset, it will be marked `in_preparation` until it is (automatically) verified. Once approved, the dataset will become `active` (or `verified`). If a severe issue has been found with a dataset, it can become `deactivated` (or `deprecated`) signaling that it should not be used. By default, dataset search only returns verified datasets, but you can access and download datasets with any status.

## Caching
When downloading datasets, tasks, runs and flows, OpenML will automatically cache them locally. By default, OpenML will use ~/.openml/cache as the cache directory

The cache directory can be either specified through the OpenML config file. To do this, add the line `cachedir = ‘MYDIR’` to the config file, replacing ‘MYDIR’ with the path to the cache directory.

You can also set the cache dir temporarily via the Python API:

``` python
    import os
    import openml
    
    openml.config.cache_directory = os.path.expanduser('YOURDIR')
```


