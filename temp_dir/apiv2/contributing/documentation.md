# Documentation with mkdocs-material

Our documentation is built using [mkdocs](https://www.mkdocs.org) and the
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme. We also use some
[plugins](https://squidfunk.github.io/mkdocs-material/plugins/).
Please refer to the ["Getting Started"](https://squidfunk.github.io/mkdocs-material/getting-started/)
pages of `mkdocs-material` for a general overview on how to work with `mkdocs-material`.
All documentation files are in the `docs/` folder, except for the configuration file
which is `mkdocs.yml` at the root of the repository.

For minor changes, it should be fine to edit the page directly on Github.
That should commit to a separate branch (or fork), and you can set up a pull request.
For larger changes, clone a fork of the repository as described in the
["Local Installation"](../installation.md#local-installation) section.


=== "Docker"

    After cloning the repository, you may also build and serve the documentation through Docker:

    ```
    docker compose up docs
    ```


=== "Local installation"

    Instead of installing all dependencies (with `python -m pip install -e ".[docs]"`),
    you may also install just the documentation dependencies:

    ```bash
    python -m pip install mkdocs-material mkdocs-section-index
    ```

    You can then build and serve the documentation with

    ```bash
    python -m mkdocs serve
    ```

This will serve the documentation from the `docs/` directory to [http://localhost:8000/](http://localhost:8000/).
Any updates you make to files in that directory will be reflected on the website.
When you are happy with your changes, just commit and set up a pull request!
