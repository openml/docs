# Pytorch extension for OpenML python

Pytorch extension for [openml-python API](https://github.com/openml/openml-python).

#### Installation Instructions:

`pip install openml-pytorch`

PyPi link https://pypi.org/project/openml-pytorch/

## Usage
To use this extension, you need to have a task from OpenML. You can either browse the [OpenML website](https://openml.org/search?type=task&sort=runs) to find a task (and get it's ID), or follow the [example](./Examples/Create%20Dataset%20and%20Task.ipynb) to create a task from a custom dataset.

Then, follow one of the examples in the [Examples](./Examples) folder to see how to use this extension for your type of data.

Import openML libraries
```python
import torch.nn
import torch.optim

import openml_pytorch.config
import openml
import logging

from openml_pytorch.trainer import OpenMLTrainerModule
from openml_pytorch.trainer import OpenMLDataModule
from torchvision.transforms import Compose, Resize, ToPILImage, ToTensor, Lambda
import torchvision
from openml_pytorch.trainer import convert_to_rgb

```
Create a pytorch model and get a task from openML
```python
model = torchvision.models.efficientnet_b0(num_classes=200)
# Download the OpenML task for tiniest imagenet
task = openml.tasks.get_task(362128)
```
Download the task from openML and define Data and Trainer configuration
```python
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
data_module = OpenMLDataModule(
    type_of_data="image",
    file_dir="datasets",
    filename_col="image_path",
    target_mode="categorical",
    target_column="label",
    batch_size = 64,
    transform=transform
)
trainer = OpenMLTrainerModule(
    data_module=data_module,
    verbose = True,
    epoch_count = 1,
)
openml_pytorch.config.trainer = trainer
```
Run the model on the task
```python
run = openml.runs.run_model_on_task(model, task, avoid_duplicate_runs=False)
run.publish()
print('URL for run: %s/run/%d' % (openml.config.server, run.run_id))
```
Note: The input layer of the network should be compatible with OpenML data output shape. Please check [examples](/examples/) for more information.

Additionally, if you want to publish the run with onnx file, then you must call ```openml_pytorch.add_onnx_to_run()``` immediately before ```run.publish()```. 

```python
run = openml_pytorch.add_onnx_to_run(run)
```