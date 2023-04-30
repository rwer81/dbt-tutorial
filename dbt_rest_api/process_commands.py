import os
import subprocess
import traceback


def run_dbt_commands(dbt_command):
    try:
        if not dbt_command.startswith("dbt "):
            return "Not a DBT command"
        dbt_command = dbt_command.strip()
        # more checks for commands

        sub_command = "python run_commands.py {0} &".format(dbt_command)

        process = os.system(sub_command)

        return "Command started."

    except Exception as e:
        return str(traceback.print_exc())
