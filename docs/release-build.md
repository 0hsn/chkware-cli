## Release build process

Follow the steps to do a manual release on PyPi.


- Please confirm that Python 3.10.x with [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) is installed and setup on this machine
- Clone the repo 
    ```
    $ git clone https://github.com/chkware/cli.git ./cli-release
    ```

- Change to the directory 
    ```bash
    $ cd ./cli-release
    ```

- Update version number on `setup.cfg`
    ```ini
    version = 0.X.X
    ```

- Update version number on `chk/console/main.py`
    ```python
    """v0.X.X | supported version strings: 0.7.2, ..."""
    ```

- Make directory for local _virtualenv_ setup
    ```bash
    $ mkdir ./.venv
    ```

- Install all required packages
    ```bash
    $ pipenv install
    ```

- Install all required packages for build and push to PyPI
    ```bash
    $ pipenv run pip install -U build twine
    ```

- Use the environment's python to build
    ```bash
    $ pipenv run python -m build --wheel --sdist
    ```

- Push the packages to PyPi. This setup will require your PyPi username and password. So, make sure to setup an account, and have permission to push setup ready on the `chk` package repository.
    ```bash
    $ pipenv run twine upload dist/*
    ```

- Write proper [_changelog_](CHANGELOG.md) for the release _0.X.X_

- Publish and push an annotated tag
    ```bash
    $ git tag -a v0.X.X -m "..."
    $ git push -u origin v0.X.X
    ```
- [tbd] build and zipapp, and release a version

And a new version is release!