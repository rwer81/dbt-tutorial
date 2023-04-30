import os
import queue
import threading
import subprocess
import logging
import traceback
import google.cloud.logging
from flask import Flask, request


app = Flask(__name__)


@app.route("/get_command", methods=['POST'])
def submit_job():
    logging.info("in submit_job")
    srv_json_data = request.get_json()
    if "command" not in srv_json_data.keys():
        return "'command' key not found"
    requested_command = srv_json_data["command"]

    if not requested_command.startswith("dbt "):
        return "Not a DBT command"
    # more checks for commands
    dbt_command = requested_command.strip()
    dbt_command = dbt_command.split(" ")

    try:
        dbt_work_dir = os.environ.get("DBT_DIR")
        logging.info(dbt_work_dir)
        process = subprocess.Popen(dbt_command, cwd=dbt_work_dir,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()
        return process.stdout.read()

    except Exception:
        return str(traceback.print_exc())



# service document

@app.route("/")
def welcome_page():
    return "Welcome"


if __name__ == '__main__':
    client = google.cloud.logging.Client()
    client.setup_logging()

    logging.info("in maninnnnnnnnnnnnnn")

    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8080)), threaded=False)
