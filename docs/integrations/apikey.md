# Authentication

The OpenML server can only be accessed by users who have signed up on the
OpenML platform. If you don’t have an account yet, sign up now.
You will receive an API key, which will authenticate you to the server
and allow you to download and upload datasets, tasks, runs and flows.

* Create an OpenML account (free) on https://www.openml.org.
* After logging in, open your account page (avatar on the top right)
* Open 'Account Settings', then 'API authentication' to find your API key.

There are two ways to permanently authenticate:

* Use the ``openml`` CLI tool with ``openml configure apikey MYKEY``,
  replacing **MYKEY** with your API key.
* Create a plain text file **~/.openml/config** with the line
  **'apikey=MYKEY'**, replacing **MYKEY** with your API key. The config
  file must be in the directory ~/.openml/config and exist prior to
  importing the openml module.