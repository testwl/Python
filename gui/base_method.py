import cv2
import os
import re
import subprocess
import signal
from PIL import Image, ImageTk
from pystrich.code128 import Code128Encoder
from pystrich.qrcode import QRCodeEncoder
from xml.dom.minidom import parse

class Method():

    def barcode(self, code):
        encoder = Code128Encoder(code)
        encoder.save('barcode.png')

    def qcode(self, code):
        encoder = QRCodeEncoder(code)
        encoder.save('qrcode.png')

    def capture(self):
        os.system("adb shell screencap -p /sdcard/screen.png ")
        os.system('adb pull /sdcard/screen.png ./')

    def info(self, container, command):
        text = os.popen(command).read()
        container.config(text=text)

    def record(self):
        os.system("adb shell screenrecord --size 270x480 --time-limit 10 /sdcard/record.mp4")
        os.system('adb pull /sdcard/record.mp4 ./')

    def show_image(self, container, file, x=1):
        image_open = Image.open(file)
        w, h = image_open.size
        image = image_open.resize((int(w/x), int(h/x)), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        container.config(image=render)
        container.image = render

    def show_video(self):
        cap = cv2.VideoCapture('./record.mp4')
        while(1):
            ret ,frame = cap.read()
            if ret != True:
                break
            cv2.imshow('video',frame)
            cv2.waitKey(1000)
        cap.release()
        cv2.destroyAllWindows()

    def apk_apktool(self, container, apkfile):
        if apkfile:
            apkname = os.path.basename(apkfile)
            name = re.findall('(.*).apk', apkname)
            os.system('apktool d -f {} -o .//doc//{}'.format(apkfile, name[0]))
            dom = parse('.//doc//{}//AndroidManifest.xml'.format(name[0]))
            root=dom.documentElement
            package=root.getAttribute('package')
            activityList = root.getElementsByTagName('activity')
            for activity in activityList:
                if activity.toxml().find("android.intent.action.MAIN")>0 \
                and activity.toxml().find("android.intent.category.LAUNCHER")>0:
                    MainActivity=activity.getAttribute('android:name')

            container.config(text='package:{}\nMainActivity:{}'.format(package, MainActivity))
        else:
            container.config(text = '请选择文件或输入安装包路径')

    def apk_aapt(self, container, apkfile):
        if apkfile:
            content = subprocess.Popen(['aapt', 'dump', 'badging', '{}'.format(apkfile)], shell=True, stdout=subprocess.PIPE).communicate()
            text = content[0].decode('utf-8')
            result1 = re.findall("package: name='(.*?)' versionCode='(.*?)' versionName='(.*?)'", text)
            result2 = re.findall("launchable-activity: name='(.*?)'  label", text)
            output = 'package name：{}\n versionCode: {}\n versionName: {}\n launchable-activity: {}'.format(result1[0][0], result1[0][1], result1[0][2], result2[0])
            container.config(text = output)
        else:
            container.config(text = '请选择文件或输入安装包路径')

    def inapk(self, container, apkfile):
        if apkfile:
            text = os.popen('adb install -r {}'.format(apkfile))
            container.config(text=text.read())
        else:
            container.config(text = '请选择文件或输入安装包路径')
            
    def log_level(self, path, level):
        content = open(path, encoding = 'utf8').readlines()
        results = []
        for line in content:
            result = re.findall('^{}.+'.format(level), line)
            if  result:
                results.append(result)
        return results

    def get_pid(self, path, packagename):
        content = open(path, encoding = 'utf-8').readlines()
        pids = []
        for line in content:
            if packagename in line:
                pid = re.findall('\(([\s\d]*)?\):', line)
                if pid not in pids:
                    pids.append(pid)
        return pids

    def log_pid(self, path, pids):
        content = open(path, encoding='utf8').readlines()
        lines = []
        for line in content:
            for pid in pids:
                pid_log = re.findall('\(([\s\d]*)?\):', line)
                if pid_log:
                    if pid[0] == pid_log[0]:
                        lines.append(line)
        return lines

    def get_log(self):
        os.system("adb logcat -c")
        cmd = 'adb logcat -v brief'
        log = open('.//log.log', 'w')
        content = subprocess.Popen(cmd, shell=True, stdout=log, stderr=subprocess.PIPE)
        # subprocess.Popen(cmd, shell=True, stdout=log, stderr=subprocess.PIPE)
        return content
    
    def close_log(self):
        os.system('adb kill-server')
        

