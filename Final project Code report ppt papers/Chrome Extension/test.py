import pandas
from PIL import ImageTk, Image
import os
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
import sys

def main():
    url = sys.argv[1]

    def load_model(fileModelJSON,fileWeights):
        with open(fileModelJSON, 'r') as f:
            model_json = json.load(f)
            model = model_from_json(model_json)
        model.load_weights(fileWeights)
        return model

    def print_result(proba):
        if proba > 0.5:
            return "False"
        else:
            return "True"

    url_int_tokens = [[printable.index(x) + 1 for x in url if x in printable]]
    max_len=75
    X = sequence.pad_sequences(url_int_tokens, maxlen=max_len)
    model = load_model("C:\\xampp\\htdocs\\1\\model_weights95.json","C:\\xampp\\htdocs\\1\\model_weights95.h5")
    target_proba = model.predict(X, batch_size=1)
    
    from datetime import datetime
    from datetime import timedelta
    import requests
    import base64
    class PhishTankError(Exception):
        pass
    class Result():
        def __init__(self, response):
            self.url = response.get('url', None)
            self.in_database = response.get('in_database', None)
            self.phish_id = response.get('phish_id', None)
            self.phish_detail_page = response.get('phish_detail_page', None)
            self.verified = response.get('verified', None)
            self.valid = response.get('valid', None)
            
        def __phish(self):
            if self.valid:
                return True
            return False
        
    class PhishTank():
        __apikey = 'c2450ce424e2ad46756de2e9f0d6572e4053d119661baa48679e547006ba5662'

        def __init__(self, api_url='http://checkurl.phishtank.com/checkurl/', apikey='c2450ce424e2ad46756de2e9f0d6572e4053d119661baa48679e547006ba5662'):
            self.__apikey = apikey
            self._api_url = api_url
            
        def check(self, url):
            post_data = {
                'url': base64.b64encode(url.encode("utf-8")),
                'format': 'json',
                'app_key': self.__apikey,
            }
            response = requests.post(self._api_url, data=post_data)
            data = response.json()

            if 'errortext' in data.keys():
                raise PhishTankError(data['errortext'])
            return Result(data['results'])
            
    p = PhishTank()
    result =p.check(url)
    if (result.valid=="True" and print_result(target_proba[0])=="False"):
        print("Malicious")
    else:
        if result.valid:
            print("Malicious")
        else:
            print("SAFE")
    
    
    print_result(target_proba[0])

if __name__ == "__main__":
    main()
