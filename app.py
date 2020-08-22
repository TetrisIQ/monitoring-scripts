from flask import Flask, jsonify
from flask import request
import subprocess
import urllib.request
import socket
import psutil
import shutil

app = Flask(__name__)

apiKey = 'e2387605-c0b7-4a6d-9f7b-0a3bdae1d49b'

def checkCredentials(key):
    return apiKey.__eq__(key)


@app.route('/ping')  # Ping
def ping():
    args = request.args
    if checkCredentials(args["key"]):
        return 'Pong!'
    else:
        return ""


@app.route('/service/<service>')
def service(service):
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    if service != None:
        # request ist valid
        res = ""
        try:
            res = subprocess.check_output(['systemctl', 'status', service])
        except subprocess.CalledProcessError as exc:
            res = exc.output
        if (str(res).find("active (running)") != -1):
            return "running"
        elif (str(res).find("inactive (dead)") != -1):
            return "not running"
    return "service not found"


@app.route('/ip/')
def public_ip():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    public_ip = urllib.request.urlopen("https://ipinfo.io/ip").read().decode("utf-8")
    public_ip = str(public_ip).replace("\n", "")

    if not (str(public_ip).find("Could not resolve host")):
        public_ip = "No network connection!"
    private_ip = socket.gethostbyname(socket.gethostname())
    return {
        "private": private_ip,
        "public": public_ip
    }


@app.route('/cpu/')
def current_cpu():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    return str(psutil.cpu_percent())


@app.route('/ram/')
def current_ram():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    return str(psutil.virtual_memory().percent)


@app.route('/hostname/')
def hostname():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    try:
        return subprocess.check_output(['hostname'])
    except subprocess.CalledProcessError as exc:
        return exc.output


@app.route('/memory/')
def disk_memory():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    total, used, free = shutil.disk_usage("/")
    return {
        "TotalGiB:": (total // (2 ** 30)),
        "UsedGiB": (used // (2 ** 30)),
        "FreeGiB": (free // (2 ** 30))
    }

@app.route('/uptime/')
def uptime():
    key = request.args['key']
    if not checkCredentials(key):
        return "Check your API key"
    try:
        uptime = subprocess.check_output(['uptime', '-p'])
    except subprocess.CalledProcessError as exc:
        uptime = exc.output

    return {
        "hours" : str(uptime).split(",")[0][5:-6],
        "minutes" : str(uptime).split(",")[1][1:-11]
    }

if __name__ == '__main__':
    app.run()
    try:
        res = subprocess.check_output(['systemctl', 'status', 'plexmediaserver.service'])
        print(res)
    except subprocess.CalledProcessError as exc:
        result = exc.output
        print(result)
