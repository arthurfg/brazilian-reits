from prefect_dbt.cli.commands import DbtCoreOperation
from prefect import flow

@flow
def trigger_dbt_flow() -> str:
    result = DbtCoreOperation(
        commands=["dbt run"],
        project_dir="/opt/prefect/prefect-cloud-run-poc/queries",
        profiles_dir="/opt/prefect/prefect-cloud-run-poc/queries"
    ).run()
    return result

if __name__ == "__main__":
    trigger_dbt_flow()