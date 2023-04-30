import subprocess
import os
import sys
import logging
import google.cloud.logging
import traceback


def run_dbt_commands(dbt_cmd):
    subprocess_log = open('./subprocess_logs.log', 'a')
    try:
        client = google.cloud.logging.Client()
        client.setup_logging()

        dbt_cmd = dbt_cmd.split(" ")

        dbt_work_dir = os.environ.get("DBT_DIR")
        print(dbt_cmd)
        process = subprocess.Popen(dbt_cmd, cwd=r"C:\Users\SAHIN\Desktop\projects\dbt_works\case_study",
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
        process.wait()
        out_log = process.stdout.read()
        err_log = process.stderr.read()

        logging.info(out_log)
        logging.info(err_log)

    except Exception as e:
        logging.info(str(traceback.print_exc()))


if __name__ == '__main__':
    dbt_command = " ".join(sys.argv[1:])
    run_dbt_commands(dbt_command)




