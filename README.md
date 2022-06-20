# Data Science Jupyter Lab

Mount a Docker container with essential python packages ready for data science and data visualization.

- All packages in [@jupyter/scipy-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook): *numpy, pandas, scipy, matplotlib, sqlalchemy, ...*
- Geospatial packages: *geopandas, shapely, geopy, geoplot*
- Data viz: *ipyleaflet, plotly*

## Install

```bash
git clone https://github.com/snowplanner/jupyterlab-data-science.git
```

In case you need another package that is not included in the container, just add it to the `requirements.txt` file and launch the following command on terminal to rebuild the image.

```bash
docker compose build
```

## Usage

After launching Docker, run the following command in terminal from the project directory root.

```bash
# Use -d flag for detached mode
docker compose up -d

# Access inside shell with
docker compose exec jupyter-lab sh

# Shutdown the container
docker compose down
```

Jupyter Lab is accessible on your browser at `http://localhost:8888`.

Alternatively, you can [connect to the Docker container with VS Code](https://code.visualstudio.com/docs/remote/containers). Despite this method adds some performance overhead, you'll be able to use the toolbox of your choice (linters, formatters, tests, etc.).

## Contribute

> :warning: **KEEP THIS REPO TIDY**.  
> Use folders and subfolders to structure your notebooks and modules. Use appropriate semantic names following python [naming conventions](https://peps.python.org/pep-0008/#prescriptive-naming-conventions).

There is some basic sample code in the folder `examples` to help you get started.

Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) whenever possible; that means, always.

Always use a **feature branch** to develop your code and avoid future merge conflicts. If you'd like to integrate your code to the basecode, issue a new **pull request** to the `main` branch.

A **code review** process is a must to ensure standard compliant code.

:no_entry_sign: **Never ever EVER commit sensitive data or secrets**.  
Use *environment variables* to store tokens, passwords and other information that must be kept safe. The Docker container automatically embeds all environment variables from a `.env` file (not trackable with git) in the root of the repo. Access variables as follows:

```python
import os

# Considering .env file to contain the API_KEY variable
# API_KEY=pk.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
api_key = os.environ['API_KEY']
```
