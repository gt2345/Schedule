from __future__ import print_function
import pandas as pd
import datetime
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
class_input = 'Input/class_input_for_RL finished.csv'
infobase = pd.read_csv(class_input).fillna(0)


def get_ss_value(sheetName):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '13qKTcwqIL8ZrLvqkuq2NSKBMHb-CAWy8wgCGKxeK4Vo'
    RANGE_NAME = sheetName + '!A:H'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def if_valid_date(row):
    if len(row) < 8:
        return False
    try:
        if '/' in str(row[1]):
            cur_date_month, cur_date_day, cur_date_year = str(row[1]).split('/')
        else:
            cur_date_year, cur_date_month, cur_date_day = str(row[1]).split('-')
        datetime.datetime(int(cur_date_year), int(cur_date_month), int(cur_date_day))
    except ValueError:
        return False
    return True


def get_practice_num(cell):
    print(cell)
    num = re.findall(r'\d+', cell)
    print(num)
    if len(num) > 0:
        return num[0]
    return -1


def import_history(title):
    # history = pd.read_csv('Input/' + title + '_history.csv').fillna(0)
    try:
        history = get_ss_value(sheetName=title.replace("0", " ")) + (get_ss_value(sheetName='Current Week'))
    except HttpError:
        history = get_ss_value(sheetName='Current Week')


    result = []
    index = 0
    while index < len(history) - 2:
        row = history[index]

        # see if this row is a date
        if if_valid_date(row):
            result.append(row)
            index += 1
            while index < len(history) - 2:
                if if_valid_date(history[index]):
                    break
                if history[index][0] == title.replace("0", " ") and history[index + 1][0] == "正式班":
                    cur = history[index: index + 3]
                    result.append(cur)
                    break
                index += 1
        index += 1
    output_list = []
    for r in result:
        if len(r) == 8:
            output_list.append(r)
        else:
            for s in r:
                output_list.append(s)
    print(output_list)
    if len(output_list) % 4 != 0:
        print("error")
        print(len(output_list))
        quit(11)
    output_df = pd.DataFrame(columns=["Date", "Class", "Title", "Ins"])

    index = 0
    while index <= len(output_list) - 4:
        tmp = pd.DataFrame(output_list[index: index + 4])
        tmp = tmp.T[1:]
        tmp.columns = ["Date", "Class", "Title", "Ins"]
        output_df = output_df.append(tmp, ignore_index=True)
        index += 4

    output_df = output_df[output_df['Class'] != ""]
    output_df['Id'] = -1
    output = output_df.set_index('Date')

    for index, row in output.iterrows():
        if str(row['Class']).startswith('Practice'):
            key = str(row['Class']).replace(':', ' ').split(' ')[1]
            if row['Title'] is not None and len(row['Title']) > 1:
                temp_key = get_practice_num(row['Title'])
                if int(temp_key) > 0:
                    key = temp_key
            key = key if len(key) == 2 else "0" + key
            key = "Practice " + key
            output.loc[index, 'Class'] = key
            output.loc[index, 'Id'] = infobase.loc[infobase['Title'].str.startswith(key, na=False), 'Id'].item()
        else:
            key = str(row['Title']).lower()
            if key != '0':
                if not infobase.loc[infobase['Title'].str.lower() == key].empty:
                    output.loc[index, 'Id'] = infobase.loc[infobase['Title'].str.lower() == key, 'Id'].item()

    output = output[1:]
    output['Course'] = title
    output.to_csv("Output/" + title + '_history_cleaned.csv')


title = ["Fall01"]
for t in title:
    import_history(t)
