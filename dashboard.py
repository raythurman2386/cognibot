from flask import Flask, render_template
import os
import psutil
import platform
from datetime import datetime
import subprocess
import threading
import time

from utils.logger import app_logger

app = Flask(__name__)

bot_status = None
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = "db/chat_log.sqlite"


def update_bot_status(status):
    global bot_status
    bot_status = status


def check_service_status():
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "cognibot.service"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode == 0:
            return "active"
        else:
            return "inactive"
    except Exception as e:
        return f"error: {str(e)}"


def periodic_status_check(interval=10):
    while True:
        status = check_service_status()
        update_bot_status(status)
        time.sleep(interval)


def get_system_info():
    try:
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        temperatures = psutil.sensors_temperatures()
        cpu_thermal = temperatures.get("cpu_thermal")
        temp = (
            # Raspberry Pi Temp Sensor
            cpu_thermal[0].current
            if cpu_thermal
            else (
                # Temp sensor on my machine
                temperatures.get("coretemp")[0].current
                if temperatures.get("coretemp")
                else "N/A"
            )
        )
        net_io = psutil.net_io_counters()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        db_size = os.path.getsize(db_path) / (1024 * 1024)

        return {
            "cpu_percent": cpu_percent,
            "memory": memory,
            "disk": disk,
            "temp": temp,
            "net_io": net_io,
            "uptime": uptime,
            "db_size": db_size,
        }
    except Exception as e:
        app_logger.error(f"Error fetching system info: {str(e)}")
        return None


def get_last_20_lines(file_path, num_lines=20):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines[-num_lines:]
    except Exception as e:
        app_logger.error(f"Error reading log file: {str(e)}")
        return ["Error fetching logs."]


@app.route("/")
def home():
    try:
        system_info = get_system_info()
        if system_info is None:
            return "Error fetching system information", 500

        return render_template(
            "home.html",
            bot_status=bot_status,
            system_info=system_info,
            platform_system=platform.system(),
            platform_release=platform.release(),
        )
    except Exception as e:
        app_logger.error(f"Error in dashboard home route: {str(e)}")
        return "An error occurred", 500


@app.route("/update_cpu")
def update_cpu():
    system_info = get_system_info()
    return render_template("components/cpu_usage.html", system_info=system_info)


@app.route("/update_memory")
def update_memory():
    system_info = get_system_info()
    return render_template("components/memory_usage.html", system_info=system_info)


@app.route("/update_disk")
def update_disk():
    system_info = get_system_info()
    return render_template("components/disk_usage.html", system_info=system_info)


@app.route("/update_temp")
def update_temp():
    system_info = get_system_info()
    return render_template("components/cpu_temperature.html", system_info=system_info)


@app.route("/update_bot_status")
def update_bot_status_view():
    return render_template("components/bot_status.html", bot_status=bot_status)


@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    shutdown_script = os.path.join(current_dir, "scripts", "shutdown.sh")
    try:
        result = subprocess.run(
            [shutdown_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            return "Bot stopped successfully"
        else:
            return f"Failed to stop bot: {result.stderr.decode()}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/restart_bot", methods=["POST"])
def restart_bot():
    restart_script = os.path.join(current_dir, "scripts", "restart.sh")
    try:
        result = subprocess.run(
            [restart_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode == 0:
            return "Bot restarted successfully"
        else:
            return f"Failed to restart bot: {result.stderr.decode()}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/update_bot", methods=["POST"])
def update_bot():
    update_script = os.path.join(current_dir, "scripts", "update.sh")
    try:
        result = subprocess.run(
            [update_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            return "Bot updated successfully"
        else:
            return f"Failed to update bot: {result.stderr.decode()}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/logs")
def fetch_logs():
    log_file_path = os.path.join(current_dir, "Logs", "cognibot.log")
    logs = get_last_20_lines(log_file_path)
    return render_template("components/logs.html", logs=logs)


def run_flask_app():
    app_logger.info("Starting dashboard...")
    app.run(host="0.0.0.0", port=5000, threaded=True)


status_thread = threading.Thread(target=periodic_status_check, args=(60,))
status_thread.daemon = True
status_thread.start()

if __name__ == "__main__":
    run_flask_app()
