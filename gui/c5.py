import subprocess
import os
import signal
try:
    os.system("adb logcat -c")
    cmd = 'adb logcat -v brief'
    log = open('.//log2.log', 'w')
    content = subprocess.Popen(cmd, shell=True, stdout=log, stderr=subprocess.PIPE)
    # p =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # content.send_signal(signal.CTRL_C_EVENT)
    
except KeyboardInterrupt:
    os.kill(0, signal.CTRL_C_EVENT)
