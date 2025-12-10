import re 
import pandas as pd




def preprocesdata(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s|\u202f)?(?:am|pm|AM|PM)\s-\s'
    messages=re.split(pattern,data) [1:]
    dates = re.findall(pattern, data)
    clean = [d.replace('\u202f', ' ') for d in dates]
    

    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    

    df['date'] = df['date'].dt.strftime('%d/%m/%y, %I:%M %p')

    users = []
    messages = []

    for message in df['user_message']:
        
        entry = re.split(r'(^[^:]+):\s', message)

        if len(entry) > 2:              # means sender exists
            users.append(entry[1])      # sender (phone/name)
            messages.append(entry[2])       # message text
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].str.extract(r'/(\d{2}),')[0].apply(lambda y: '20' + y)
    # Extract month number
    df['month'] = df['date'].str.extract(r'^(\d{1,2})/(\d{1,2})/')[1]


# Map month number to month name
    month_map = {
    '01': 'January', '1': 'January',
    '02': 'February', '2': 'February',
    '03': 'March', '3': 'March',
    '04': 'April', '4': 'April',
    '05': 'May', '5': 'May',
    '06': 'June', '6': 'June',
    '07': 'July', '7': 'July',
    '08': 'August', '8': 'August',
    '09': 'September', '9': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
    }

    df['month_name'] = df['month'].map(month_map)

    df['day'] = df['date'].str.extract(r'^(\d{1,2})/')

    df['hour'] = df['date'].str.extract(r',\s(\d{1,2}):')

    df['minute'] = df['date'].str.extract(r':(\d{2})')

    df['period'] = df['date'].str.extract(r'\s(AM|PM|am|pm)$')

    df['only_date'] = df['date'].str.extract(r'^(\d{1,2}/\d{1,2}/\d{2})')

    df['day_name'] = pd.to_datetime(df['only_date'], format="%d/%m/%y").dt.day_name()


 

    return df

