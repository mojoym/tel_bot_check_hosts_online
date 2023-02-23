HOW TO LUNCH:

1 Create file  tel_tok.env
2 Create variable BOT_TOKEN
3 Save your token into variable
4 It should look line this:
BOT_TOKEN="YOUR PERSONAL TELEGRAM TOKEN"

5 instal telebot:           pip install pyTelegramBotAPI
6 install dotenv:           pip install python-dotenv
7 install pathlib:          pip install pathlib
8 file hosts.txt after lunching will be created automaticaly, and bot will add one test item

This Telegram bot:
1 Can show list of hosts
2 Can show offline hosts
3 Can show online hosts
4 Can check is host from the list, which you will chose online or not
5 Can add hosts with ip to list of monitoring hosts, but, before you will add new item:
    - it will check correctly enter name
    - is name exist in list
    - it will check correctly entered ip address
    - is ip address exist in the list
6 Can remove host from the list