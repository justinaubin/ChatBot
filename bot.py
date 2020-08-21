import wikipedia
import random
import string 
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True) # Download the punkt package

# Specify the title of the Wikipedia page
wiki = wikipedia.page('Basketball')
# Extract the plain text content of the page, excluding images, tables, and other data.
text = wiki.content
# Replace '==' with '' (an empty string)
text = text.replace('==', '')
# Replace '\n' (a new line) with '' & end the string at $1000.
text = text.replace('\n', '')[:-12]
# print(text)

#Tokenization
sent_tokens = nltk.sent_tokenize(text) # txt to a list of sentences 
# print(sent_tokens)

#Function to return a random greeting response to a users greeting
def greeting_response(text):
  #Convert the text to be all lowercase
  text = text.lower()
  # Keyword Matching
  #Greeting responses back to the user from the bot
  bot_greetings = ["howdy","hi", "hey", "what's good", "hello", "hey there"]
  #Greeting input from the user
  user_greetings = ["hi", "hello", "greetings", "what's up", "wassup", "hey"] 
  
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
def bot_response(user_input):
    user_input = user_input.lower() #Convert the users input to all lowercase letters
    sentence_list.append(user_input) #Append the users response to the list of sentence tokens
    bot_response='' #Create an empty response for the bot
    cm = CountVectorizer().fit_transform(sentence_list) #Create the count matrix
    similarity_scores = cosine_similarity(cm[-1], cm) #Get the similarity scores to the users input
    flatten = similarity_scores.flatten() #Reduce the dimensionality of the similarity scores
    index = index_sort(flatten) #Sort the index from 
    index = index[1:] #Get all of the similarity scores except the first (the query itself)
    response_flag=0 #Set a flag letting us know if the text contains a similarity score greater than 0.0
    #Loop the through the index list and get the 'n' number of sentences as the response
    j = 0
    for i in range(0, len(index)):
      if flatten[index[i]] > 0.0:
        bot_response = bot_response+' '+sentence_list[index[i]]
        response_flag = 1
        j = j+1
      if j > 2:
        break  
    #if no sentence contains a similarity score greater than 0.0 then print 'I apologize, I don't understand'
    if(response_flag==0):
        bot_response = bot_response+' '+"I apologize, I don't understand."
sentence_list.remove(user_input) #Remove the users response from the sentence tokens
       
    return bot_response
