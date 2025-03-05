# Using datasets

## Discovery
OpenML allows fine-grained search over thousands of machine learning datasets. 

### Web UI
Via the <a href="https://www.openml.org">website</a>, you can filter by many dataset properties, such as size, type, format, and many more. 
It also allows you to explore every dataset via [interactive dashboards](../concepts/data).

![](../img/data-ss.png){ width="100%" style="max-width: 700px;" }

### API
Via our [APIs](https://www.openml.org/apis) you have access to many more filters, and you can download a complete table with statistics of all datasest.

=== "Python"

    ``` python
    import openml

    # List all datasets and their properties
    # It's possible to filter on status, tags, and meta-data attributes
    openml.datasets.list_datasets(output_format="dataframe", status="active", tag="vision")
    ```
    
    ```plaintext
    did	    name                version	uploader	status	NumberOfClasses	....
	554	    mnist_784	        1	    2	        active	10	
	40923	Devnagari-Script	1	    3948	    active	46	
	40927	CIFAR_10	        1	    2	        active	10	
	40996	Fashion-MNIST	    1	    2506	    active	10	
	41039	EMNIST_Balanced	    1	    2506	    active	47	
	41081	SVHN	            1	    2506	    active	10	
	41082	USPS	            2	    2506	    active	10	
	41083	Olivetti_Faces	    1	    2506	    active	40	
	41084	UMIST_Faces_Cropped	1	    2506	    active	20	
	41103	STL-10	            1	    2506	    active	10	
	42766	kits-subset	        4	    9186	    active	2
    ...	    ...	                ...	    ... 	    ...     ...
    ```

=== "R"

    ``` r
    library(mlr3oml)
    library(mlr3)

    # Search for specific datasets
    odatasets = list_oml_data(
    number_features = c(10, 20),
    number_instances = c(45000, 50000),
    number_classes = 2
    )
    ```

=== "Julia"

    ``` julia
    using OpenML
    using DataFrames

    # List all datasets and their properties
    ds = OpenML.list_datasets(output_format = DataFrame)
    ```

=== "Java"

    ``` java
    import org.openml.apiconnector.io.ApiConnector;

    // Create a client. Your API key can be found in your account.
    OpenmlConnector openml = new OpenmlConnector("api_key");

    // List all datasets and their properties
    DataSet[] datasets = openml.dataList();
    ```


## Loading data

### Web UI
Via the OpenML website, you can download datasets with the 'download' button, or download a JSON, XML, or Croissant description of the dataset.

![](../img/editdata.png){ width="100%" style="max-width: 700px;" }

### API
You can load data directly into common data structures in you language of choice. No need to run data loaders.

=== "Python"

    ``` python
    import openml

    # Get dataset by ID
    dataset = openml.datasets.get_dataset(61)

    # Get dataset by name
    dataset = openml.datasets.get_dataset('Fashion-MNIST')

    # Get the data itself. Returns a pandas dataframe by default.
    X, _, _, _ = dataset.get_data()

    # Other data formats can be requested (e.g. numpy)
    # Target features, feature names and types are also returned 
    X, y, is_categorical, feat_names = dataset.get_data(
        dataset_format="array", target=dataset.default_target_attribute)
    ```

=== "R"

    ``` r
    library(mlr3oml)
    library(mlr3)

    # Get dataset by ID
    odata = odt(id = 1590)

    # Access the actual data
    odata$data
    ```

=== "Julia"

    ``` julia
    using OpenML
    using DataFrames

    # Get dataset by ID
    OpenML.describe_dataset(40996)

    # Get the data itself as a dataframe (or otherwise)
    table = OpenML.load(40996)
    df = DataFrame(table)
    ```

=== "Java"

    ``` java
    import org.openml.apiconnector.io.ApiConnector;

    // Create a client. Your API key can be found in your account.
    OpenmlConnector openml = new OpenmlConnector("api_key");

    // Get dataset by ID
    DataSetDescription data = openml.dataGet(40996);
    String file_url = data.getUrl();
    ```

### Library integrations

You can also easily feed the data directly into common machine learning libraries

=== "scikit-learn"

    ``` python
    import openml
    from sklearn import ensemble

    # Get dataset by ID
    dataset = openml.datasets.get_dataset(20)

    # Get the X, y data
    X, y, _, _ = dataset.get_data(target=dataset.default_target_attribute)

    # Create a model and train it
    clf = ensemble.RandomForestClassifier()
    clf.fit(X, y)
    ```

=== "PyTorch"

    ``` python
    import torch.nn
    import openml_pytorch
    import torchvision
    from torchvision.transforms import Compose, Resize, ToPILImage, ToTensor, Lambda

    # Image to tensor conversion
    transform = Compose(
        [
            ToPILImage(),  # Convert tensor to PIL Image to ensure PIL Image operations can be applied.
            Lambda(
                convert_to_rgb
            ),  # Convert PIL Image to RGB if it's not already.
            Resize(
                (64, 64)
            ),  # Resize the image.
            ToTensor(),  # Convert the PIL Image back to a tensor.
        ]
    )

    # Create a data loader
    data_module = OpenMLDataModule(
        type_of_data="image",
        file_dir="datasets",
        filename_col="image_path",
        target_mode="categorical",
        target_column="label",
        batch_size = 64,
        transform=transform
    )

    # Create a trainer module
    trainer = OpenMLTrainerModule(
        data_module=data_module,
        verbose = True,
        epoch_count = 1,
        callbacks=[],
    )
    openml_pytorch.config.trainer = trainer

    # Download an OpenML task and a Pytorch model
    task = openml.tasks.get_task(362128)
    model = torchvision.models.efficientnet_b0(num_classes=200)

    # Run the model on the OpenML task
    run = openml.runs.run_model_on_task(model, task, avoid_duplicate_runs=False)
    ```

=== "Tensorflow"

    ``` python
    import openml
    import openml_tensorflow
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    import tensorflow as tf
    from tensorflow.keras import layers, models

    # Configure OpenML based on datasets meta-data
    datagen = ImageDataGenerator()
    openml_tensorflow.config.datagen = datagen
    openml_tensorflow.config.dir = openml.config.get_cache_directory()+'/datasets/44312/PNU_Micro/images/'
    openml_tensorflow.config.x_col = "FILE_NAME"
    openml_tensorflow.config.y_col = 'encoded_labels'
    openml_tensorflow.config.datagen = datagen
    openml_tensorflow.config.batch_size = 32
    openml_tensorflow.config.epoch = 1
    openml_tensorflow.config.class_mode = "categorical"

    # Set up cross-validation
    openml_tensorflow.config.perform_validation = True
    openml_tensorflow.config.validation_split = 0.1
    openml_tensorflow.config.datagen_valid = ImageDataGenerator()

    IMG_SIZE = (128, 128)
    IMG_SHAPE = IMG_SIZE + (3,)

    # Example tensorflow image classification model. 
    model = models.Sequential()
    model.add(layers.Conv2D(128, (3, 3), activation='relu', input_shape=IMG_SHAPE))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(84, activation='relu'))
    model.add(layers.Dense(19, activation='softmax'))  # Adjust output size
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['AUC'])

    # Download the OpenML task for the Meta_Album_PNU_Micro dataset.
    task = openml.tasks.get_task(362071)

    # Run the Keras model on the task (requires an API key).
    run = openml.runs.run_model_on_task(model, task, avoid_duplicate_runs=False)
    ```
=== "mlr3"

    ``` r
    library(mlr3oml)
    library(mlr3)

    # create an mlr3 Learner and Resampling and run a resample experiment
    sample(
        task = tsk_adult,
        learner = lrn("classif.rpart"),
        resampling = rsmp("cv", folds = 10)
    )
    ```

### Croissant support

OpenML will automatically create a Croissant description when you create (or edit) an OpenML dataset.
Croissant also has data loaders that allow you to load the data and import it into AI tools.


#### Getting the Croissant file
You can fetch a dataset's Croissant file from the dataset detail page on the OpenML website. Simply click the croissant icon.

![](../img/editdata.png){ width="100%" style="max-width: 700px;" }

You can also retrieve the url for the Croissant file using the API

``` python
    import openml
    import requests

    # Get dataset by name
    dataset = openml.datasets.get_dataset('Fashion-MNIST')

    # Get the croissant URL
    # Currently this works via a predictive naming scheme
    croissant_url = dataset._parquet_url.replace(".pq","_croissant.json")

    # Download the croissant file
    response = requests.get(croissant_url)
    croissant = response.json()
```

#### Loading data

With the croissant URL you can load the data into common data structures.
Here, we use TFRecords:

``` python
    import mlcroissant as mlc

    # Create a croissant dataset
    ds = mlc.Dataset(croissant_url)

    # Load the data
    tfr = ds.records(record_set="default")
```

#### Loading data into ML tools

You can load croissant datasets directly into AI tools as well.
Here, we use TensorFlow:

``` python
    import mlcroissant as mlc
    import tensorflow_datasets as tfds

    # Create dataset builder
    builder = tfds.core.dataset_builders.CroissantBuilder(
        jsonld=croissant_url,
        record_set_ids=["record_set_fashion_mnist"],
        file_format='array_record',
    )
    builder.download_and_prepare()

    # Train-test split
    train, test = builder.as_data_source(split=['train', 'test'])

    # Create dataloaders
    batch_size = 128
    train_sampler = torch.utils.data.RandomSampler(train, num_samples=len(train))
    train_loader = torch.utils.data.DataLoader(
        train,
        sampler=train_sampler,
        batch_size=batch_size,
    )
    test_loader = torch.utils.data.DataLoader(
        test,
        sampler=None,
        batch_size=batch_size,
    )

    # Train a model
    shape = train[0]["image"].shape
    num_classes = 10
    model = LinearClassifier(shape, num_classes)
    model.train()
```

Check the Croissant repository for [more recipes](https://github.com/mlcommons/croissant/tree/main/python/mlcroissant/recipes).