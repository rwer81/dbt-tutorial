import os
import logging
from flask import Flask, request
from process_commands import run_dbt_commands

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/get_command", methods=['POST'])
def get_command():

    srv_json_data = request.get_json()
    logger.info(srv_json_data)

    try:
        requested_command = srv_json_data["command"]
    except KeyError:
        return "<command> key not found"

    command_run_result = run_dbt_commands(requested_command)
    logger.info(command_run_result)

    return command_run_result

# service document


@app.route("/hello_world")
def welcome_page():
    return "Welcome"


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8080)))
