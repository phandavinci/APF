import pandas as pd
import numpy as np
import os

transactions = os.path.join('env','transactions.csv')

df = pd.read_csv(transactions)

df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.to_csv(transactions, index=False)

def split_narration(narration):
    parts = narration.split('-')
    if len(parts) > 6:
        parts[2]+='-'+parts.pop(3)
    return parts


df[['Type', 'Name', 'ID', 'BankID', 'RefNo.', 'Comments']] = df['Narration'].apply(lambda x: pd.Series(split_narration(x)))



df = df.drop(columns=['Narration', 'RefNo.'])

df.to_csv(transactions, index=False)

print("CSV file updated successfully.")

debitRecords = df[df['Debit Amount']==0.00] 
creditRecords = df[df['Debit Amount']==0.00]

print(creditRecords, debitRecords)