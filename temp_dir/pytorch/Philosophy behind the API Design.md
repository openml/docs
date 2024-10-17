# Philosophy behind the API design
This API is designed to make it easier to use PyTorch with OpenML and has been heavily inspired by the current state of the art Deep Learning frameworks like FastAI and PyTorch Lightning. 

To make the library as modular as possible, callbacks are used throughout the training loop. This allows for easy customization of the training loop without having to modify the core code.

## Separation of Concerns
Here, we focus on the data, model and training as separate blocks that can be strung together in a pipeline. This makes it easier to experiment with different models, data and training strategies.

That being the case, the OpenMLDataModule and OpenMLTrainerModule are designed to handle the data and training respectively. This might seem a bit verbose at first, but it makes it easier to understand what is happening at each step of the process and allows for easier customization.
