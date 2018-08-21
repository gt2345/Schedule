import pandas as pd
import datetime

history = pd.read_csv('Input/Summer02_history.csv').fillna(0)
infobase = pd.read_csv('Input/Punch card - Final 0806.csv').fillna(0)
#['Info', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
result = []
for index, row in history.iterrows():
    is_valid_date = True
    try:
        month, day, year = str(row['Monday']).split('/')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        is_valid_date = False
    if is_valid_date:
        cur = history.iloc[index : index + 4].T
        cur.columns = ['Date', 'Class', 'Title', 'Ins']
        result.append(cur)
        #print(cur)
output = pd.concat(result)
output = output[(output['Class'] != 0) & (output['Date'] != 0)]
output['Id'] = -1
output = output.set_index('Date')
print(output)
for index, row in output.iterrows():
    #print(index)
    if str(row['Class']).startswith('Practice'):
        key = str(row['Class']).replace(':', ' ').split(' ')[1]
        key = key if len(key) == 2 else "0" + key
        key = "Practice " + key
        output.loc[index, 'Id'] = infobase.loc[infobase['Title'].str.startswith(key, na=False), 'Id'].item()
    else:
        key = str(row['Title']).lower()
        print(key)
        if key != '0':
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            if not infobase.loc[infobase['Title'].str.lower() == key].empty:
                output.loc[index, 'Id'] = infobase.loc[infobase['Title'].str.lower() == key, 'Id'].item()

output = output[2:]
title = 'Summer02'
output['Course'] = title
#output = output.drop(['Title'], axis=1)
output.to_csv(title + '_history_final.csv')


