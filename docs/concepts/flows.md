# Flows

Flows are machine learning pipelines, models, or scripts. They are typically uploaded directly from machine learning libraries (e.g. scikit-learn, pyTorch, TensorFlow, MLR, WEKA,...) via the corresponding [APIs](https://www.openml.org/apis). Associated code (e.g., on GitHub) can be referenced by URL.

## Analysing algorithm performance

Every flow gets a dedicated page with all known information. The Analysis tab shows an automated interactive analysis of all collected results. For instance, below are the results of a <a href="https://www.openml.org/f/17691" target="_blank">scikit-learn pipeline</a> including missing value imputation, feature encoding, and a RandomForest model. It shows the results across multiple tasks, and how the AUC score is affected by certain hyperparameters.

<!-- <img src="img/flow_top.png" style="width:100%; max-width:800px;"/> -->
![](../img/flow_top.png)

This helps to better understand specific models, as well as their strengths and weaknesses.

## Automated sharing

When you evaluate algorithms and share the results, OpenML will automatically extract all the details of the algorithm (dependencies, structure, and all hyperparameters), and upload them in the background.

``` python
    from sklearn import ensemble
    from openml import tasks, runs

    # Build any model you like.
    clf = ensemble.RandomForestClassifier()

    # Evaluate the model on a task
    run = runs.run_model_on_task(clf, task)

    # Share the results, including the flow and all its details.
    run.publish()
```

## Reproducing algorithms and experiments

Given an OpenML run, the exact same algorithm or model, with exactly the same hyperparameters, can be reconstructed within the same machine learning library to easily reproduce earlier results. 

``` python
    from openml import runs

    # Rebuild the (scikit-learn) pipeline from run 9864498
    model = openml.runs.initialize_model_from_run(9864498)
```

!!! note
    You may need the exact same library version to reconstruct flows. The API will always state the required version. We aim to add support for VMs so that flows can be easily (re)run in any environment <i class="fa fa-heart fa-fw fa-lg" style="color:red"></i>