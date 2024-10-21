When you submit datasets or experiments (runs) to OpenML, they will be processed by set of server-side processes, combined in the 'Evaluation Engine':

- It extracts the features in tabular datasets and their statistical types
- It computes a set of dataset characteristics (meta-features), e.g. the number of features and classes, that help with search and filtering, or to compute dataset similarity measures
- It evaluates experiments using a set of server-side evaluation metrics that are computed uniformly for all experiments so that they are comparable
- It creates consistent train-test splits based on task characteristics.

!!! tip "Phasing out"
    This documentation is about the older Java-based version of the OpenML evaluation engine, which will be phased out. These parts are being rewritten as a set of independent services in Python.

The application that implements the evaluation engine was originally implemented in Java because it bulds on the Weka API. It is invoked from the OpenML API by means of a CLI interface. Typically, a call looks like this:

`java -jar webapplication.jar -config "api_key=S3CR3T_AP1_K3Y" -f evaluate_run -r 500`

Which in this case executes the webapplication jar, invokes the function "evaluate run" and gives it parameter run id 500. The config parameter can be used to set some config items, in this case the api_key is mandatory. Every OpenML user has an api_key, which can be downloaded from their [OpenML profile page](http://www.openml.org/u). The response of this function is a call to the OpenML API uploading evaluation results to the OpenML database. Note that in this case the PHP website invokes the Java webapplication, which makes a call to the PHP website again, albeit another endpoint. 

The webapplication does not have direct writing rights into the database. All communication to the database goes by means of the [OpenML Connector](http://search.maven.org/#search|ga|1|g%3A%22org.openml%22), which communicates with the OpenML API. As a consequence, the webapplication could run on any system, i.e., there is no formal need for the webapplication to be on the same server as the website code. This is important, since this created modularity, and not all servers provide a command line interface to PHP scripts.

Another example is the following:

`java -jar webapplication -config "api_key=S3CR3T_AP1_K3Y" -f all_wrong -r 81,161 -t 59`

Which takes a comma separated list of run ids (no spaces) and a task id as input and outputs the test examples on the dataset on which all algorithms used in the runs produced wrong examples (in this case, weka.BayesNet_K2 and weka.SMO, respectively). An error will be displayed if there are runs not consistent with the task id in there. 

## Extending the Java App

The bootstrap class of the webapplication is

`org.openml.webapplication.Main`

It automatically checks authentication settings (such as api_key) and the determines which function to invoke. 

It uses a switch-like if - else contruction to facilitate the functionalities of the various functions. Additional functions can be added to this freely. From there on, it is easy to add functionality to the webapplication. 

Parameters are handled using the Apache Commons CommandLineParser class, which makes sure that the passed parameters are available to the program. 

In order to make new functionalities available to the website, there also needs to be programmed an interface to the function, somewhere in the website. The next section details on that. 

## Interfacing from the OpenML API
By design, the REST API is not allowed to communicate with the Java App. All interfaces with the Java webapplication should go through other controllers of the PHP CodeIgniter framework., for example api_splits. Currently, the website features two main API's. These are represented by a Controller. Controllers can be found in the folder openml_OS/controllers. Here we see:
* api_new.php, representing the REST API
* api_splits.php, representing an API interfacing to the Java webapplication. 

## Helper functions
The Java code is available in the 'OpenML' repository: https://github.com/openml/OpenML/tree/master/Java

### Components
Support for tasks:  

- *foldgeneration*: Java code for generating cross-validation folds. Can be used from command line.
- *splitgeneration*: Split generator for cross validation and holdout. Unsure what's the difference with the previous?
- *generate_predictions*: Helper class to build prediction files based on WEKA output. Move to WEKA repository?
- *evaluate_predictions*: The evaluation engine computing evaluation scores based on submitted predictions



