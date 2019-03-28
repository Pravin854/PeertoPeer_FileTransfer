import numpy
import os
import sys
import socket as s
import commands
import hashlib
import pickle

host_name = 'localhost'
port_number = 5050


def name_split(cmnd, i):
    cmnd = cmnd.split(" ")
    return cmnd[i]


def soc(cmnd):
    s1 = s.socket(s.AF_INET, s.SOCK_STREAM)
    s1.connect((host_name, port_number))
    s1.sendall(cmnd)

    return s1

def upload(cmnd):

    s1 = soc(cmnd)
    file_name = name_split(cmnd,1)
    with open(file_name, "rb") as file_send:
        for data in file_send:
            s1.sendall(data)
    s1.close()
    print "Data uploaded"
    file_send.close()
    print os.popen("ls -og --time-style=long-iso " + file_name).read()
    hash_nm = "FileHash verify " + file_name
    FileHash(hash_nm)
    
    return


def download(cmnd):

    s1 = soc(cmnd)
    file_name = name_split(cmnd,1)
    with open(file_name, "wb") as file_receive:
        while True:
            data = s1.recv(4096)
            if not data:
                break
            file_receive.write(data)
    
    file_receive.close()
    print os.popen("ls -og --time-style=long-iso " + file_name).read()
    print "Data downloaded"
    hash_nm = "FileHash verify " + file_name
    FileHash(hash_nm)
    s1.close()
    return




def FileHash(cmnd):
    
    raw1 = name_split(cmnd,1)
    s1 = soc(cmnd)

    if raw1 == "verify":

        raw2 = name_split(cmnd,2)
    	hashServer=s1.recv(4096)

    	hash_code = hashlib.md5()
    	with open(raw2, "rb") as file:
	        file_r = file.read(65536)
	        while len(file_r) > 0:
	            hash_code.update(file_r)
	            file_r = file.read(65536)


		hashClient = hash_code.hexdigest()
		print "Hash Value (Server) = ", hashServer
		print "Hash Value (Client) = ", hashClient
		# if hashClient == hashServer:
		# 	print 'No updates'
		# else:
		# 	print 'Updated' 

		s1.close()


    elif raw1 == 'checkall':

        hash_code = hashlib.md5()

        while 1:
        	
            f = s1.recv(4096)
            f1 = pickle.loads(f)
            # print f1
            for key, value in f1.items():

                with open(key, 'rb') as file:
                    
                    file_r = file.read(65536)
                    # print "file_r"
                    while len(file_r) > 0:
                        hash_code.update(file_r)
                        file_r = file.read(65536)
                            
                        hashClient = hash_code.hexdigest()
                        hashServer = value 

                        print "Filename = ", key
                        print "Hash Value (Server) = ", (hashServer)
                        print "Hash Value (Client) = ", (hashClient)
            break
        s1.close()
    return
  
def return_hash(command):
    hasha = os.popen(command).read()
    hasha = name_split(hasha, 0)
    return hasha 


def quit(cmnd):

    s1 = soc(cmnd)
    s1.close()
    return


def IndexGet(cmnd, flag_bon1):

    s1 = soc(cmnd)
    print cmnd
    command = name_split(cmnd,1)
    s1.sendall(cmnd)
    t1=s1.recv(4096)
    mid = pickle.loads(t1)
    bon_ar1 = []
    bon_lon = []
    bon_arr_extn = []
    bon_lon_extn = []


    if command == 'shortlist':
    
        if(len(cmnd.split(" ")) == 7):
            extn = name_split(cmnd,6)
            extn = extn + ":"
            extn = extn.split(".")
        str1 = ''.join(mid[1])
        k1 = str1.split("\n")

        if(flag_bon1 == 0):

            for i in range(len(k1) - 1):
                print mid[0][i], k1[i]

        else:
            flag_bon1 = 0 
            
            for i in range(len(k1) - 1):
                bon_ar1.append(k1[i].split(" "))

            for i in range(len(k1) - 1):
                bon_arr_extn.append(bon_ar1[i][0].split("."))

            for i in range(len(k1) - 1):
                
                if(extn[1] == bon_arr_extn[i][1]):
                    print mid[0][i], ",", k1[i]
                

    elif (command =='longlist'):

        if(len(cmnd.split(" ")) == 3):
            extn = name_split(cmnd,2)
            extn = extn + ":"
            extn = extn.split(".")
        
        if(flag_bon1 == 0):
            
            str1 = ''.join(mid[1])
            print mid[0], str1

        else:

            flag_bon1 = 0

            str1 = ''.join(mid[1])
            nxt_ln = str1.split("\n")

            jst_prnt = mid[0].split("\n")

            for i in range(len(jst_prnt) - 1):

                jst_prnt[i] = jst_prnt[i+1]
            
            
            for i in range(len(mid[1])):

                bon_lon.append(nxt_ln[i].split(":"))

            for i in range(len(mid[1])):
                
                bon_lon_extn.append(bon_lon[i][0].split("."))

            for i in range(len(mid[1])):

                bon_lon_extn[i][1] = bon_lon_extn[i][1] + ":"

            for i in range(len(mid[1])):

                if(extn[1] == bon_lon_extn[i][1]):
                    print jst_prnt[i], ",", mid[1][i]

    s1.close()
    return

def serverfiles(cmnd):

    k = -1
    s1 = soc(cmnd)
    fileString=s1.recv(4096)
    fileList=fileString.split(" ")
    for f in fileList[:k]:
        print f

    s1.close()
    return

def his(history, cmnd):
    print history
    return

def bonus1(cmnd):
    flag_bon1 = 1
    IndexGet(cmnd,flag_bon1)
    

history = ""
while(True):
    print " "
    print "#######################################################################################"
    print " "
    print "FileUpload <filename>, sendall file to the server."
    print "FileDownload <filename>, Download file from the server."
    print "show_client_files, List all files in this directory"
    print "show_server_files, List all files in the server"
    print "IndexGet shortlist <starttimestamp> <endtimestamp>, List the files modified in mentioned timestamp."
    print "IndexGet shortlist <starttimestamp> <endtimestamp> .entension, Bonus 1."
    print "IndexGet longlist, Similar to shortlist but with complete file listing"
    print "IndexGet longlist .extension, Bonus 2."
    print "FileHash verify/checkall <filename>, Checksum and lastmodified timestamp of the input file."
    print "history, To see command history"
    print "q or Q, To exit"
    print " "
    

    sys.stdout.write ("$> ")
    inp = sys.stdin.readline().strip()
    history = history + (inp +"\n")
    bon = inp.split(" ")
    flag_bon1 = 0
    if (inp == 'q' or inp == 'Q'):
        quit(inp)
        break
    elif (inp == 'show_server_files'):
        serverfiles('show_server_files')

    elif (inp == 'history'):
        his(history,inp)

    elif (inp == 'show_client_files'):
    	path = os.getcwd()
    	dirs = os.listdir(path)
    	for f in dirs:
    		print f
    
    elif (len(bon) == 7):
        if(bon[0] == "IndexGet"):
            bonus1(inp)

    elif(len(bon) == 3 and bon[0] == "IndexGet"):
        bonus1(inp)
             
    else:
    	command = name_split(inp,0)
    	if command == 'FileUpload':
    		upload(inp)
    	elif command == 'FileDownload':
    		download(inp)
        elif command =='IndexGet':
            IndexGet(inp,flag_bon1)
        elif command == 'FileHash':
            FileHash(inp)
