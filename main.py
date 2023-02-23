from functions import *                                                                     # functions.py
import os                                                                                   # os commands, ping
from telebot import *                                                                       # telebot for telegram
from dotenv import load_dotenv                                                              # load env from file tel_tok.env                                              
from pathlib import Path                                                                    # need for dotenv


# hosts_list - List of hosts
# oflline - Offline hosts
# online - Online hosts
# check_host - Check host
# add_host - Add new host
# remove_host - Remove host from list

############################################# Main Program ############################################

                                                      
dotenv_path = Path('tel_tok.env')                                                           # path to .env file
load_dotenv(dotenv_path=dotenv_path)                                                        # take environment variables from .env.
BOT_TOKEN = os.getenv('BOT_TOKEN')  

bot = telebot.TeleBot(BOT_TOKEN)                                                            # creating bot
new_host = Host()                                                                           # in add_host section
check_exist_file_hosts()                                                                    # check is file with host exist


############################################## TELEGRAM BOT



# ------------------------------------ Menu hosts_list

@bot.message_handler(commands=['hosts_list'])                                                  
def hosts_list(message):
    bot.send_message(message.from_user.id, "LIST OF ALL HOSTS:")
    hosts_dict = open_file()                                                                                # get dict of hosts from file
    for key in hosts_dict:
        bot.send_message(message.from_user.id, f"{key} - {hosts_dict[key]}")                                # bot unsver
    bot.send_message(message.from_user.id, f"Go to main Menu")


#-------------------------------------- Menu offline

@bot.message_handler(commands=['oflline'])
def offline(message):
    bot.send_message(message.from_user.id, "LIST OF OFFLINE HOSTS:")
    offline_host_dict = list_of_down_hosts(open_file())                                                     # get dict of hosts with state down
    for key in offline_host_dict:
        bot.send_message(message.from_user.id, f"{key} - {offline_host_dict[key]}")                         # print every item in dict
    bot.send_message(message.from_user.id, f"Go to main Menu")

#-------------------------------------- Menu Online

@bot.message_handler(commands=['online'])
def online(message):
    bot.send_message(message.from_user.id, "LIST OF ONLINE HOSTS:")
    online_host_dict = list_of_up_hosts(open_file())                                                        # get dict of hosts with state up
    for key in online_host_dict:
        bot.send_message(message.from_user.id, f"{key} - {online_host_dict[key]}")                          # print every item in dit
    bot.send_message(message.from_user.id, f"Go to main Menu")


#-------------------------------------- Menu check_host

@bot.message_handler(commands=['check_host'])
def check_host(message):
    bot.send_message(message.from_user.id, "LIST OF AVAILABLE HOSTS:")
    dict = open_file()                                                                                      # get dict of all hosts
    counter = 1
    for key in dict:
        bot.send_message(message.from_user.id, f"{counter} - {key}")                                        # print every item in dict
        counter += 1
    msg = bot.send_message(message.from_user.id, "Please tell me name of host which you want to check")     # get a message from user
    bot.register_next_step_handler(msg, check_host_in_list)                                                 # call check_host_in_list() with getted from user message

def check_host_in_list(message):
    try:
        if (message.text not in open_file()):                                                               # if name of host, entered from user is not in list
            raise InputValueError("Hostname is not correct")                                                # send error message
        else:
            pass
    except InputValueError as error:
        bot.send_message(message.from_user.id, error)
        bot.register_next_step_handler(message, check_host_in_list)                                         # call check_host_in_list() again, until user will enter host name from list
    else:
        ip_address = find_ip_of_host(message.text, open_file())                                             # if host eneter correct, get ip of this host
        if ping_command(ip_address) == 0:                                                                   # if ip is up
            bot.send_message(message.from_user.id, f"{message.text} - {ip_address} is up")                  # send message
        else:                                                                                       
            bot.send_message(message.from_user.id, f"{message.text} - {ip_address} is down")
        bot.send_message(message.from_user.id, f"Go to main Menu")




#-------------------------------------- Menu add_host

@bot.message_handler(commands=['add_host'])
def add_host(message):
    bot.send_message(message.from_user.id, "Ok lets, add new item in list")                                 # get name of host from user
    msg = bot.send_message(message.from_user.id, "Please enter hostname without pass, len should be from 3 to 15 symbols, firsl letter - uppercase:")
    bot.register_next_step_handler(msg, add_host_data)                                                      # call next function add_host_data()

def add_host_data(message):
    try:
        if (message.text in open_file()):                                                                   # if the host already exist
            raise InputValueError("Hostname already exist in list")                                         # send error message
        if check_hostname(message.text) == False:                                                           # if host name entered not correct
            raise InputValueError("Not correct host, try again")                                            # send error message
        else:
            bot.send_message(message.from_user.id, "Greate, now lets enter ip address this host:")          
            bot.register_next_step_handler(message, add_host_ip)                                            # if host entered correct, call add_host_ip()
            new_host.hostname = message.text
    except InputValueError as error:
        bot.send_message(message.from_user.id, error)
        bot.register_next_step_handler(message, add_host_data)                                              # if error, call add_host_data() again

def add_host_ip(message):
    try:
        if check_ip(message.text) == False:                                                                 # if ip is not correct
            raise InputValueError("Not correct ip address")                                                 # send message
        if message.text in open_file().values():                                                            # if ip already in the list
            raise InputValueError("Host with this ip already exist in list")                                # send message
        if check_host_up(message.text) == False:                                                            # if ip is down
            raise InputValueError("Host is not up, I will not add new host, until it will be up")           # send error message
        else: 
            new_host.ip_address = message.text
            bot.send_message(message.from_user.id, f"{new_host.hostname} - {new_host.ip_address} added")    # if ip is correct and up - send message
            append_data_file(new_host.hostname, new_host.ip_address)                                        # add new item to the file
            bot.send_message(message.from_user.id, f"Go to main Menu")
    except InputValueError as error:
        bot.send_message(message.from_user.id, error)
        bot.register_next_step_handler(message, add_host_ip)                                                # if error - call add_host_ip() again


# ------------------------------------ Menu remove_host

@bot.message_handler(commands=['remove_host'])
def remove_host(message):
    bot.send_message(message.from_user.id, "LET ME SHOW YOU LIST OF HOST:")
    hosts_dict = open_file()                                                                                # get dict of hosts from file
    for key in hosts_dict:
        bot.send_message(message.from_user.id, f"{key} - {hosts_dict[key]}")                                # show list of all hosts
    msg = bot.send_message(message.from_user.id, "TEL ME WHICH HOST YOU WANT TO DELETE:")                   # send a message and get unswer from user
    bot.register_next_step_handler(msg, remove_host_from_list)                                              # call remove_host_from_list() to remove the host

def remove_host_from_list(message):
    try:
        if (message.text not in open_file()):                                                               # if hostname not in list
            raise InputValueError("Hostname is not in the list")                                            # send a message
        else:
            change_value(f"{message.text} - {open_file()[message.text]}\n", "")                             # if host in list - change_value to delete host from file
            bot.send_message(message.from_user.id, "Host is succesfully deleted")
            bot.send_message(message.from_user.id, "Go to main Menu")
    except InputValueError as error:
        bot.send_message(message.from_user.id, error)                                                       
        bot.register_next_step_handler(message, remove_host_from_list)                                      # if error, call remove_host_from_list() to get correct hostname again


bot.polling(none_stop=True, interval=0)                                                                     # Repeat circle of process all the time