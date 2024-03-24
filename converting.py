import pandas as pd
import numpy as np
import os
transcationsExcel = os.path.join('env', 'transactions.xlsx')
transactions = os.path.join('env','transactions.csv')

csv_data = pd.read_csv(transactions)


try:
    print("Tryping to get existing excel")
    excel_data = pd.read_excel(transcationsExcel)

    print("Got the file")
    updated_rows = pd.concat([excel_data, csv_data]).drop_duplicates(keep=False)

    print("Updating the new rows")
    if not updated_rows.empty:
        with pd.ExcelWriter(transcationsExcel, if_sheet_exists='replace', mode='a', engine='openpyxl') as writer:
            updated_rows.to_excel(writer, index=False, header=False)
    print("Updated Row:")
    print(pd.DataFrame(updated_rows))

except FileNotFoundError:
    print("No file found, creating new excel")
    csv_data.to_excel(transcationsExcel, index=False)
print("Data updated successfully.")
