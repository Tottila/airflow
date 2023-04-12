from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator

# Создаем DAG(контейнер) в который поместим наши задачи
# Для DAG-а характерны следующие атрибуты
# - Интервал запусков
# - Начальная точка запуска
with DAG(dag_id='dag',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily', # Интервал запусков
         start_date=days_ago(1) # Начальная точка запуска
    ) as dag:

 
    # Создадим задачу которая будет запускать питон функция
    # Все именно так, создаем код для запуска другого кода
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/dm-novikov/stepik_airflow_course/main/data/data.csv',
            'tmp_file': '/tmp/file.csv'}
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv',
            'group': ['A', 'B', 'C'],
            'agreg': {"D": sum}}
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={
            'tmp_file': '/tmp/file_agg.csv',
            'table_name': 'table'
        }
    )

    # Создадим задачу которая будет отправлять файл на почту
    email_op = EmailOperator(
        task_id='send_email',
        to="flow5tep@yandex.ru",
        subject="Test Email Please Ignore",
        html_content=None,
        files=['/tmp/file_agg.csv']
    )

    # Создадим порядок выполнения задач
    # В данном случае 2 задачи буудт последователньы и ещё 2 парараллельны
    extract_data >> transform_data >> [load_data, email_op]
