FROM prefecthq/prefect:2-python3.10

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry lock 

RUN poetry install 
# Add our flow code to the image
COPY . /opt/prefect/prefect-cloud-run-poc
