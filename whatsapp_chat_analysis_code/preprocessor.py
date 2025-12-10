import re 
import pandas as pd

def preprocesdata(data):
    # Enhanced pattern to match both 12-hour and 24-hour formats
    # Handles both regular space and non-breaking space (\u202f)
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s|\u202f)?(?:am|pm|AM|PM)?\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    if len(messages) == 0 or len(dates) == 0:
        raise ValueError("No messages found. Please check your WhatsApp chat format.")
    
    # Clean non-breaking spaces and extra whitespace
    clean_dates = [d.replace('\u202f', ' ').strip() for d in dates]
    
    df = pd.DataFrame({'user_message': messages, 'message_date': clean_dates})
    
    # Parse dates with multiple format attempts
    def parse_date(date_str):
        date_str = date_str.rstrip(' -').strip()
        
        # List of possible formats
        formats = [
            '%d/%m/%y, %I:%M %p',    # 12-hour with space before AM/PM
            '%d/%m/%Y, %I:%M %p',
            '%d/%m/%y, %I:%M%p',     # 12-hour without space
            '%d/%m/%Y, %I:%M%p',
            '%d/%m/%y, %H:%M',       # 24-hour
            '%d/%m/%Y, %H:%M',
        ]
        
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        # If all formats fail, return NaT
        return pd.NaT
    
    df['date_parsed'] = df['message_date'].apply(parse_date)
    
    # Check if parsing was successful
    if df['date_parsed'].isna().all():
        raise ValueError("Could not parse any dates. Please check your date format.")
    
    # Extract user and message
    users = []
    messages_list = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) == 3:  # Changed from >2 to ==3 for more precise matching
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])
    
    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message', 'message_date'], inplace=True)
    
    # Extract date components from parsed datetime
    df['year'] = df['date_parsed'].dt.year.astype(str)
    df['month'] = df['date_parsed'].dt.month.astype(str).str.zfill(2)
    df['day'] = df['date_parsed'].dt.day.astype(str)
    df['hour'] = df['date_parsed'].dt.hour.astype(str)
    df['minute'] = df['date_parsed'].dt.minute.astype(str).str.zfill(2)
    
    # Convert to 12-hour format for display
    df['hour_12'] = df['date_parsed'].dt.strftime('%I').str.lstrip('0').fillna('12')
    df['period'] = df['date_parsed'].dt.strftime('%p').fillna('AM')
    
    # Month name mapping
    month_map = {
        '01': 'January', '02': 'February', '03': 'March',
        '04': 'April', '05': 'May', '06': 'June',
        '07': 'July', '08': 'August', '09': 'September',
        '10': 'October', '11': 'November', '12': 'December'
    }
    df['month_name'] = df['month'].map(month_map)
    
    # Format dates for reference
    df['only_date'] = df['date_parsed'].dt.strftime('%d/%m/%y')
    df['day_name'] = df['date_parsed'].dt.day_name()
    df['date'] = df['date_parsed'].dt.strftime('%d/%m/%y, %I:%M %p')
    
    # Drop the temporary parsed column
    df.drop(columns=['date_parsed'], inplace=True)
    
    # Remove any rows with NaN values in critical columns
    df = df.dropna(subset=['year', 'month', 'day'])
    
    return df