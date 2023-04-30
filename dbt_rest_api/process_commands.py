import subprocess
import traceback


def run_dbt_commands(dbt_command):
    try:
        if not dbt_command.startswith("dbt "):
            return "Not a DBT command"
        dbt_command = dbt_command.strip()
        # more checks for commands

        sub_command = ["python", "run_commands.py", dbt_command]

        process = subprocess.Popen(sub_command, text=True)

        if not process.stderr.read():

            return "Command started"
        else:
            process.stderr.read()

    except Exception as e:
        return str(traceback.print_exc())
