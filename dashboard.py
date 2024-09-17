from flask import Flask, render_template
import os
import psutil
import platform
from datetime import datetime
from functools import lru_cache
import subprocess
import threading
import time

from utils.logger import app_logger

app = Flask(__name__)

bot_status = None
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


def periodic_status_check(interval=60):
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
        temp = cpu_thermal[0].current if cpu_thermal else "N/A"
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


def run_flask_app():
    app_logger.info("Starting dashboard...")
    app.run(host="0.0.0.0", port=5000, threaded=True)


status_thread = threading.Thread(target=periodic_status_check, args=(60,))
status_thread.daemon = True
status_thread.start()

if __name__ == "__main__":
    run_flask_app()
