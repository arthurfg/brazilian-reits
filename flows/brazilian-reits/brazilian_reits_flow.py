from prefect import flow, task, get_run_logger
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm
import os
import zipfile
import pyarrow as pa
import pyarrow.parquet as pq

@task
def extract_links_and_dates(url) -> pd.DataFrame:
    """
    Extracts all file names and their respective last update dates in a pandas dataframe.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontra todos os links dentro do HTML
    links = soup.find_all("a")
    links_zip = []

    for link in links:
        if link.has_attr("href") and link["href"].endswith(".zip"):
            links_zip.append(link["href"])
    # Encontra todas as datas de atualização dentro do HTML
    padrao = r"\d{2}-\w{3}-\d{4} \d{2}:\d{2}"
    datas = soup.find_all(string=lambda text: re.findall(padrao, text))
    datas_atualizacao = []
    for data in datas:
        data_atualizacao = re.findall(padrao, data)[0]
        datas_atualizacao.append(data_atualizacao)

    dados = {
        "arquivo": links_zip,
        "ultima_atualizacao": datas_atualizacao[0:],
        "data_hoje": datetime.now().strftime("%Y-%m-%d"),
    }

    df = pd.DataFrame(dados)
    df.ultima_atualizacao = df.ultima_atualizacao.apply(
        lambda x: datetime.strptime(x, "%d-%b-%Y %H:%M").strftime("%Y-%m-%d")
    )

    df["desatualizado"] = df["data_hoje"] == df["ultima_atualizacao"]
    return df

@task
def check_for_updates(df):
    """
    Checks for outdated tables.
    """
    logger = get_run_logger()
    logger.info(df.head())
    
    return df.query("desatualizado == False").arquivo.to_list()       

@task  # noqa
def download_unzip_csv(
    files,url: str = "https://dados.cvm.gov.br/dados/FII/DOC/INF_MENSAL/DADOS/", chunk_size: int = 128, mkdir: bool = True, id="raw",
) -> str:
    """
    Downloads and unzips a .csv file from a given list of files and saves it to a local directory.
    Parameters:
    -----------
    url: str
        The base URL from which to download the files.
    files: list or str
        The .zip file names or a single .zip file name to download the csv file from.
    chunk_size: int, optional
        The size of each chunk to download in bytes. Default is 128 bytes.
    mkdir: bool, optional
        Whether to create a new directory for the downloaded file. Default is False.
    Returns:
    --------
    str
        The path to the directory where the downloaded file was saved.
    """
    logger = get_run_logger()
    if mkdir:
        os.makedirs(f"/tmp/data/br_cvm_fii/{id}/input/", exist_ok=True)

    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    if isinstance(files, list):
        for file in files:
            logger.info(f"Baixando o arquivo {file}")
            download_url = f"{url}{file}"
            save_path = f"/tmp/data/br_cvm_fii/{id}/input/{file}"

            r = requests.get(
                download_url, headers=request_headers, stream=True, timeout=50
            )
            with open(save_path, "wb") as fd:
                for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
                    fd.write(chunk)

            try:
                with zipfile.ZipFile(save_path) as z:
                    z.extractall(f"/tmp/data/br_cvm_fii/{id}/input")
                logger.info("Dados extraídos com sucesso!")

            except zipfile.BadZipFile:
                logger.info(f"O arquivo {file} não é um arquivo ZIP válido.")

            os.system(
                f'cd /tmp/data/br_cvm_fii/{id}/input; find . -type f ! -iname "*.csv" -delete'
            )

    elif isinstance(files, str):
        logger.info(f"Baixando o arquivo {files}")
        download_url = f"{url}{files}"
        save_path = f"/tmp/data/br_cvm_fii/{id}/input/{files}"

        r = requests.get(download_url, headers=request_headers, stream=True, timeout=10)
        with open(save_path, "wb") as fd:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
                fd.write(chunk)

        try:
            with zipfile.ZipFile(save_path) as z:
                z.extractall(f"/tmp/data/br_cvm_fi/{id}/input")
            logger.info("Dados extraídos com sucesso!")

        except zipfile.BadZipFile:
            logger.info(f"O arquivo {files} não é um arquivo ZIP válido.")

        os.system(
            f'cd /tmp/data/br_cvm_fii/{id}/input; find . -type f ! -iname "*.csv" -delete'
        )

    else:
        raise ValueError("O argumento 'files' possui um tipo inadequado.")

    return f"/tmp/data/br_cvm_fii/{id}/input/"

@task
def make_partitions(path: str):
    logger = get_run_logger()
    files = os.listdir(path)
    for i in ['geral', 'complemento', 'ativo_passivo']: os.makedirs(f"/tmp/data/br_cvm_fii/{i}", exist_ok=True) 
    ROOT_DIR = "/tmp/data/br_cvm_fii/"
    for file in files:
        df = pd.read_csv(f'{ROOT_DIR}/raw/input/{file}', sep=";", encoding="ISO-8859-1")
        partition_name = None
        if "_geral_" in file:
            partition_name = "geral"
        elif "_complemento_" in file:
            partition_name = "complemento"
        elif "ativo_passivo" in file:
            partition_name = "ativo_passivo"
        logger.info(f"Fazendo partições para o arquivo {file}")
        if partition_name:
            pq.write_to_dataset(
                table=pa.Table.from_pandas(df),
                root_path=f'{ROOT_DIR}{partition_name}',
                partition_cols=["Data_Referencia"]
            )          





@flow()
def test():
    links_and_dates = extract_links_and_dates(url= "https://dados.cvm.gov.br/dados/FII/DOC/INF_MENSAL/DADOS/")
    files = check_for_updates(df = links_and_dates)
    path = download_unzip_csv(files = files)
    make_partitions(path = path)
if __name__ == "__main__":
    test()