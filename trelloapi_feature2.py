import requests
import json
import dateutil.parser
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# extracting the present time
time_now = datetime.datetime.utcnow()

# setting a days of inactivity limit: 1 hour
seconds_of_inactivity_limit = 3600

# trying to read all the boards where I am a member
url_member = "https://api.trello.com/1/members/dsd2981"
querystring = {"key":"b282952c1211b7eb3c16b7c3adfbbf7f","token":"12f1ebbfd62746257dbfb66c07ce42d1240d0a0cf0d1959b5706f411edd6315d"}
response_member = requests.request("GET", url_member, params=querystring)


# converting the html object to a json object for easy convenience of handling the object
data_member = json.loads(response_member.text)

# removing the first 2 boards as they are my personal boards
board_ids = data_member['idBoards'][2:]

message = "The following cards have been pushed in testing phase just an hour ago! \n"
for i in range(0, len(board_ids)):

    #retrieving the name of the board using board id
    url_board_name = "https://api.trello.com/1/boards/" + board_ids[i] +"/name"
    response_board_name = requests.request("GET", url_board_name, params=querystring)
    board_name = json.loads(response_board_name.text)
    message += "Cards in "  + board_name['_value'] + ": \n"

    # retreiving cards from board using board id
    url_board_cards = "https://api.trello.com/1/boards/" + board_ids[i] +"/cards"
    response_board_cards = requests.request("GET", url_board_cards, params=querystring)
    data_board_cards = json.loads(response_board_cards.text)

    # iterating over all the board cards
    for i in range(0, len(data_board_cards)):

        # converting timestamp from ISO 8601 extended format to timestamp type of python
        card_latest_activity_timestamp = dateutil.parser.parse(data_board_cards[i]['dateLastActivity']).replace(tzinfo=None)

        # calculating the time difference between present time and card's latest activity time
        time_difference = time_now - card_latest_activity_timestamp

        # extracting name of list of card using the list id
        url_card_list = "https://api.trello.com/1/lists/" + data_board_cards[i]['idList'] + "/name"
        response_card_list = requests.request("GET", url_card_list, params=querystring)
        data_card_list = json.loads(response_card_list.text)
        card_list_name = data_card_list['_value']

        # finding whether card previous activity was more than or equal to seconds_of_inactivity_limit
        # and card is present in Testing list
        if(time_difference.seconds <= seconds_of_inactivity_limit and card_list_name in ('Testing', 'testing')):
            message += data_board_cards[i]['name'] + " " + data_board_cards[i]['shortUrl'] +"\n"
    message += "\n"


# set up the SMTP server
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(user="devopsnyu@gmail.com", password="***********")

to_contacts = ["dsd298@nyu.edu", "ejc369@nyu.edu"]
for i in range(0, len(to_contacts)):
    msg = MIMEMultipart()       # create a message
    # message = "this is a test"
    msg['From'] = "devopsnyu@gmail.com"
    msg['To'] = to_contacts[i]
    msg['Subject'] = "Card Inactivity Information E-Mail"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg
s.quit()
