from os import (system, path)
from re import match

FILE_PATH = ".\hosts.txt"

################################################# Clases

#------------------ Custom error

class InputValueError(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)

#------------------ class host with hostname and ip_address

class Host:
    def __init__(self):
        self.hostname = None
        self.ip_address = None


################################################# Functions


#---------------- check is file hosts.txt exist, if not - create it

def check_exist_file_hosts():
    if path.isfile(FILE_PATH) == False:
        creater = open(FILE_PATH, "w")
        creater.close()

#--------------- Open file and return dict with host and it's ip

def open_file():

    """Open file and return dict with host and it's ip"""

    reader = open(FILE_PATH, 'r')
    try:
        lines = reader.readlines()
        ready_dyct = {}                                                 # create empty dict 
        for index in range(0, len(lines)):                              # in every line change end of line and add to dict values like host - ip
            lines[index] = lines[index].replace("\n", "")
            s = lines[index].split(" - ")
            ready_dyct[s[0]] = s[1]
    finally:
        reader.close

    return ready_dyct


#------------------ Will append new data to hosts.txt

def append_data_file(hostname, ip_address):
    append_d = open(FILE_PATH, "a")
    append_d.write(f"\n{hostname} - {ip_address}")
    append_d.close


#---------------- make ping to host and return 0 if it up, 1 - if down

def ping_command(hostname):

    """It makes ping requests, return 0 if up, 1 if down"""

    response = system("ping -n 1 " + hostname + " -l 1400")

    return response


#---------------------- add hostname / return True if hostname name is correct, False - if no
    
def check_hostname(hostname):
        if match(r"^[A-Z]{1}[a-zA-Z0-9_]{2,14}$", hostname):
            return True
        else:
            return False

#---------------------- add ip address / return True if ip is correct, False - if no

def check_ip(ip_address):  
    if match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", ip_address) == False:
        return False
    else:
        bytes = ip_address.split(".")
        for ip_byte in bytes:
            if int(ip_byte) > 0 and int(ip_byte) < 255:
                return True
            else:
                return False      

#----------------------- if ip is up - add new host to hosts.txt / return True if host is up, False - if no

def check_host_up(ip_address):
    if ping_command(ip_address) == 0:
        return True
    else:
        return False
    

#------------------------- Find ip of host

def find_ip_of_host(hostname, dict_hosts):
    return dict_hosts[hostname]


#------------------------- List of upp hosts / return dict

def list_of_up_hosts(dict_hosts):
    dict_up_hosts = {}
    
    for key in dict_hosts:
        if ping_command(dict_hosts[key]) == 0:
            dict_up_hosts[key] = dict_hosts[key]

    return dict_up_hosts


#--------------------------- list of down hosts / return dict

def list_of_down_hosts(dict_hosts):
    dict_down_hosts = {}

    for key in dict_hosts:
        if ping_command(dict_hosts[key]) == 1:
            dict_down_hosts[key] = dict_hosts[key]
            print(f"host {key} added")

    return dict_down_hosts


#---------------------------- Delete item from list

def change_value(old_value, new_value):

    with open(FILE_PATH, "r") as file:
        filedata = file.read()

    filedata = filedata.replace(old_value, new_value)
    with open(FILE_PATH, "w") as file:
        file.write(filedata)