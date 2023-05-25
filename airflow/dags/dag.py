from airflow import DAG
from airflow.operators.python import PythonOperator 
import sys
import os
# directory reach
directory = os.path.abspath('__file__')
directory = os.path.dirname(directory)
directory = os.path.dirname(directory)
directory = os.path.dirname(directory)
# setting path
sys.path.append(directory) 
# importing
print(sys.path)

from deploy_fromFixtures import main
from datetime import datetime


dag = DAG(dag_id='deploy_fromFixtures',
          schedule_interval="0 4 * * *",
          start_date=datetime(2023, 5, 18, 15, 50)
          )

deploy_fromFixtures = PythonOperator(python_callable=main,
                                     dag=dag,
                                     task_id='deploy_fromFixtures')

#
deploy_fromFixtures


