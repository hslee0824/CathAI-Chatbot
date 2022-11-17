# Imports
import pyrebase 
import json
import time

config = {
    "apiKey" : "AIzaSyBYNH3Wsmt50QZZ09Goa8qosoa3AUFerQk",
    "authDomain" : "connectingfirebasedbtopy-a2562.firebaseapp.com",
    "projectId" : "connectingfirebasedbtopy-a2562",
    "databaseURL":"https://connectingfirebasedbtopy-a2562-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket" : "connectingfirebasedbtopy-a2562.appspot.com",
    "messagingSenderId" : "738803069313",
    "appId" : "1:738803069313:web:fbc180ffd0a6ea9ad7b880",
    "measurementId" : "G-74DZQV73MX"
}


def init_chatbot_get_user_input():

    # Initialize database
    print('\n+----------------------------+')
    print("Initializing database...")
    print('+----------------------------+\n')
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()

    # #------------------------------------------------------------------------------------------
    # Create Data with local file

    # intents.json 파일 없을 때 생각해야함 ***
    chatbot_data_feed = json.loads(open('intents.json').read())
    database.child("chatbot_data_feeded").set(chatbot_data_feed)

    # -------------------------------------------------------------------------------------------
    # add user's input manually
    # user_input = {
    #     "User" : "What is your name?"
    # }
    # database.child('user_input').set(user_input)
    #-------------------------------------------------------------------------------------------
    
    # Read Data from firebase
    print('\n+----------------------------+')
    print("Reading chatbot data...")
    print('+----------------------------+\n')

    chatbot_data_from_firebase = database.child("chatbot_data_feeded").get()
    chatbot_data_from_firebase_string = json.dumps(chatbot_data_from_firebase.val(), indent=4)
    chatbot_data_from_firebase_string_to_json = open('chatbot_data_from_firebase.json', 'w')
    chatbot_data_from_firebase_string_to_json.write(chatbot_data_from_firebase_string)
    chatbot_data_from_firebase_string_to_json.close()

    print('+--------------------------+')
    print("Readding user input...")
    print('+--------------------------+\n')
 
    user_input_from_firebase = database.child('user_input').get()
    print(dict(user_input_from_firebase.val()))
    len_of_user_input_from_firebase = len(str(dict(user_input_from_firebase.val())))

    # user_input_check = json.loads(open('user_input_from_firebase').read())
    # len_of_user_input_from_json = len(str(user_input_check))

    # if len_of_user_input_from_firebase == len_of_user_input_from_json:
    #     print('inputs are same')
    #     pass
    # print(len(str(dict(user_input_check.val()))))
    # print(user_input_check)
    # print(user_input_to_json)

    # print(len(user_input_to_json))
    # dict_user_input = dict(user_input_from_firebase.val())
    # user_input_list = list(dict_user_input.values())

    print('+----------------------------------------+')
    print("Successully downloaded data from firebase!")
    print('+----------------------------------------+\n')

    # save user's input
    user_input_to_json = json.dumps(user_input_from_firebase.val())
    print("user_input_to_json_in_firebase", user_input_to_json)
    user_input_to_json_file = open('user_input_from_firebase', 'w')
    user_input_to_json_file.write(user_input_to_json)
    user_input_to_json_file.close()

    return user_input_to_json_file


def init_training_chatbot():
    print('+---------------------------+')
    print("initializiing training.py...")
    print('+---------------------------+\n')
    import training
    training.init()

    print('+---------------------------+')
    print("initializiing chatbot.py...")
    print('+---------------------------+\n')
    import chatbot
    chatbot.init()
    print("DONE")
    

def get_chatbot_response_from_chatbot_response():
    chatbot_response = json.loads(open('chatbot_response.json').read())
    print("Chatbot Response:", chatbot_response)
    return chatbot_response
    

def send_chatbot_response_to_firebase(chatbot_response):
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    chatbot_responses = {
        "CathAI" : chatbot_response
    }
    database.child('chatbot_responses').set(chatbot_responses)


if __name__ == "__main__":

    for x in range(2):
        input_from_user = init_chatbot_get_user_input()
        init_training_chatbot()
        chatbot_response = get_chatbot_response_from_chatbot_response()
        send_chatbot_response_to_firebase(chatbot_response)
        time.sleep(10)
