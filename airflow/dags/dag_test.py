from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime
import logging

def test():
    logging.getLogger("airflow.task")    
    logging.info('test')

dag = DAG(dag_id='test',
          schedule_interval="*/1 * * * *",
          start_date=datetime(2023, 5, 18, 15, 50)
          )


test = PythonOperator(python_callable=test,
                                     dag=dag,
                                     task_id='test')


test