import numpy
import os
import sys
import socket
import commands
import hashlib
import pickle
from datetime import datetime, time

host_name = "localhost"
port_number = 5050

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Server Activated, YAYY !!"
except socket.error, msg :
    print "Unable to create Server :("
    print "Please Try again (Do not give up !!)"
    # print 'Error Code : ' , msg[0] 
    # print 'Message :' , msg[1]
    sys.exit()

try:
    s.bind((host_name, port_number))
except socket.error , msg:
    print 'Server binding failed. </3'
    # print 'Error Code :', msg[0] 
    # print 'Message :' , msg[1]
    sys.exit()

s.listen(1)
print "Server listening :D"
history = ""

def serverfiles():
    lst = ""
    addr = os.getcwd()
    for i in os.listdir(addr):
        lst = lst + i + " "
    snd.sendall(lst)
    return


def time_in_range(start, end, x):

    if(start <= end):
        return start <= x and x <= end
    if(start >= end):
        return start <= x or x <= end

def shortlist(data_0):

    strt_date = data_0[2]
    strt_time = data_0[3]
    end_date = data_0[4]
    end_time = data_0[5]

    strt_date = strt_date.split("-")
    strt_time = strt_time.split(":")
    end_date = end_date.split("-")
    end_time = end_time.split(":")


    strt_year = strt_date[0]
    strt_month = strt_date[1]
    strt_day = strt_date[2]

    strt_hr = int(strt_time[0])
    strt_minn = int(strt_time[1])

    end_year = end_date[0]
    end_month = end_date[1]
    end_day = end_date[2]

    end_hr = int(end_time[0])
    end_ti = end_time[1].split("I")
    end_minn = int(end_ti[0])


    ls = os.popen("ls -og --time-style=long-iso ").read()
    t2 = ls.split("\n")
    present_date = []
    present_time = []
    year = []
    month = []
    day = []
    hr = []
    minn = []
    rslt = []

    for i in range(len(t2) - 1):
        if(i != 0):
            k = t2[i].split(" ")
            present_date.append(k[len(k) - 3])
            present_time.append(k[len(k) - 2])

    t3 = []
    t4 = []
    rslt_type = []

    for i in range(len(t2) - 1):
        k = t2[i].split(" ")
        t3.append(k[len(k) - 1])

    for i in range(len(t3)):
        if(i != 0):
            t4.append(os.popen("file " + t3[i]).read())



    for i in range(len(present_date)):
        temp_date = present_date[i].split("-")
        temp_time = present_time[i].split(":")

        year.append(temp_date[0])
        month.append(temp_date[1])
        day.append(temp_date[2])

        hr.append(temp_time[0])
        minn.append(temp_time[1])

    for i in range(len(hr)):
        hr[i] = int(hr[i])
        minn[i] = int(minn[i])


    for i in range(len(present_date)):

        date_format = "%d/%m/%Y"
        temp1 = day[i] + "/" + month[i] + "/" + year[i]
        temp_strt_date = strt_day + "/" + strt_month + "/" + strt_year
        temp_end_date = end_day + "/" + end_month + "/" + end_year

        temp_present_date = datetime.strptime(temp1, date_format)

        if(datetime.strptime(temp_strt_date, date_format) <= temp_present_date < datetime.strptime(temp_end_date, date_format)):
            time_in_range(time(strt_hr, strt_minn), time(end_hr, end_minn), time(hr[i], minn[i]))

            rslt.append(t2[i+1])
            rslt_type.append(t4[i])
        



    finl_rslt = []
    finl_rslt = [rslt, rslt_type]
    snd_rslt = pickle.dumps(finl_rslt)
    snd.sendall(snd_rslt)
    return

def longlist():


    ls = os.popen("ls -og --time-style=long-iso ").read()
    t2 = ls.split("\n")
    t3 = []
    t4 = []

    for i in range(len(t2) - 1):
        k = t2[i].split(" ")
        t3.append(k[len(k) - 1])

    for i in range(len(t3)):
        if(i != 0):
            t4.append(os.popen("file " + t3[i]).read())

    t5 = []
    t5 = [ls,t4]
    data_long = pickle.dumps(t5)
    snd.sendall(data_long)

    return

def hasher():
    file_size = 65536
    return hashlib.md5()

def verify(tq1):

    hash_code = hasher()
    with open(tq1, "rb") as file:
        file_r = file.read(65536)
        while len(file_r) > 0:
            hash_code.update(file_r)
            file_r = file.read(65536)
    snd.sendall(hash_code.hexdigest())
    return

def checkall():

    hash_code = hasher()
    addr = os.getcwd()
    file_hash = {}
    for f in os.listdir(addr):
        print f

        with open(f, "rb") as file:
            file_r = file.read(65536)

            while len(file_r) > 0:
                hash_code.update(file_r)
                file_r = file.read(65536)

            file_hash.update({f:hash_code.hexdigest()})

        file.close()
    # print(file_hash)
    hash_data = pickle.dumps(file_hash)
    snd.sendall(hash_data)

    return

def FileUpload(cmnd):
    file_up = open(reqFile,"wb")
    si = data_0[2:]
    for p in si:
        p = p + " "
        file_up.write(p)
    while True:
        data = snd.recv(4096)
        if not data:
            break
        file_up.write(data)
    file_up.close()
    file_name = cmnd.split(" ")
    verify(file_name[1])
    print 'Data received'
    return

def FileDownload(cmnd):
    file_name = cmnd.split(" ")
    with open(reqFile, 'rb') as file_down:
        for data in file_down:
            snd.sendall(data)
    verify(file_name[1])
    print 'Data sent'
    return


def print_result(command, data):
    command = command.split(' ')
    if command[0] == "index": 
        print data
    elif command[0] == "hash" :
        if(command[1] == "verify") :
            print "MD5 checksum      Last modified"
            print data
        elif(command[1] == "checkall") :
            data = data.split('\n')
            print "Filename       MD5 checksum      Last modified"
            for entry in data:
                print entry
    return



while True:
    snd, num = s.accept()
    print "Got connected from ", num[0], ':', num[1]
    data = snd.recv(4096)
    print "$> ", data
    history = history + (data + "\n")
    data_0 = data.split(" ")

    if (data == 'Q' or data == 'q'):
        break
    
    elif (data == "show_server_files"):
        serverfiles()

    elif (data_0[1] == "shortlist"):
        shortlist(data_0)

    elif (data_0[1] == "longlist"):
        longlist()

    elif (data_0[0] == "FileHash"):
        if(data_0[1] == "verify"):
            verify(data_0[2])

        elif (data_0[1] == "checkall"):
            checkall()
        print "Hashed"

    else:
        data_0 = data.split(" ")
        if(len(data_0) > 1):
            reqFile = data_0[1]
            if (data_0[0] == "FileUpload"):
                FileUpload(data)
            elif (data_0[0] == "FileDownload"):
                FileDownload(data)

    snd.close()

s.close()