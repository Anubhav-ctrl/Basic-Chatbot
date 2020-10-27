from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#Download the punkt package
nltk.download('punkt',quiet=True)

#Get the article
article=Article("https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521")
article.download()
article.parse()
article.nlp()
corpus=article.text
#print(corpus)

#Tokenization
text=corpus
sentence_list=nltk.sent_tokenize(text) #A list of sentences
#print(sentence_list)

#A function to return a random greeting response to ausers greeting
def greeting_response(text):
    text=text.lower()

    #Bots greeting response
    bot_greetings=["Howdy..","Hi..","Hay..","Hola..","Hello.."]
    #Users greeting
    user_greetings=["hi","hii..","hi..","hello..","hey","hola","hello","greetings","wassup"]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index

# create the bots response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ""
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag= 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response + " " + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + " " +"I apolize, I don't understand."
    sentence_list.remove(user_input)
    return bot_response

# start the chat
print("Doc Bot: I am doctor bot i will solve the queries of a asked question by your side.")
exit_list=["exit","see u later","bii","bye","quit","break"]


while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print("Take care! See u later.")
        break
    else:
        if greeting_response(user_input)!=None:
            print("Doc Bot: "+greeting_response(user_input))
        else:
            print("Doc Bot:"+bot_response(user_input))