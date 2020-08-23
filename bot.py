import wikipedia
import requests
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import random
import string 
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
from flask import Flask, request_finished, request
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True) # Download the punkt package
app = Flask(__name__)
  
@app.route('/', methods=['POST'])
def transcript():
    user_text = request.json['data']
    if (user_text == "first_message"):
      print("Hello, I am Doc Bot. I will answer your queries about Corona Virus. If you want to exit, type Bye!")
    chatbot(user_text)
    return user_text

def get_text(url):    
    if ("wikipedia" in url):
        # Specify the title of the Wikipedia page
        wiki = wikipedia.page(url.strip("https://en.wikipedia.org/wiki/"))
        # Extract the plain text content of the page, excluding images, tables, and other data.
        text = wiki.content
        # Replace '==' with '' (an empty string)
        text = text.replace('==', '')
        # Replace '\n' (a new line) with '' & end the string at $1000.
        text = text.replace('\n', '')[:-12]
        return text
    else:
        html = urlopen(url).read()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

#Function to return a random greeting response to a users greeting
def greeting_response(text):
  #Convert the text to be all lowercase
  text = text.lower()
  # Keyword Matching
  #Greeting input from the user
  user_greetings = ["hi", "hello", "greetings", "what's up", "wassup", "hey"] 
  #Greeting responses back to the user from the bot
  bot_greetings = ["howdy","hi", "hey", "what's good", "hello", "hey there"]
  
  #If user's input is a greeting, return a randomly chosen greeting response
  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

#Return the indices of the values from an array in sorted order by the values
def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))
  x  = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index

# Generate the response
def bot_response(user_input, sentence_list):
    user_input = user_input.lower() #Convert the users input to all lowercase letters
    sentence_list.append(user_input) #Append the users response to the list of sentence tokens
    bot_response = '' #Create an empty response for the bot
    cm = CountVectorizer().fit_transform(sentence_list) #Create the count matrix
    similarity_scores = cosine_similarity(cm[-1], cm) #Get the similarity scores to the users input
    flatten = similarity_scores.flatten() #Reduce the dimensionality of the similarity scores
    index = index_sort(flatten) #Sort the index from 
    index = index[1:] #Get all of the similarity scores except the first (the query itself)
    response_flag=0 #Set a flag letting us know if the text contains a similarity score greater than 0.0
    #Loop the through the index list and get the 'n' number of sentences as the response
    j = 0
    for i in range(0, len(index)):
      if flatten[index[i]] > 0.1:
        bot_response = bot_response + ' ' + sentence_list[index[i]]
        response_flag = 1
        j = j+1
      if j > 2:
        break  
    #if no sentence contains a similarity score greater than 0.0 then print 'I apologize, I don't understand'
    if (response_flag == 0):
        bot_response = bot_response + ' ' + "I apologize, I don't understand."
        sentence_list.remove(user_input) #Remove the users response from the sentence tokens
       
    return bot_response

def chatbot(user_text):
    # url1 = "https://www.breakthroughbasketball.com/basics/basics.html"
    # url2 = "https://www.rulesofsport.com/sports/basketball.html"
    # url3 = "https://en.wikipedia.org/wiki/Basketball"
    # url4 = "https://www.britannica.com/sports/basketball"
    url1 = "https://www.cdc.gov/coronavirus/2019-ncov/faq.html"
    url2 = "https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html"
    url3 = "https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html"
    url4 = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/index.html"
    # url_test = 'https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521'
    # urls = [url_test]
    urls = [url1, url2, url3, url4]

    sentence_list = []
    for url in urls:
        #Tokenization
        text = get_text(url)
        sentence_list += nltk.sent_tokenize(text) # txt to a list of sentences 

    #Start the chat
    # if (first):
    #   print("Hello, I am Mr. Bot. I will answer your queries about the sport of Basketball. If you want to exit, type Bye!")
    #   first = False
    
    exit_list = ['exit', 'see you later','bye', 'quit', 'break']
    # while (True):
    #     user_input = input()
    if (user_text.lower() in exit_list):
        print("Doc Bot: Talk to you later!")
    elif (greeting_response(user_text) != None):
        print("Doc Bot: " + greeting_response(user_text))
    else:
        print("Doc Bot: " + bot_response(user_text, sentence_list))


if __name__ == "__main__":
    app.run()

