import pandas as pd
import numpy as np
import os

transactions = os.path.join('env','transactions.csv')

cleanedTransactions = os.path.join('env', 'cleanedTransactions.csv')

df = pd.read_csv(transactions)

df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.to_csv(transactions, index=False)
#splitting the narration
def split_narration(narration):
    parts = narration.split('-')
    if parts[0]=='A2AINT01':
        return [parts[0], parts[1], None, None, None, parts[-1]]
    if parts[0]=='NWD':
        return [parts[0], parts[2], None, parts[1], None, 'ATM']
    if len(parts) > 6:
        parts[2]+='-'+parts.pop(3)
    return parts
#splitting the comments
def split_comment(row):
    #xxyy&comment
    #xx - priority - n, w, d
    #yy - types - s, l, b, o, c, m, i
    ## f(last km)lbl(petrollitres) - fuel
    comment = row['Comments']
    dic = {'s':"Split", 'l': 'Lend', 'b': 'Borrow', 'o': 'Others', 'c': 'Credited', 'm': 'Myself', 'h':'Holdings', 'n':'Need', 'w':'Want', 'd':'Desire'}
    s = [i for i in comment.strip().lower().split('lbl') if i]
    if len(s)==0: return [None]*3
    if len(s)!=2 or s[0][0] not in dic : return ([None]*2)+[comment]
    try:
        if len(s[0])==1: parts = [s[0], 'm', s[1]]
        else: parts = [s[0][0], s[0][1:],s[1]]
        if parts[0]=='f':
            parts[1] = parts[1]+'ltr(s)'
            parts[2] = 'LK: '+parts[2]
            return parts
        if parts[1][0]=='s':
            div = int(parts[1][1])
            row['Debit Amount'] /= div
        parts = [dic[parts[0]], dic[parts[1]] if parts[1][0]!='s' else dic[parts[1][0]]+'-'+parts[1][1], parts[2]]
        parts = [i.capitalize() for i in parts]
    except Exception as e:
        print(e)
        return ([None]*2)+[comment]
    return [row['Debit Amount']]+parts




df[['TransferType', 'Name', 'ID', 'BankID', 'RefNo.', 'Comments']] = df['Narration'].apply(lambda x: pd.Series(split_narration(x)))

df[['Debit Amount', 'Priority', 'TypeOfPayment', 'Comment']] = df.apply(lambda row: pd.Series(split_comment(row)), axis=1)


df = df.drop(columns=['Narration', 'RefNo.', 'Value Dat', 'Comments'])

df.to_csv(cleanedTransactions, index=False)

print("CSV file updated successfully.")

# debitRecords = df[df['Credit Amount']==0.00] 
# creditRecords = df[df['Debit Amount']==0.00]

# debitRecords = debitRecords.drop(columns='Credit Amount')
# creditRecords = creditRecords.drop(columns='Debit Amount')

# debitRecords.to_csv(os.path.join('env', 'debitRecords.csv'))
# creditRecords.to_csv(os.path.join('env', 'creditRecords.csv'))

# print(creditRecords, debitRecords)