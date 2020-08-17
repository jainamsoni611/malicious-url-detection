from tkinter import *
from tkinter import messagebox
import pandas
from PIL import ImageTk, Image
import os,subprocess
import numpy as np
import re
import tensorflow as tf
from keras.preprocessing import sequence
from string import printable
from sklearn import model_selection
from keras.models import Sequential, Model, model_from_json, load_model
from pathlib import Path
import json
import warnings
warnings.filterwarnings("ignore")


root = Tk()
root.geometry('1100x600+0+0')
root.configure(background = "#001a4d")
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

im = Image.open('image.png').resize((1100,500))#width,height
#size= width,height = im.size
#im.resize((5000,128))
img = ImageTk.PhotoImage(im)
panel = Label(root, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.pack()

L1 = Label(frame, text="Enter the URL: ",fg="MidnightBlue",font = 'times 17 bold underline')# for text enter the url
L1.pack( side = LEFT)
E1 = Entry(frame,bd =35, width=180,fg="#001a4d" ,bg="AliceBlue")# for text box
#E1.insert(0, 'Enter your URL')
E1.pack(side = RIGHT)

#  load model from disk function!
def load_model(fileModelJSON,fileWeights):
    #print("Saving model to disk: ",fileModelJSON,"and",fileWeights)
    with open(fileModelJSON, 'r') as f:
         model_json = json.load(f)
         model = model_from_json(model_json)
    
    model.load_weights(fileWeights)
    return model


def print_result(proba):
    if proba > 0.5:
        return "Phish!"
    else:
        return "not a Phish!"
		
def submitCallBack():
    url=E1.get()
    url_int_tokens = [[printable.index(x) + 1 for x in url if x in printable]]
    max_len=75
    X = sequence.pad_sequences(url_int_tokens, maxlen=max_len)
    model = load_model('model_weights95.json','model_weights95.h5')
    target_proba = model.predict(X, batch_size=1)
    messagebox.showinfo( "URL Checker Result", " "+url+" is "+ print_result(target_proba[0]))      

B1 = Button(bottomframe, text ="Submit", command = submitCallBack,bg="LightSeaGreen",height=3,width=10)
B1.pack()
root.mainloop()
   