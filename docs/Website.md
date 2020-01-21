## Installation
The OpenML website runs on [Flask](http://flask.pocoo.org/), [React](https://reactjs.org/), and [Dash](https://dash.plot.ly/). You need to install these first.

* Download or clone the source code for the OpenML website from [GitHub](https://github.com/openml/openml.org).
Then, go into that folder (it should have the `requirements.txt` and `package.json` files).

* Install Flask, Dash, and dependencies using [PIP](https://pip.pypa.io/en/stable/installing/)
``` python
pip install -r requirements.txt
```

* Install React and dependencies using [NPM (6 or higher)](https://nodejs.org/en/download/).
``` python
npm install
```

## Building and running

Do a production build of the frontend by going to `server/src/client/app` and running

``` python
npm run build
```

Start the server by going back to the home directory and running:

``` python
flask run
```

You should now see the app running in your browser at `localhost:5000`

Note: If you run the app using HTTPS, add the SSL context or use 'adhoc' to use on-the-fly certificates

``` python
flask run --cert='adhoc'
```


## Development

To start the React frontend in developer mode, follow the installation steps above, go to `server/src/client/app` and run:

``` python
npm run start
```

The app should automatically open at `localhost:3000` and any changes made to
the code will automatically reload the website (hot loading).

## Structure
<img src="../img/structure.png" alt="OpenML Website structure" width="500"/>

The website is built on the following components:  

* A [Flask backend](../Flask). Written in Python, the backend takes care of all communication with the OpenML server. It builds on top of the OpenML Python API. It also takes care of user authentication and keeps the search engine (ElasticSearch) up to date with the latest information from the server. Files are located in the `server` folder.
* A [React frontend](../React). Written in JavaScript, this takes care of rendering the website. It pulls in information from the search engine, and shows plots rendered by Dash. It also contains forms (e.g. for logging in or uploading new datasets), which will be sent off to the backend for processing. Files are located in `server/src/client/app`.
* [Dash dashboards](../Dash). Written in Python, Dash is used for writing interactive plots. It pulls in data from the Python API, and renders the plots as React components. Files are located in `server/src/dashboard`.
