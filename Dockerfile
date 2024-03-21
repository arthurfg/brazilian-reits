# We're using the latest version of Prefect with Python 3.10
FROM prefecthq/prefect:2-python3.10

# Add our requirements.txt file to the image and install dependencies
RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry lock 

RUN poetry install 
# Add our flow code to the image
COPY flows /opt/prefect/flows

# Run our flow script when the container starts
CMD ["python", "flows/prefect-docker-guide-flow.py"]