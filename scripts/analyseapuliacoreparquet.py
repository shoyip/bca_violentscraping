# -*- coding: utf-8 -*-
"""AnalyseApuliacoreParquet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S4-_bTCgWAcx2jVDmfGTzMaDpCfi25ck
"""

import pandas as pd

df = pd.read_parquet('/content/bca_apuliacore.parquet')

def is_summary(s):
  if s.startswith('Eventi di oggi'):
    return True
  else:
    return False

df['is_summary'] = df.Content.apply(is_summary)

def data_from_desc(s):
  try:
    title = s.split('📅')[0].split(']')[0][1:]
  except:
    title = None

  try:
    dates = s.split('📅')[1].split('📍')[0][:-1]
  except:
    dates = None

  try:
    place = s.split('📅')[1].split('📍')[1].split(']')[0]
  except:
    place = None

  try:
    description = ''.join(''.join(s.split('📍')[1:]).split(')')[1:])[1:]
  except:
    description = None

  return title, dates, place, description

#[['title', 'dates', 'place', 'description']]
new_df = pd.DataFrame(df.query("is_summary == False").Content.apply(data_from_desc).tolist(), columns=['title', 'dates', 'place', 'description'])

new_df.to_csv('bca_apuliacore.csv')