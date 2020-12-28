#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.naive_bayes import *
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


# In[32]:


df = pd.read_csv('bank-full.csv')


# In[33]:


for index, row in df.iterrows():
    if row['balance'] < 0:
        row['balance'] = 'inDebt'
    else:
        row['balance'] = 'notInDebt'

df.loc[( df['balance'] >= 10000), 'balanceSummary'] = 'veryPositive' 
df.loc[( (df['balance'] < 0) & (df['balance'] >= -10000)), 'balanceSummary'] = 'negative' 
df.loc[( (df['balance'] < 10000) & (df['balance'] >= 0)), 'balanceSummary'] = 'positive' 
df.loc[df['balance'] < -500, 'balanceSummary'] = 'veryNegative' 


df.loc[( (df['age'] < 25) & (df['age'] >= 0)),  'ageBand'] = 'ageBand1' 
df.loc[( (df['age'] < 30) & (df['age'] >= 25)), 'ageBand'] = 'ageBand2' 
df.loc[( (df['age'] < 40) & (df['age'] >= 30)), 'ageBand'] = 'ageBand3' 
df.loc[( (df['age'] < 50) & (df['age'] >= 40)), 'ageBand'] = 'ageBand4' 
df.loc[( (df['age'] < 120) & (df['age'] >= 50)),'ageBand'] = 'ageBand5' 

df.loc[ (df['default'] == 'no'), 'defaultValue'] = 'defaultNo' 
df.loc[ (df['default'] == 'yes'), 'defaultValue'] = 'defaultYes' 
df.loc[ (df['housing'] == 'no'), 'housingVal'] = 'houseNo' 
df.loc[ (df['housing'] == 'yes'), 'housingVal'] = 'houseYes' 
df.loc[ (df['loan'] == 'no'), 'loanVal'] = 'loanNo' 
df.loc[ (df['loan'] == 'yes'), 'loanVal'] = 'loanYes' 


# In[58]:


assData = df[['marital','education','y','balanceSummary','ageBand','defaultValue','housingVal','loanVal']]


# In[59]:


assData


# In[60]:


assData = assData.values


# In[61]:


bank_te = TransactionEncoder()
bank_te_ary = bank_te.fit(assData).transform(assData)


# In[62]:


bank_ass_df = pd.DataFrame(bank_te_ary,columns=bank_te.columns_)


# In[63]:


bankFreq = apriori(bank_ass_df, min_support=0.1,use_colnames=True)


# In[64]:


bankRules = association_rules(bankFreq, metric='confidence',min_threshold=0.3)
bankRules.columns = [ 'antecedents', 'consequents', 'antsup', 'consup', 'support', 'confidence', 'lift', 'leverage', 'conviction']


# In[65]:


rules_sorted = bankRules.iloc[bankRules['lift'].sort_values(ascending=False).index][['antecedents','consequents','support','confidence','lift']]


# In[66]:


rules_sorted.head(20)


# In[ ]:




