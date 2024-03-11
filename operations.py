import pandas as pd
import numpy as np
import os

transactions = os.path.join('env','transactions.csv')

df= pd.DataFrame(pd.read_csv(transactions))

print(df.head())