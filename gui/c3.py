import subprocess
import time
import os

order='adb logcat'

pi= subprocess.Popen(order,shell=True,stdout=subprocess.PIPE)

for i in iter(pi.stdout.readline,'b'):

    print(i)

time.sleep(5)

os.system('adb kill-server')

