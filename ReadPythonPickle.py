#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os
os.chdir("C:/Users/yche465/Desktop/CS570/Project")

import pandas as pd
def read_pickle_file(file):
    pickle_data = pd.read_pickle(file)
    return pickle_data

