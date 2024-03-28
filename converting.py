import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook
transcationsExcel = os.path.join('env', 'transactions.xlsx')
transactions = os.path.join('env','cleanedTransactions.csv')



if os.path.exists(transactions):
    csv_data = pd.read_csv(transactions)
    try:
        print("Tryping to get existing excel")
        excel_data = pd.read_excel(transcationsExcel)

        print("Got the file")
        new_rows = pd.concat([excel_data, csv_data]).drop_duplicates(keep=False)

        print("Updating the new rows")
        combined_rows = pd.concat([excel_data, new_rows], ignore_index=True)
        combined_rows.to_excel(transcationsExcel, index=False)
        print("Updated Row:")
        print(pd.DataFrame(new_rows))

    except FileNotFoundError:
        print("No file found, creating new excel")
        csv_data.to_excel(transcationsExcel, index=False)
    print("Data updated successfully.")
else:
    print("No cleanedTransactions file found.")