from logging import debug
from flask import Flask, request
import os
import psycopg2
import uuid
import json
from flask_cors import CORS

app = Flask(__name__)
# https://stackoverflow.com/a/64657739
CORS(app, support_credentials=True)
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# https://stackoverflow.com/a/43634941
conn.autocommit = True

cursor = conn.cursor()
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task (
        task_id varchar(64) PRIMARY KEY,
        service_id varchar(64),
        task_date_time varchar(256),
        task_consumer varchar(256),
        task_provider varchar(256),
        task_status varchar(256),
        task_price varchar(256)
    );
    ''')
except psycopg2.Error:
    print('Error occurred while creating table')

@app.route('/health-check')
def health_check():
    return {'status': 200}

@app.route('/create-task', methods=['POST'])
def create_task():
    # https://stackoverflow.com/a/67461897
    data = request.get_json()
    task_id = str(uuid.uuid4())
    service_id = data['service_id']
    task_date_time = data['task_date_time']
    task_consumer = data['task_consumer']
    task_provider = data['task_provider']
    task_status = data['task_status']
    task_price = data['task_price']
    query = '''
        INSERT INTO task (task_id, service_id, task_date_time, task_consumer, task_provider, task_status, task_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, [task_id, service_id, task_date_time, task_consumer, task_provider, task_status, task_price])
    conn.commit()
    return {'status': 201, 'task_id': task_id}

@app.route('/get-all-task/<user_id>')
def get_all_task(user_id):
    query = '''
        SELECT task_id, service_id, task_date_time, task_consumer, task_provider, task_status, task_price FROM task WHERE task.task_consumer=%s OR task.task_provider=%s
    '''
    cursor.execute(query, [str(user_id), str(user_id)])
    res = cursor.fetchall()
    if (len(res) == 0):
        return {'status': 200, 'task': None}
    task_list = list()
    task = dict()
    for i in range(len(res)):
        task = {
            'task_id': res[i][0],
            'service_id': res[i][1],
            'task_date_time': res[i][2],
            'task_consumer': res[i][3],
            'task_provider': res[i][4],
            'task_status': res[i][5],
            'task_price': res[i][6]
        }
        task_list.append(task)
    return {'status': 200, 'task': task_list}

@app.route('/delete-task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    query = '''
        DELETE FROM task WHERE task.task_id=%s
    '''
    cursor.execute(query, [str(task_id)])
    conn.commit()
    return {'status': 200}

@app.route('/change-task-status/<task_id>/<task_status>', methods=['POST'])
def change_task_status(task_id, task_status):
    query = '''
        UPDATE task SET task_status=%s WHERE task.task_id=%s
    '''
    cursor.execute(query, [str(task_status), str(task_id)])
    conn.commit()
    return {'status': 200}

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)