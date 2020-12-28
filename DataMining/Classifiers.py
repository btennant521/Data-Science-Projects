#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.naive_bayes import *


# In[13]:


df = pd.read_csv('bank-full.csv')


# In[14]:


df['job'] = df['job'].astype('category')
df['job'] = df['job'].cat.codes
df['marital'] = df['marital'].astype('category')
df['marital'] = df['marital'].cat.codes
df['education'] = df['education'].astype('category')
df['education'] = df['education'].cat.codes
df['default'] = df['default'].astype('category')
df['default'] = df['default'].cat.codes
df['contact'] = df['contact'].astype('category')
df['contact'] = df['contact'].cat.codes
df['month'] = df['month'].astype('category')
df['month'] = df['month'].cat.codes
df['poutcome'] = df['poutcome'].astype('category')
df['poutcome'] = df['poutcome'].cat.codes
df['housing'] = df['housing'].astype('category')
df['housing'] = df['housing'].cat.codes
df['loan'] = df['loan'].astype('category')
df['loan'] = df['loan'].cat.codes
df['y'] = df['y'].astype('category')
df['y'] = df['y'].cat.codes

df = df.drop('pdays',axis=1)
df['balance'] = (df['balance'] - df['balance'].min()) / ( df['balance'].max() - df['balance'].min() )

Y = df['y']
df = df.drop('y',axis=1)
X = df


# In[22]:


X.head()


# In[19]:


x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.25)


# In[25]:


from sklearn.decomposition import PCA
tree_acc = []
for i in range(1,15):
    pca = PCA(n_components=i)
    x_train_pca = pca.fit_transform(x_train)
    x_test_pca = pca.transform(x_test)
    a_tree = tree.DecisionTreeClassifier(criterion='gini',max_depth=50,random_state=1)
    a_tree.fit(x_train_pca,y_train)
    pred = a_tree.predict(x_test_pca)
    tree_acc.append(accuracy_score(y_test,pred))


# In[37]:


import matplotlib.pyplot as plt
plt.scatter([i for i in range(1,15)],tree_acc)
plt.xlabel('Number of components derived from PCA')
plt.ylabel('Model Accuracy')
plt.title('Decision Tree PCA')
plt.show()


# In[35]:


from sklearn.inspection import permutation_importance
tree_model = tree.DecisionTreeClassifier(criterion='gini',max_depth=50,random_state=1)
tree_model.fit(x_train,y_train)
importance = tree_model.feature_importances_
for i,v in enumerate(importance):
    print('Feature: %0d, FName: %15s, Score: %.5f' % (i,df.columns[i], v) )


# PCA determined that 12 components produce the most accurate model. Based on the feature importances of the tree model fit on all components I would elect to drop 'default', 'loan' and 'contact' from the model. Default has the lowest feature importance so that is dropped for sure. 'Contact' appears to be the method used to contact the customer so I am not surprised that it is not very useful. The 'loan' however is surprising because I would imagine that a loan on the account would have a considerable effect on the predictive ability of the model. However, the model shows that 'loan' has very little importance to the model so I would still drop it.

# In[36]:


nb_acc = []
for i in range(1,15):
    pca = PCA(n_components=i)
    x_train_pca = pca.fit_transform(x_train)
    x_test_pca = pca.transform(x_test)
    model = GaussianNB()
    model.fit(x_train_pca,y_train)
    pred = model.predict(x_test_pca)
    nb_acc.append(accuracy_score(y_test,pred))


# In[38]:


import matplotlib.pyplot as plt
plt.scatter([i for i in range(1,15)],nb_acc)
plt.xlabel('Number of components derived from PCA')
plt.ylabel('Model Accuracy')
plt.title('Naive-Bayes PCA')
plt.show()


# In[40]:


nb_full = GaussianNB()
nb_full.fit(x_train,y_train)
nb_pred = nb_full.predict(x_test)
nb_imps = permutation_importance(nb_full,x_test,y_test)
print(imps.importances_mean)


# In[41]:


X.columns[[8,10,11,13]]


# The PCA on the Naive-Bayes model is drastically different than that of the decision tree's. Mainly, the most accurate Naive-Bayes model has only 4 components. What's more strange is what those components are. It seems to find a lot of importance on timing and communication with the customer. 'Contact' is jsut the method of communication used to reach the customer, 'month' is the last month that the customer was contacted (I think), 'duration' is how long in seconds the communication with the customer went on and 'previous' is the number of times the customer had been contacted before the current campaign. This is interesting because 'contact' was one of the components we removed from the decision tree model, however it is one of the most significant component in the Naive-Bayes. Based on this analysis, I would conclude that the Naive-Bayes classifier would be the better model for this dataset. For every iteration of the PCA, its accuracy was higher than the decision tree's and the optimal Naive-Bayes model only used 4 components rather than 12 and the Naive-Bayes still had a better accuracy. I can also conclude that communication is very important to predicting the outcome for this dataset based on the most significant components of the NB. This can be very valuable information to a marketing team.
