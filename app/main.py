from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS
from flask import redirect, url_for, jsonify
from bson import ObjectId
import pika, os, json, datetime
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
resources = {r"/*": {"origins": "*"}}
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False

try:
    client = MongoClient('mongodb')
    db = client['test']
    print("MongoClient Connected to DB: ", db.name)
except Exception as e:
    print("MongoClient Exception :", e)

# # Iterate loop to read and print all environment variables
# print("The keys and values of all environment variables:")
# for key in os.environ:
#     print(key, '=>', os.environ[key])

@app.route('/')
@app.route('/index')
def index():
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)

@app.route('/dashboard/<name>')
def dashboard(name):
    list_users = []
    col = db["user"]
    for user in col.find({}):
        list_users.append({
            "id": str(user['_id']),
            "name": str(user['name']),
            "created": user['date_created'].strftime("%Y-%m-%d")
            })
    return render_template('dashboard.html', username=name, list_users=list_users)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      add(user)
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('login.html')
  
def get_rabbitmq_connection():
    connection = None   
    try:
            
        print(' Connecting to rabbitmq server ...')

        RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
        RABBITMQ_USER = os.environ['RABBITMQ_USER']
        RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
        RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
        
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_HOST,
                                            RABBITMQ_PORT,
                                            '/',
                                            credentials)
        connection = pika.BlockingConnection(parameters)
        
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
    return connection

def add(cmd):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
   
    connection.close()
    return " ___ Sent: %s" % cmd

if __name__ == '__main__':
   app.run(debug = True,  host = '0.0.0.0', port = 5000)
   