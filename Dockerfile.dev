FROM prefecthq/prefect:2-python3.10

COPY . /opt/prefect/prefect-cloud-run-poc

RUN pip install -r /opt/prefect/prefect-cloud-run-poc/flows/brazilian_reits/requirements.txt

CMD ["python3", "/opt/prefect/prefect-cloud-run-poc/flows/brazilian_reits/brazilian_reits.py"]
