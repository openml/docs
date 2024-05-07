# Runs

## Automated reproducible evaluations
Runs are experiments (benchmarks) evaluating a specific flows on a specific task. As shown above, they are typically submitted automatically by machine learning
libraries through the OpenML [APIs](https://www.openml.org/apis)), including lots of automatically extracted meta-data, to create reproducible experiments. With a few for-loops you can easily run (and share) millions of experiments.

## Online organization
OpenML organizes all runs online, linked to the underlying data, flows, parameter settings, people, and other details. See the many examples above, where every dot in the scatterplots is a single OpenML run.

## Independent (server-side) evaluation
OpenML runs include all information needed to independently evaluate models. For most tasks, this includes all predictions, for all train-test splits, for all instances in the dataset, including all class confidences. When a run is uploaded, OpenML automatically evaluates every run using a wide array of evaluation metrics. This makes them directly comparable with all other runs shared on OpenML. For completeness, OpenML will also upload locally computed evaluation metrics and runtimes. 

New metrics can also be added to OpenML's evaluation engine, and computed for all runs afterwards. Or, you can download OpenML runs and analyse the results any way you like.

!!! note
    Please note that while OpenML tries to maximise reproducibility, exactly reproducing all results may not always be possible because of changes in numeric libraries,  operating systems, and hardware.