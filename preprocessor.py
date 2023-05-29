import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\W[a-z][a-z]\s'
    date = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({'user_message': messages, 'messages_date': date})
    df["messages_date"] = pd.to_datetime(df['messages_date']).dt.strftime('%d/%m/%Y, %I:%M %p')
    df["messages_date"] = pd.to_datetime(df["messages_date"])
    df.rename(columns={'messages_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('\S\s([\w\W]+?):\s', message)
        if (entry[1:]):
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['active_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['day_name'] = df['date'].dt.day_name()
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df.hour:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df