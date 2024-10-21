# Machine Learning in R (mlr)

OpenML is readily integrated with mlr through the [mlr3oml](https://mlr3oml.mlr-org.com/index.html) package.

!!! example
    ```r
    library(mlr3oml)
    library(mlr3)

    # Search for specific datasets
    odatasets = list_oml_data(
    number_features = c(10, 20),
    number_instances = c(45000, 50000),
    number_classes = 2
    )

    # Get dataset
    odata = odt(id = 1590)
    # Access the actual data
    odata$data

    # Convert to an mlr3::Task
    tsk_adult = as_task(odata, target = "class")
    ```

Key features:  

* Query and download OpenML datasets and use them however you like  
* Build any mlr learner, run it on any task and save the experiment as run objects  
* Upload your runs for collaboration or publishing  
* Query, download and reuse all shared runs  

There is also an older (deprecated) [OpenML R package](http://openml.github.io/openml-r/).
