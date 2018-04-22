# moldmates
Moldmate finder

## Setup

This setup assumes you have [conda installed](https://conda.io/docs/user-guide/install/index.html).

First, clone this git repository and navigate to the directory:

```bash
git clone https://github.com/dconathan/moldmates.git
cd moldmates
```

Run the `./setup_env.sh` script to create (and activate) the conda environment (named `moldmates`), and install all the requirements.

In the future, if the environment is already created, you just need to `source activate.sh` to activate the environment.

## Run the notebook

With the environment activated, run `jupyter notebook` and open the `notebooks/moldmates_demo.ipynb` notebook to see moldmates in action.


## Run tests

There are some tests in `tests/`.  You can run them by (after activating the environment) running `pytest`.

