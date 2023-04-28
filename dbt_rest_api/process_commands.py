import subprocess
import os


def run_dbt_commands(dbt_command):
    if not dbt_command.startswith("dbt "):
        return "Not a DBT command"

    dbt_work_dir = os.environ.get("DBT_DIR")

    result = subprocess.Popen([dbt_command], cwd=dbt_work_dir,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)

    #result = subprocess.run([dbt_command], #cwd=dbt_work_dir,
    #                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr
