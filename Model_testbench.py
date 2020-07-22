#!/usr/bin/env python
# coding: utf-8

# In[21]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[22]:


dataset = pd.read_csv("test.csv")
y=dataset.iloc[:,-1]
X=df = dataset.iloc[:,:-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)


# In[45]:


clf = LogisticRegression(random_state=0, penalty='l2').fit(X_train, y_train)


# In[46]:


#baseline model
clf.score(X_test, y_test)


# In[ ]:





# In[ ]:




