import subprocess
import traceback


def run_dbt_commands(dbt_command):
    try:
        if not dbt_command.startswith("dbt "):
            return "Not a DBT command"
        dbt_command = dbt_command.strip()
        # more checks for commands

        sub_command = ["python", "run_commands.py", dbt_command]

        process = subprocess.Popen(sub_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return process.stdout.read() + "----" + process.stderr.read()

    except Exception as e:
        return str(traceback.print_exc())
