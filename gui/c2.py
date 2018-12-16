import subprocess
import time
def get_log(path):
        cmd = 'adb logcat -d -v brief'
        log = open(path, 'w')
        content = subprocess.Popen(cmd, shell=True, stdout=log, stderr=subprocess.PIPE)
        return content

result = get_log('.//log.log')
text = result.communicate()
print(text)

time.sleep(5)

result.terminate()