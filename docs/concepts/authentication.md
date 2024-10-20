# Authentication
OpenML is as open as possible. You can download and inspect all datasets, tasks, flows and runs through the website or the API without creating an account.

However, if you want to upload datasets or experiments, you need to <a href="https://www.openml.org/auth/sign-up" target="_blank">create an account</a>, sign in, and find your API key on your profile page. This key can then be used with any of the [OpenML APIs](https://www.openml.org/apis).

## API keys
If you don’t have an account yet, sign up now.
You will receive an API key, which will authenticate you to the server
and allow you to download and upload datasets, tasks, runs and flows.

* Create an OpenML account (free) on https://www.openml.org.
* After logging in, open your profile page. Click on the avatar on the top right, and choose 'Your Profile'.
* Click on 'API key' to find your API key. You can also reset it if needed.

To store your API key locally (to permanently authenticate), create a plain text file **~/.openml/config** with the line
**'apikey=MYKEY'**, replacing **MYKEY** with your API key. The config
file must be in the directory ~/.openml/config and exist prior to
importing the openml module.