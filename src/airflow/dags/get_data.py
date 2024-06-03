import datetime
from airflow.operators.bash import BashOperator
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from botocore.config import Config
import os


config = Config(read_timeout=900, connect_timeout=900, retries={"max_attempts": 1, "mode": "standard"})


default_args = {
    "owner": "Data Team",
    "start_date": datetime.datetime(2021, 1, 1),
    "retries": 0,
    "retry_delay": datetime.timedelta(minutes=5),
    "email_on_failure": True,
    "recipients": os.getenv("ALERTS_RECIPIENTS_LIST")
}



# This Airflow DAG is responsible for: 
#     1.Envoking AWS Lambda which fetches data from an API and drops it into a bucket
#     2. Triggering an AWS Glue job which tansforms the data according to the business rules specified and then drops it to another bucket
#     3. Triggering another AWS Lambda which fetches the data from that bucket and drops it into Redshift DB where it will recreate the table with the new data.

# In case of any errors during the process, an email will be sent to the recipient list configured 
# in the Airflow environment variables (ALERTS_RECIPIENTS_LIST)

# The DAG is scheduled to run every 20 minutes.


with DAG(
    dag_id="api_to_redshift",
    default_args=default_args,
    schedule="* 20 * * *",
    dagrun_timeout=60 * 59,
    catchup=False,
):

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    fetch_data_task = BashOperator(
        task_id="fetch_data_task",
        bash_command="curl 'http://api_to_s3_lambda:8080/2015-03-31/functions/function/invocations' -d '{}'"    
    )

    transformation_task = BashOperator(
        task_id="transformation_task",
        bash_command="python glue_job.py",
        cwd= "/opt/airflow/scripts"
    )

    load_data_task = BashOperator(
        task_id="load_data_task",
        bash_command="curl 'http://s3_to_redshift_lambda:8080/2015-03-31/functions/function/invocations' -d '{}'"    
    )

    start >> fetch_data_task >> transformation_task >> load_data_task >> end
