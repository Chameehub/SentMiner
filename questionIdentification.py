import nltk
import json
from nltk.corpus import movie_reviews

with open('QA_Grocery_and_Gourmet_Food.json','r') as json_data:
    d = json.load(json_data)
    json_dump = json.dump(d)
    print(json_dump)