from airflow import DAG
from airflow.operators.python import PythonOperator 
import deploy_fromFixtures
from datetime import datetime

dag = DAG(dag_id='deploy_fromFixtures',
          schedule_interval="0 9 * * *",
          start_date=datetime(2023, 5, 18, 15, 50)
          )

deploy_fromFixtures = PythonOperator(python_callable=deploy_fromFixtures.main,
                                     dag=dag,
                                     task_id='deploy_fromFixtures')

#
deploy_fromFixtures