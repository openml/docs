---
title: Getting Started
description: A short tutorial on installing the software and running a simple benchmark.
---

# Getting Started

The [AutoML Benchmark](https://openml.github.io/automlbenchmark/index.html) is a tool for benchmarking AutoML frameworks on tabular data.
It automates the installation of AutoML frameworks, passing it data, and evaluating
their predictions. 
[Our paper](https://arxiv.org/pdf/2207.12560.pdf) describes the design and showcases 
results from an evaluation using the benchmark. 
This guide goes over the minimum steps needed to evaluate an
AutoML framework on a toy dataset.

Full instructions can be found in the [API Documentation.](https://openml.github.io/automlbenchmark/docs/)

## Installation
These instructions assume that [Python 3.9 (or higher)](https://www.python.org/downloads/) 
and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) are installed,
and are available under the alias `python` and `git`, respectively. We recommend
[Pyenv](https://github.com/pyenv/pyenv) for managing multiple Python installations,
if applicable. We support Ubuntu 22.04, but many linux and MacOS versions likely work
(for MacOS, it may be necessary to have [`brew`](https://brew.sh) installed).

First, clone the repository:

```bash
git clone https://github.com/openml/automlbenchmark.git --branch stable --depth 1
cd automlbenchmark
```

Create a virtual environments to install the dependencies in:

### Linux

```bash
python -m venv venv
source venv/bin/activate
```

### MacOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv ./venv
venv/Scripts/activate
```

Then install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```


??? windows "Note for Windows users"

    The automated installation of AutoML frameworks is done using shell script,
    which doesn't work on Windows. We recommend you use
    [Docker](https://docs.docker.com/desktop/install/windows-install/) to run the
    examples below. First, install and run `docker`. 
    Then, whenever there is a `python runbenchmark.py ...` 
    command in the tutorial, add `-m docker` to it (`python runbenchmark.py ... -m docker`).

??? question "Problem with the installation?"

    On some platforms, we need to ensure that requirements are installed sequentially.
    Use `xargs -L 1 python -m pip install < requirements.txt` to do so. If problems 
    persist, [open an issue](https://github.com/openml/automlbenchmark/issues/new) with
    the error and information about your environment (OS, Python version, pip version).


## Running the Benchmark

To run a benchmark call the `runbenchmark.py` script specifying the framework to evaluate.

See the [API Documentation.](https://openml.github.io/automlbenchmark/docs/) for more information on the parameters available.

