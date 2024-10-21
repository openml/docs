# OpenML Server API Software Documentation

This is the Python-based OpenML REST API server.
It's a rewrite of our [old backend](http://github.com/openml/openml) built with a
modern Python-based stack.


!!! question "Looking to access data on OpenML?"

    If you simply want to access data stored on OpenML in a programmatic way,
    please have a look at connector packages in
    [Python](https://openml.github.io/openml-python/main/),
    [Java](https://github.com/openml/openml-java),
    or [R](http://openml.github.io/openml-r/).

    If you are looking to interface directly with the REST API, and are looking
    for documentation on the REST API endpoints, visit the
    [APIs](https://openml.org/apis) page.

    This documentation is for developing and hosting your own OpenML REST API.

## Development Roadmap

First we will mimic current server functionality, relying on many implementation details
present in the current production server. We will implement all endpoints using the SQL
text queries based on PHP implementation, which should give near-identical responses to
the current JSON endpoints. Minor exceptions are permitted but will be documented.

At the same time we may also provide a work-in-progress "new" endpoint, but there won't
be official support for it at this stage. After we verify the output of the endpoints
are identical (minus any intentional documented differences), we will officially release
the new API. The old API will remain available. After that, we can start working on a
new version of the JSON API which is more standardized, leverages typing, and so on:

 - Clean up the database: standardize value formats where possible (e.g., (un)quoting
   contributor names in the dataset's contributor field), and add database level
   constraints on new values.
 - Redesign what the new API responses should look like and implement them,
   API will be available to the public as it is developed.
 - Refactor code-base to use ORM (using `SQLAlchemy`, `SQLModel`, or similar).
 - Officially release the modernized API.

There is no planned sunset date for the old API. This will depend on the progress with
the new API as well as the usage numbers of the old API.
