import subprocess
import logging
def run_shell(command):
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for info in iter(cmd.stdout.readline, 'utf8'):
        logging.info(info)

cmd = 'adb logcat'
run_shell(cmd)