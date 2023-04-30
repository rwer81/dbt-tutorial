import os
import queue
import threading
import subprocess
import logging
import traceback
import google.cloud.logging
from flask import Flask, request


app = Flask(__name__)


def run_dbt_command():
    logging.info("in run_dbt_command")
    with lock:
        while not cmd_queue.empty():
            try:

                dbt_command = cmd_queue.get()
                logging.info(dbt_command)
                dbt_work_dir = os.environ.get("DBT_DIR")
                logging.info(dbt_work_dir)
                process = subprocess.Popen(dbt_command, cwd=dbt_work_dir,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           text=True)
                process.wait()
                out_log = process.stdout.read()
                err_log = process.stderr.read()

                logging.info(out_log)
                logging.info(err_log)
                logging.info("completed")
            except Exception:
                return str(traceback.print_exc())


@app.route("/get_command", methods=['POST'])
def submit_job():
    srv_json_data = request.get_json()
    if "command" not in srv_json_data.keys():
        return "'command' key not found"
    requested_command = srv_json_data["command"]

    if not requested_command.startswith("dbt "):
        return "Not a DBT command"

    # more checks for commands
    dbt_command = requested_command.strip()
    dbt_command = dbt_command.split(" ")
    # more checks for commands
    if not cmd_queue.empty():
        cmd_queue.put(dbt_command)
        return 'QUEUED. New queue size {0}'.format(cmd_queue.qsize()), 200
    else:
        cmd_queue.put(dbt_command)
        cc = threading.Thread(target=run_dbt_command)
        cc.start()
        return 'QUEUED and STARTED. New queue size {0}'.format(cmd_queue.qsize()), 200

# service document

@app.route("/")
def welcome_page():
    return "Welcome"


if __name__ == '__main__':
    client = google.cloud.logging.Client()
    client.setup_logging()

    cmd_queue = queue.Queue()
    lock = threading.RLock()
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8080)), threaded=False)
