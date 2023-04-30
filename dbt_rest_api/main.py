import os
import logging
import google.cloud.logging
from flask import Flask, request
from process_commands import run_dbt_commands


app = Flask(__name__)

client = google.cloud.logging.Client()
client.setup_logging()


@app.route("/get_command", methods=['POST'])
def get_command():

    srv_json_data = request.get_json()
    logging.info(srv_json_data)
    logging.info([[name, value] for name, value in os.environ.items()])
    try:
        requested_command = srv_json_data["command"]
    except KeyError:
        return "<command> key not found"

    command_run_result = run_dbt_commands(requested_command)
    logging.info(command_run_result)

    return command_run_result

# service document


@app.route("/")
def welcome_page():
    return "Welcome"


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8080)))
