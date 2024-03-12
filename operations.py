import pandas as pd
import numpy as np
import os

transactions = os.path.join('env','transactions.csv')

df= pd.DataFrame(pd.read_csv(transactions))
print(df.columns)

debitRecords = df[df['Debit Amount       ']==0.00] 
creditRecords = df[df['Debit Amount       ']==0.00]

print(creditRecords, debitRecords)