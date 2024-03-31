# Separate Music

This is an API wrapper around the [demucs library](https://github.com/facebookresearch/demucs?tab=readme-ov-file#demucs-music-source-separation) for music source separation.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project requires Python 3.9 (strictly) and pipenv. To install pipenv, go to [pipenv](https://pipenv.pypa.io/en/latest/installation.html).
The reason Python 3.9 is fixed is because the project uses [pytorch](https://pytorch.org/) which is not yet available for Python 3.10.

This project also requires [redis](https://redis.io/) to be installed and running on the default port (6379).

### Environment variables

The project requires the following environment variables to be set:
```bash
REDIS_URL= # defaults to redis://localhost:6379
```


### Starting the project

First, clone the repository:
```bash
git clone https://github.com/andreifilip123/separate-python.git
cd separate-python
```

Then, install the dependencies:
```bash
pipenv install
```

Now, you can run the project:
```bash
pipenv run uvicorn src.main:app --reload
```

To start the queue worker, run:
```bash
pipenv run rq worker
```