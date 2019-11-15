# -*- coding:utf-8 -*-
import socket
import urllib
import thread
import threading
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-+8')

host = '192.168.0.104'
print(host)
port = 5000

ENV_Len = 8
ENV_Status = [0,10000,2,23,43,321,498,54]

def Communicate(info):
    if info == 'G' or  info == 'Get' or  info == 'GET':
        threadLock.acquire()
        ENV_DATA = ''
        for i in range(ENV_Len):
            ENV_DATA += str(ENV_Status[i])
            ENV_DATA += '|'
        threadLock.release()
        return ENV_DATA
    else:
        return ''

def Server_Socket(host,port):
    Socket_status = 'BUSY'
    while True:
        while Socket_status == 'BUSY':
            try:
                clnt = ''
                addr = ''
                Sk = socket.socket()
                Sk.bind((host, port))
                Sk.listen(1)
                clnt, addr = Sk.accept()
                print('Address is:', addr)
                print('I am waiting for Client...')
                Socket_status = 'FREE'
                pass
            except Exception:
                print('Try Socket Error:',Exception)
                Socket_status = 'BUSY'
                pass
        print('Getting a new Connect!')
        while Socket_status == 'FREE':
            data = clnt.recv(1024)
            recv_n = len(data)
            print('Going to:', data , ' Len: ', recv_n)
            if recv_n == 0:
                Sk.close()
                print('Server Socket Closed!')
                Socket_status = 'BUSY'
                break
            result = Communicate(data)
            if len(result) == 0:
                result = 'EXD'
            clnt.sendall(result)
    Sk.close()


while True:
    threadLock = threading.Lock()
    try:
        thread.start_new_thread(Server_Socket,(host,port,))
        pass
    except e:
        print('Thread Create Failed! Main Finished.')
        break
    while True:
        print('I am the main thread:', ENV_Status[0],'|',ENV_Status[1],'|',ENV_Status[2],'|',ENV_Status[3],'|',ENV_Status[4],'|',ENV_Status[5],'|',ENV_Status[6],'|',ENV_Status[7])
        time.sleep(2)
        threadLock.acquire()
        ENV_Status[0] += 1
        ENV_Status[1] -= 2
        ENV_Status[2] += 3
        ENV_Status[3] += 2
        ENV_Status[4] += 5
        ENV_Status[5] += 7
        ENV_Status[6] -= 1
        ENV_Status[7] += 3
        threadLock.release()
    
