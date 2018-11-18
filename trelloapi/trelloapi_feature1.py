#!/usr/bin/python
"""
Script to send an email to professor whenever
any cards in the DevOps course boards did not
move from last 14 days
This script can be executed every EOD
"""
import requests
import json
import dateutil.parser
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from typing import List, Set, Dict
except ImportError:
    print("WARNING: Typing module is not found! Kindly install the latest version of python!")

# extracting the present time
time_now = datetime.datetime.utcnow()

# setting a days of inactivity limit
days_of_inactivity_limit = 14 # type: int #default value: 14 days

# initializing key and token api for trelloapi to function
querystring = {"key":"b282952c1211b7eb3c16b7c3adfbbf7f", "token":"12f1ebbfd62746257dbfb66c07ce42d1240d0a0cf0d1959b5706f411edd6315d"} # type: Dict[str, str]

# Board Ids and their names
# '5a5017502c3092150d1e26e1': Workflow Management
# '5a5040eef206a59341eacd54': Testing
# '5a503f72e8f6616d36627f5e': Coding
# '5a70c638108a389f8ab0df60': Build
# '5a5346bedc0d13bc7f6c6510': Cloud
# '5a534507c990c6fd56225bb7': Deployment
# '5a85afe2db1a07af8f284db5': DevOPS Security
# '5a5344efc1d9a27718e6d066': Monitoring
# '5a526708bb22ff0c72baadc8': Security
# '5a53452c4d4dae41b7d936f8': User Interface

board_ids = ['5a5017502c3092150d1e26e1', '5a5040eef206a59341eacd54', '5a503f72e8f6616d36627f5e',
             '5a70c638108a389f8ab0df60', '5a5346bedc0d13bc7f6c6510', '5a534507c990c6fd56225bb7',
             '5a85afe2db1a07af8f284db5', '5a5344efc1d9a27718e6d066', '5a526708bb22ff0c72baadc8',
             '5a53452c4d4dae41b7d936f8'] # type: List[str]

# storing email body in message string
message = "The following cards have not been moved from past 14 days \n \n" # type: str

# reading cards of a single board using the board id

for i in range(0, len(board_ids)):

    #retrieving the name of the board using board id
    url_board_name = "https://api.trello.com/1/boards/" + board_ids[i] +"/name" # type :str
    response_board_name = requests.request("GET", url_board_name, params=querystring)
    board_name = json.loads(response_board_name.text)
    message += "Cards in "  + board_name['_value'] + ": \n" # type :str

    # retreiving cards from board using board id
    url_board_cards = "https://api.trello.com/1/boards/" + board_ids[i] +"/cards" # type :str
    response_board_cards = requests.request("GET", url_board_cards, params=querystring)
    data_board_cards = json.loads(response_board_cards.text)

    # iterating over all the board cards
    for i in range(0, len(data_board_cards)):

        # converting timestamp from ISO 8601 extended format to timestamp type of python
        card_latest_activity_timestamp = dateutil.parser.parse(data_board_cards[i]['dateLastActivity']).replace(tzinfo=None)

        # calculating the time difference between present time and card's latest activity time
        time_difference = time_now - card_latest_activity_timestamp
#         print(time_difference.seconds)
        # extracting name of list of card using the list id
        url_card_list = "https://api.trello.com/1/lists/" + data_board_cards[i]['idList'] + "/name" # type :str
        response_card_list = requests.request("GET", url_card_list, params=querystring)
        data_card_list = json.loads(response_card_list.text)
        card_list_name = data_card_list['_value']  # type: List[str]

        # finding whether card previous activity was more than or equal to days_of_inactivity_limit
        # and card is not present in wish list and done list
        if(time_difference.days >= days_of_inactivity_limit and card_list_name not in ('Wish List', 'Done')):
            message += data_board_cards[i]['name'] + " " + data_board_cards[i]['shortUrl'] + "\n" # type :str
    message += "\n" # type :str

message += "Note: Removed cards in Wish List and Done List" # type :str

# set up the SMTP server
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()

# reading login credentials from a EMAIL_INFO.txt file
# Format of EMAIL_INFO.txt file: <email_id> <password>
text_file = open("EMAIL_INFO.txt", "r")
lines = text_file.read().split(' ')
s.login(user=lines[0], password=lines[1])

to_contacts = ["dsd298@nyu.edu", "ejc369@nyu.edu"] # type :List[str]
for i in range(0, len(to_contacts)):
    msg = MIMEMultipart()       # create a message
    # message = "this is a test"
    msg['From'] = "devopsnyu@gmail.com" # type :List[str]
    msg['To'] = to_contacts[i] # type :List[str]
    msg['Subject'] = "Card Inactivity Information E-Mail" # type :List[str]

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg

# closing SMTP connection
s.quit()
