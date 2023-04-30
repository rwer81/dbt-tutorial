import subprocess
import traceback
import os

def run_dbt_commands(dbt_command):
    try:
        if not dbt_command.startswith("dbt "):
            return "Not a DBT command"
        dbt_command = dbt_command.strip()

        sub_command = "python run_commands.py {0}".format(dbt_command)
        print([[name, value] for name, value in os.environ.items()])
        process = subprocess.Popen(sub_command, text=True)

        return "Command started"

    except Exception as e:
        return str(traceback.print_exc())
