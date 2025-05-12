import psutil
import platform
import time
from datetime import datetime
from collections import deque
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Store historical data (in-memory, consider Redis for production)
history = {
    'cpu': deque(maxlen=60),
    'memory': deque(maxlen=60),
    'disk': deque(maxlen=60),
    'network': deque(maxlen=60),
    'timestamps': deque(maxlen=60)
}

def get_system_info():
    return {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'user': proc.info['username'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(processes, key=lambda p: p['cpu'], reverse=True)[:10]  # Top 10 by CPU

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def get_metrics():
    # Get current metrics
    cpu_metric = psutil.cpu_percent()
    mem_metric = psutil.virtual_memory().percent
    swap_metric = psutil.swap_memory().percent
    
    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    try:
        disk_metric = psutil.disk_usage(disk_path).percent
    except Exception as e:
        disk_metric = None

    net_io = psutil.net_io_counters()
    net_sent = round(net_io.bytes_sent / (1024 * 1024), 2)
    net_recv = round(net_io.bytes_recv / (1024 * 1024), 2)
    
    process_count = len(psutil.pids())
    
    # Update history
    timestamp = datetime.now().strftime("%H:%M:%S")
    history['cpu'].append(cpu_metric)
    history['memory'].append(mem_metric)
    history['disk'].append(disk_metric)
    history['network'].append(net_sent + net_recv)
    history['timestamps'].append(timestamp)
    
    # Check for alerts
    alerts = []
    if cpu_metric > 90:
        alerts.append({"type": "danger", "message": f"High CPU usage: {cpu_metric}%"})
    elif cpu_metric > 70:
        alerts.append({"type": "warning", "message": f"Moderate CPU usage: {cpu_metric}%"})
    
    if mem_metric > 90:
        alerts.append({"type": "danger", "message": f"High Memory usage: {mem_metric}%"})
    elif mem_metric > 70:
        alerts.append({"type": "warning", "message": f"Moderate Memory usage: {mem_metric}%"})

    data = {
        "cpu_metric": cpu_metric,
        "mem_metric": mem_metric,
        "swap_metric": swap_metric,
        "disk_metric": disk_metric,
        "net_sent": net_sent,
        "net_recv": net_recv,
        "process_count": process_count,
        "system_info": get_system_info(),
        "processes": get_processes(),
        "history": {
            "cpu": list(history['cpu']),
            "memory": list(history['memory']),
            "disk": list(history['disk']),
            "network": list(history['network']),
            "timestamps": list(history['timestamps'])
        },
        "alerts": alerts
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')