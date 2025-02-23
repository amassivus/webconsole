from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import paramiko
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

def ssh_connect(hostname, username, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode(), stderr.read().decode()

@socketio.on('execute_command')
def handle_execute_command(json):
    hostname = json['hostname']
    username = json['username']
    password = json['password']
    command = json['command']
    stdout, stderr = ssh_connect(hostname, username, password, command)
    emit('command_output', {'stdout': stdout, 'stderr': stderr})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
