import os
import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/run_command", methods=['POST'])
def submit_job():

    service_json_data = request.get_json()

    validated_data = validate_command(service_json_data)
    if isinstance(validated_data, list):
        dbt_work_dir = os.environ.get("DBT_DIR")

        process = subprocess.Popen(validated_data, cwd=dbt_work_dir,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()

        return jsonify("Command executed successfully. Result: " + process.stdout.read()), 200
    else:
        return jsonify({"code": 400, "name": "BadRequest", "description": validated_data})


# service document

@app.route("/")
def welcome_page():
    return jsonify("Welcome")


def validate_command(json_data):

    requested_command = json_data["command"]
    requested_command = requested_command.strip()

    if "command" not in json_data.keys() or len(json_data.keys()) != 1 or not isinstance(requested_command, str):
        response = '"command" key not found or misconfigured request. '\
                    'Example usage: {"command": "dbt test"}'

    elif any(multi_cmd in requested_command for multi_cmd in ["&&", ";", "||"]):
        response = "Multiple commands not allowed"

    elif not requested_command.startswith("dbt "):
        response = "Not a DBT command"
    else:
        response = requested_command.split(" ")

    return response


@app.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':

    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8080)), threaded=False)
