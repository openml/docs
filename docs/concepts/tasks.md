# Tasks
Tasks describe what to do with the data. OpenML covers several <a
href="https://www.openml.org/search?type=task_type" target="_blank">task types</a>, such as classification and clustering. Tasks are containers including the data and other information such as train/test splits, and define what needs to be returned. They are machine-readable so that you can automate machine learning experiments, and easily compare algorithms evaluations (using the exact same train-test splits) against all other benchmarks shared by others on OpenML.

## Collaborative benchmarks

Tasks are <i>real-time, collaborative</i> benchmarks (e.g. see
<a href="https://www.openml.org/t/146825" target="_blank">MNIST</a> below). In the Analysis tab, you can view timelines and leaderboards, and learn from all prior submissions to design even better algorithms.

<!-- <img src="img/task_leaderboard.png" style="width:100%; max-width:1000px;"/> -->
![](../img/task_leaderboard.png)

## Discover the best algorithms
All algorithms evaluated on the same task (with the same train-test splits) can be directly compared to each other, so you can easily look up which algorithms perform best overall, and download their exact configurations. Likewise, you can look up the best algorithms for _similar_ tasks to know what to try first.

<!-- <img src="img/task_top_flows.png" style="width:100%; max-width:1000px;"/> -->
![](../img/task_top_flows.png)

## Automating benchmarks
You can <a href="https://www.openml.org/search?type=task" target="_blank">search</a> and download existing tasks, evaluate your algorithms, and automatically share the results (which are stored in a _run_). Here's what this looks like in the Python API. You can do the same across hundreds of tasks at once.

``` python
    from sklearn import ensemble
    from openml import tasks, runs

    # Build any model you like
    clf = ensemble.RandomForestClassifier()

    # Download any OpenML task (includes the datasets)
    task = tasks.get_task(3954)

    # Automatically evaluate your model on the task
    run = runs.run_model_on_task(clf, task)

    # Share the results on OpenML.
    run.publish()
```

You can create new tasks <a href="https://www.openml.org/auth/upload-task" target="_blank">via the website</a> or [via the APIs](https://www.openml.org/apis) as well.