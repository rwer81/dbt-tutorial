import os
import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/run_command", methods=['POST'])
def submit_job():
    """
    Get and run DBT command. Before run checks if it has correct structure.
    Execute command and wait for result.

    :return: Json Response: if valid command return Dbt execution result. Else command validation result.
    """
    # Get post data
    service_json_data = request.get_json()

    # Validate post data and command if it is safe and has correct structure
    validated_data = validate_command(service_json_data)

    # If it is suitable to run validation result should be list of command strings
    if isinstance(validated_data, list):
        dbt_work_dir = os.environ.get("DBT_DIR")

        # Create a subprocess to run executable dbt command
        process = subprocess.Popen(validated_data, cwd=dbt_work_dir,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()

        # Handle the execution result
        run_result = process.stdout.read()

        if "Encountered an error" in run_result:
            return jsonify({"code": 200, "name": "Dbt Error ", "description": run_result})
        else:
            return jsonify({"code": 200, "name": "Success", "description": run_result})
    else:
        return jsonify({"code": 400, "name": "BadRequest", "description": validated_data})


@app.route("/")
def welcome_page():
    """
    Simple Get request.
    :return: Json Response.
    """
    return jsonify({"code": 200, "name": "Success", "description": "Welcome. Service is alive"})


def validate_command(json_data):
    """
    Check and validate incoming API post data to be sure it is a dbt command and safe to run.
    A valid command should:
        - have only one key that is 'command'
        - be string not a list or number etc.
        - not include any multiple command execution symbol
        - start with 'dbt '(with space)

    :param json_data: Json object that includes API post body json data
    :return: str or list obj.
    """
    if "command" not in json_data.keys() or len(json_data.keys()) != 1:
        response = '"command" key not found or misconfigured request. '\
                    'Example usage: {"command": "dbt test"}'
        return response

    requested_command = json_data["command"]

    if not isinstance(requested_command, str):
        response = "Commands can only be strings"
        return response

    requested_command = requested_command.strip()

    if any(multi_cmd in requested_command for multi_cmd in ["&&", ";", "||"]):
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
