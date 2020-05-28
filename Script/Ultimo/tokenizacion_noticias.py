import spacy
from spacy import displacy
from collections import Counter
import es_core_news_sm
nlp = es_core_news_sm.load()

doc = nlp('La vecina de Bogotá decidió en las urnas por mayorías legítimas basar nuestro sistema de transporte masivo en Metro y no en el negocio de intereses privados de Transmilenio.')
print([(X.text, X.label_) for X in doc.ents])