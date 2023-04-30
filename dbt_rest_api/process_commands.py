import subprocess
import traceback


def run_dbt_commands(dbt_command):
    try:
        if not dbt_command.startswith("dbt "):
            return "Not a DBT command"
        dbt_command = dbt_command.strip()

        sub_command = "python run_commands.py {0}".format(dbt_command)
        process = subprocess.Popen(sub_command, text=True)

        return "Command started"

    except Exception as e:
        return str(traceback.print_exc())
