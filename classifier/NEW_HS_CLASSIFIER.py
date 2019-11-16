from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
#from sklearn.model_selection import cross_validate
#import seaborn as sns
#import matplotlib.pyplot as plt
import spacy
import pandas as pd
import pickle
import os

from sqlalchemy import create_engine


dictionary_race = {
'shifty'
'shifty Jew'
'coon'
'wet back'
}

dictionary_misog = {
'cunt'
'bitch'
'whore'
'slut'
'woman driver'
}

dictionary_transph = {
'not a real woman'
'not a real man'
'tranny'
'trannie'
}

db_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')


engine = create_engine('sqlite:///'+db_file)

df = pd.read_sql_table("classifier_sub", engine)
#print(df)

nlp = spacy.load('en_core_web_sm', disable=['parser'])

preprocessing = {
'remove_quotes': True,
'replace_curly_quotes': True,
'strip_punctuation': True,
'POS': ['ADJ', 'ADV', 'INTJ', 'NOUN', 'VERB'],
'lowercase': True,
'letters_only': True,
'min_occurrences': 10,
'max_ngram': 2,
}

class Feature_model:
    def __init__(self):
        self.vectorizer = CountVectorizer(analyzer=self.preprocess)
        self.preprocessing = {
        'remove_quotes': True,
        'replace_curly_quotes': True,
        'strip_punctuation': True,
        'POS': ['ADJ', 'ADV', 'INTJ', 'NOUN', 'VERB'],
        'lowercase': True,
        'letters_only': True,
        'min_occurrences': 10,
        'max_ngram': 2,
        }
                    
        self.clfrNB = MultinomialNB()
        # Create pipeline
        self.pipe = Pipeline([('vectorize', self.vectorizer),
        ('classify', self.clfrNB)])
       

    def preprocess(self, text):
        features = []
        previous_lemma = False
        for token in nlp(text):
            valid_pos = token.pos_ in self.preprocessing['POS']
            lemma = token.lemma_
            valid_word = lemma
            if valid_pos and valid_word and (lemma.isalpha() or not self.preprocessing['letters_only']):
                if self.preprocessing['lowercase']:
                    lemma = lemma.lower()
                features.append(lemma)
                if previous_lemma:
                    features.append(' '.join([previous_lemma, lemma]))
                previous_lemma = lemma
            else:
                previous_lemma = False
        return features
    
    def fit(self, filename):
        df = pd.read_sql_table("classifier_sub", engine)
        self.pipe.fit(df.content, df.label)
        with open(filename, mode='wb') as f:
            pickle.dump(self, f)
#        predicted_train = pipe.predict(x_train)
#        predicted_test = pipe.predict(x_test)
#        score = pipe.score(x_test, y_test)
        
    def predict(self, text):
        return self.pipe.predict([text])[0]





## Extracting features using either a Count or TFIDF vectorizer
#vectorizer = CountVectorizer(analyzer=copy.copy(preprocess))
#
#            
#clfrNB = MultinomialNB()
## Create pipeline
#pipe = Pipeline([('vectorize', vectorizer),
#('classify', clfrNB)])
#pipe.fit(x_train, y_train)
#predicted_train = pipe.predict(x_train)
#predicted_test = pipe.predict(x_test)
#score = pipe.score(x_test, y_test)
#print("accuracy score is", score)






# Obtain and print most informative features (top 20 hyper-partisan, top 20 mainstream)
#def show_most_informative_features(vectorizer, clf, n=20):
#    feature_names = vectorizer.get_feature_names()
#    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
#    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
#    for (coef_1, fn_1), (coef_2, fn_2) in top:
#        print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
#        print('The number of features is', len(feature_names))

# Run test article (not from dataset) through pipeline


#trial_text = open("RACE.txt", encoding='utf-8').read()
#print(pipe.predict([trial_text]))

#def predict_class(sentence):
#    pred_class = pipe.predict(sentence)
#    return pred_class
#    words = sentence.lower().split()
#    if dict[i]((w, True) for w in words):
    