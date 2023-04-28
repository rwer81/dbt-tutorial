from flask import Flask, request
from process_commands import run_dbt_commands
app = Flask(__name__)


@app.route('/get_command', methods=['POST'])
def get_command():
    srv_json_data = request.get_json()
    try:
        requested_command = srv_json_data["command"] # command key not found
    except KeyError:
        return "<command>' key not found"
    command_run_result = run_dbt_commands(requested_command)

    return command_run_result


if __name__ == '__main__':
    app.run(port=8080)
