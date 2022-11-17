import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('chatbot_data_from_firebase.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability' : str(r[1])})

    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


print("The CathAI Chatbot is now running!")


def get_user_input_from_user_input_from_firebase():
    user_input_from_firebase = json.loads(open('user_input_from_firebase').read())
    user_input = list(user_input_from_firebase.values())
    print('User input inside chatbot: ', str(user_input))
    return user_input


def init_chatbot_get_response(user_input):
    message = str(user_input)
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("CathAI in chatbot:",res)

    chatbot_response = json.dumps(res)
    chatbot_response_to_json = open('chatbot_response.json', 'w')
    print("chatbot_response_to_json_in_chatbot", chatbot_response)
    chatbot_response_to_json.write(chatbot_response)
    chatbot_response_to_json.close()



print('Here is chatbot.py! \n')

def init():
    user_input = get_user_input_from_user_input_from_firebase()
    init_chatbot_get_response(user_input)

