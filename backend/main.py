import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
from kubernetes import client, config, watch
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Security check helpers
def check_pod_security(pod):
    alerts = []
    for c in pod.spec.containers:
        sc = c.security_context
        if not sc:
            alerts.append(f"Pod {pod.metadata.name}: Container {c.name} missing securityContext.")
            continue
        if getattr(sc, 'privileged', False):
            alerts.append(f"Pod {pod.metadata.name}: Container {c.name} is privileged!")
        if not getattr(sc, 'run_as_non_root', True):
            alerts.append(f"Pod {pod.metadata.name}: Container {c.name} may run as root!")
        if not getattr(sc, 'seccomp_profile', None):
            alerts.append(f"Pod {pod.metadata.name}: Container {c.name} missing seccompProfile.")
        if getattr(sc, 'capabilities', None):
            add_caps = getattr(sc.capabilities, 'add', [])
            if add_caps:
                alerts.append(f"Pod {pod.metadata.name}: Container {c.name} adds capabilities: {add_caps}")
    return alerts

def k8s_monitor():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event['object']
        alerts = check_pod_security(pod)
        if alerts:
            socketio.emit('security_alert', {'alerts': alerts})

@app.route('/')
def index():
    return "K8s Pod Security Monitor Backend Running. Open frontend/index.html for dashboard."

def start_k8s_thread():
    t = Thread(target=k8s_monitor, daemon=True)
    t.start()

if __name__ == '__main__':
    start_k8s_thread()
    socketio.run(app, host='0.0.0.0', port=5000)
