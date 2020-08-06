#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import pandas as pd


# # Experiment Objective

# The dataset I chose to use consists of tweets from a twitter user directed at an airline. I downloaded the archive file from kaggle, website for Data Scientist to share and play with different data science practices; it is open-source. There are many columns including locations and name of the twitter user that I am excluding to avoid any racial bias that could come from those. I will only be using the columns containing the review text and the sentiment of the review. I will use the actual tweets and a known sentiment -  positive or negative - to create a classification model to classify future tweets. Some tweets have a neutral sentiment but I will exclude those to improve the accuracy of positive and negative classifications.

# # Data Collection

# The data can be downloaded from kaggle in a csv format so I just have to read it into memory as a dataframe with pandas. (https://www.kaggle.com/crowdflower/twitter-airline-sentiment) 

# In[32]:


dat = pd.read_csv('Tweets.csv')


# # Data Preprocessing

# Pull the columns we need from the full dataframe. We only need the text reviews and the sentiment.

# In[33]:


tweets = pd.DataFrame({'label':dat['airline_sentiment'],'tweet':dat['text']})
tweets.head()


# Remove any tweets that have a neutral sentiment and encode the positive/negative sentiments as 1 or 0.

# In[34]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
tweets = tweets[tweets['label'] != 'neutral']
tweets['label'] = le.fit_transform(tweets['label'])

tweets = pd.DataFrame({'tweet':tweets['tweet'], 'label':tweets['label']})


# Reset index to start at 0

# In[35]:


tweets = tweets.reset_index(drop=True)


# Write out csv with neutral reviews removed so I can read it back in later.

# In[36]:


tweets.to_csv('tweets_clean.csv',index=False)


# Below is my initial, sub-optimal SGD Logistic Regression classifier using out-of-core learning. 

# In[37]:


import numpy as np
import re
from nltk.corpus import stopwords

stop = stopwords.words('english')


def tokenizer(text):
    text = re.sub('.<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) +        ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


def stream_docs(path):
    with open(path, 'r', encoding='utf-8') as csv:
        next(csv)  # skip header
        for line in csv:
            if len(line) < 10:
                continue
            text = line[:-3]
            label =  line[-2]
            if not label.isnumeric() or label not in ['1','0']:
                continue
            yield text, int(label)


# In[38]:


def get_minibatch(doc_stream, size):
    docs, y = [], []
    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None
    return docs, y


# In[39]:


from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier


vect = HashingVectorizer(decode_error='ignore', 
                         n_features=2**21,
                         preprocessor=None, 
                         tokenizer=tokenizer_porter)


# In[40]:


from distutils.version import LooseVersion as Version
from sklearn import __version__ as sklearn_version

clf = SGDClassifier(loss='log', random_state=1,penalty='l2',alpha = 1/1.0)


doc_stream = stream_docs(path='tweets_clean.csv')


# In[42]:


import pyprind
pbar = pyprind.ProgBar(18)

classes = np.array([0,1])
for _ in range(18):
    X_train, y_train = get_minibatch(doc_stream, size=500)
    if not X_train:
        break
    X_train = vect.transform(X_train)
    clf.partial_fit(X_train, y_train, classes=classes)
    pbar.update()


# In[43]:


X_test, y_test = get_minibatch(doc_stream, size=1000)
X_test = vect.transform(X_test)
print('Accuracy: %.3f' % clf.score(X_test, y_test))


# The inital model doesn't perform particularly well on the test set. 

# ### Anything below here was for testing

# In[60]:


import re
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           text)
    text = (re.sub('[\W]+', ' ', text.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return text


# In[61]:


tweets['tweet'] = tweets['tweet'].apply(preprocessor)


# Word stemming

# In[62]:


from nltk.stem.porter import PorterStemmer

porter = PorterStemmer()

def tokenizer(text):
    return text.split()


def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]


# In[17]:


tweets['tweet'] = tweets['tweet'].apply(tokenizer_porter)


# In[39]:


tweets.head()


# Stop-word removal

# In[63]:


import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

stop = stopwords.words('english')

def remove_stop_words(words):
    return [w for w in words if w not in stop]


# In[20]:


tweets['tweet'] = tweets['tweet'].apply(remove_stop_words)
tweets.head()


# Train-test split

# In[21]:


len(tweets)


# After removing neutral rows we have 11541 rows. I will use 9000 rows in my training set and the remaining 2541 as my test set.

# In[64]:


X_train = tweets.loc[:9000,'tweet']
y_train = tweets.loc[:9000,'label']
X_test = tweets.loc[9000:,'tweet']
y_test = tweets.loc[9000:,'label']


# # Model Optimization and Serialization

# In[49]:


from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


# Grid search for SGD Logistic Regression. 

# In[65]:


tfidf = TfidfVectorizer(strip_accents=None,
                       lowercase=False,
                       preprocessor=None)

param_grid = [{'vect__stop_words': [stop, None],
               'vect__tokenizer': [tokenizer, tokenizer_porter],
               'clf__penalty': ['l1', 'l2'],
               'clf__alpha': [0.0001, 0.01, 1.0, 10.0, 100.0, 1000.0]}]

lr_tfidf = Pipeline([('vect',tfidf),('clf',SGDClassifier(loss='log'))])

gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring='accuracy',n_jobs=1)

gs_lr_tfidf.fit(X_train,y_train)


# Below are the optimal hyperparameter for my SGD Logistic Regression classifier.

# In[66]:


print('Best parameter set: %s' % gs_lr_tfidf.best_params_)


# Below is my serialization of my SGD LR classifier.

# In[67]:


from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier


vect = HashingVectorizer(decode_error='ignore', 
                         n_features=2**21,
                         preprocessor=None, 
                         tokenizer=tokenizer_porter)


# In[68]:


from distutils.version import LooseVersion as Version
from sklearn import __version__ as sklearn_version

clf = SGDClassifier(loss='log', random_state=1,penalty='l2',alpha = 0.0001)


doc_stream = stream_docs(path='tweets_clean.csv')


# In[69]:


import pyprind
pbar = pyprind.ProgBar(18)

classes = np.array([0,1])
for _ in range(18):
    X_train, y_train = get_minibatch(doc_stream, size=500)
    if not X_train:
        break
    X_train = vect.transform(X_train)
    clf.partial_fit(X_train, y_train, classes=classes)
    pbar.update()


# Check how the classifier generalizes. As we can see the different parameters have a significant affect of the models accuracy on the test set.

# In[70]:


X_test, y_test = get_minibatch(doc_stream, size=1000)
X_test = vect.transform(X_test)
print('Accuracy: %.3f' % clf.score(X_test, y_test))


# Train the classifier on the remaining testing data.

# In[ ]:


clf.partial_fit(X_test,y_test,classes=classes)


# Create directories for my pickled objects

# In[71]:


import pickle
import os

dest = os.path.join('movieclassifier', 'pkl_objects')
if not os.path.exists(dest):
    os.makedirs(dest)

pickle.dump(stop, open(os.path.join(dest, 'stopwords.pkl'), 'wb'), protocol=4)   
pickle.dump(clf, open(os.path.join(dest, 'classifier.pkl'), 'wb'), protocol=4)


# Write the vectorizer.py file out.

# In[73]:


get_ipython().run_cell_magic('writefile', 'movieclassifier/vectorizer.py', "from sklearn.feature_extraction.text import HashingVectorizer\nimport re\nimport os\nimport pickle\n\ncur_dir = os.path.dirname(__file__)\nstop = pickle.load(open(\n                os.path.join(cur_dir, \n                'pkl_objects', \n                'stopwords.pkl'), 'rb'))\n\ndef tokenizer(text):\n    text = re.sub('<[^>]*>', '', text)\n    emoticons = re.findall('(?::|;|=)(?:-)?(?:\\)|\\(|D|P)',\n                           text.lower())\n    text = re.sub('[\\W]+', ' ', text.lower()) \\\n                   + ' '.join(emoticons).replace('-', '')\n    tokenized = [w for w in text.split() if w not in stop]\n    return tokenized\n\nvect = HashingVectorizer(decode_error='ignore',\n                         n_features=2**21,\n                         preprocessor=None,\n                         tokenizer=tokenizer_porter)")


# # Website Creation and Publishing

# Create the SQLite database and create the table for 

# In[79]:


import sqlite3
import os

conn = sqlite3.connect('reviews.sqlite')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS review_db')
c.execute('CREATE TABLE review_db'         '(review TEXT, sentiment INTEGER, date TEXT)')

conn.close()


# ### Website link

# In[ ]:


http://bentennant.pythonanywhere.com/

