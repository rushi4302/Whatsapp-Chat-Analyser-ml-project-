import re 
import pandas as pd

def preprocesdata(data):
    # Updated pattern to match both 12-hour and 24-hour formats
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s|\u202f)?(?:am|pm|AM|PM)?\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    # Clean non-breaking spaces
    clean_dates = [d.replace('\u202f', ' ').strip() for d in dates]
    
    df = pd.DataFrame({'user_message': messages, 'message_date': clean_dates})
    
    # Detect format and parse accordingly
    def parse_date(date_str):
        date_str = date_str.rstrip(' -').strip()
        
        # Try 12-hour format first
        for fmt in ['%d/%m/%y, %I:%M %p', '%d/%m/%Y, %I:%M %p', 
                    '%d/%m/%y, %I:%M%p', '%d/%m/%Y, %I:%M%p']:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        # Try 24-hour format
        for fmt in ['%d/%m/%y, %H:%M', '%d/%m/%Y, %H:%M']:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        return pd.NaT
    
    df['date'] = df['message_date'].apply(parse_date)
    
    # Extract user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'(^[^:]+):\s', message)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message', 'message_date'], inplace=True)
    
    # Extract date components
    df['year'] = df['date'].dt.year.astype(str)
    df['month'] = df['date'].dt.month.astype(str).str.zfill(2)
    df['day'] = df['date'].dt.day.astype(str)
    df['hour'] = df['date'].dt.hour.astype(str)
    df['minute'] = df['date'].dt.minute.astype(str).str.zfill(2)
    
    # Convert 24-hour to 12-hour format for display
    df['hour_12'] = df['date'].dt.strftime('%I').str.lstrip('0')
    df['period'] = df['date'].dt.strftime('%p')
    
    # Month name mapping
    month_map = {
        '01': 'January', '02': 'February', '03': 'March',
        '04': 'April', '05': 'May', '06': 'June',
        '07': 'July', '08': 'August', '09': 'September',
        '10': 'October', '11': 'November', '12': 'December'
    }
    df['month_name'] = df['month'].map(month_map)
    
    # Format only_date and day_name
    df['only_date'] = df['date'].dt.strftime('%d/%m/%y')
    df['day_name'] = df['date'].dt.day_name()
    
    # Keep original date column for reference
    df['date'] = df['date'].dt.strftime('%d/%m/%y, %I:%M %p')
    
    return df