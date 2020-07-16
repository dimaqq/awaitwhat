### Build for Alpine

```sh
cd /src
apk update
apk add build-base openssl-dev libffi-dev curl
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
cp -a ~/.poetry/lib/poetry/_vendor/py3.8 ~/.poetry/lib/poetry/_vendor/py3.9
source $HOME/.poetry/env
poetry install
poetry run pytest
env _PYTHON_HOST_PLATFORM=alpine_x86_64 poetry build
```

#### Fix Poetry for Python 3.9

`cp -a ~/.poetry/lib/poetry/_vendor/py3.8 ~/.poetry/lib/poetry/_vendor/py3.9` is included above

### Manylinux2014

🚧 Work in progress, doesn't tag the wheels correctly 🚧

`docker run -v (pwd):/src -it quay.io/pypa/manylinux2014_x86_64 sh`

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | /opt/python/cp38-cp38/bin/python
source $HOME/.poetry/env
cd /src
poetry env use /opt/python/cp38-cp38/bin/python
poetry install
poetry run pytest
poetry build
poetry env use /opt/python/cp39-cp39/bin/python
poetry install
poetry run pytest
poetry build
```
