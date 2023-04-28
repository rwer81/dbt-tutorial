import subprocess


def run_dbt_commands(dbt_command):
    #if not dbt_command.startswith("dbt "):
    #    return "eerrttr"

    dbt_work_dir = r"C:\Users\SAHIN\Desktop\projects\dbt_works\case_study"

    result = subprocess.run([dbt_command], cwd=dbt_work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            shell=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr

