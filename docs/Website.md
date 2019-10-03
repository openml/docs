## Installation
The OpenML website runs on [Flask](http://flask.pocoo.org/), [React](https://reactjs.org/), and [Dash](https://dash.plot.ly/). You need to install these first.

* If you haven't already, [install a recent version of NPM (6 or higher)](https://nodejs.org/en/download/).
* Install Flask and Dash
``` python
pip install flask
pip install dash
```

## Building and running

The source code for the OpenML website can be found on [GitHub](https://github.com/openml/openml.org)
Build the app by going to ``src/client/app` and running

``` python
npm run build
```

Start the server with:

``` python
python server.py
```

You should now see it running in your browser at `localhost:5000`

## Development

To start the React frontend in developer mode, go to ``src/client/app` and run:

``` python
npm run start
```

The app should automatically open at `localhost:3000` and any changes made to
the code will automatically reload the website.

## Structure
<img src="../img/structure.png" alt="OpenML Website structure" width="500"/>

The website is built on the following components:  

* A [Flask backend](../Flask). Written in Python, the backend takes care of all communication with the OpenML server. It builds on top of the OpenML Python API. It also takes care of user authentication and keeps the search engine (ElasticSearch) up to date with the latest information from the server.
* A [React frontend](../React). Written in JavaScript, this takes care of rendering the website. It pulls in information from the search engine, and shows plots rendered by Dash. It also contains forms (e.g. for logging in or uploading new datasets), which will be sent off to the backend for processing.
* [Dash dashboards](../Dash). Written in Python, Dash is used for writing interactive plots. It pulls in data from the Python API, and renders the plots as React components.
