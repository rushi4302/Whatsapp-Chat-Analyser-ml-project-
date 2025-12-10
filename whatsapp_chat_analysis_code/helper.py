from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percentage'})
    return x, df

def create_worldcloud(selected_user, df):
    file_path = os.path.join(os.path.dirname(__file__), "stop_hinglish.txt")
    f = open(file_path, "r")
    StopWords = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
   
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in StopWords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
    
def most_common_words(selected_user, df):
    file_path = os.path.join(os.path.dirname(__file__), "stop_hinglish.txt")
    f = open(file_path, "r")
    StopWords = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
   
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in StopWords:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).rename(
        columns={0: 'word', 1: 'count'})
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weak_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Use hour_12 for 12-hour display
    if 'hour_12' in df.columns:
        df['display_hour'] = df['hour_12'].astype(int)
    else:
        df['display_hour'] = df['hour'].astype(int)
    
    df['period'] = df['period'].str.upper()

    def make_range(row):
        hour = row['display_hour']
        period = row['period']

        current = f"{hour} {period}"

        if hour == 11:
            next_hour = 12
            next_period = "PM" if period == "AM" else "AM"
        elif hour == 12:
            next_hour = 1
            next_period = period
        else:
            next_hour = hour + 1
            next_period = period

        next_label = f"{next_hour} {next_period}"
        return f"{current} - {next_label}"

    df['hour_range'] = df.apply(make_range, axis=1)

    def sort_key(label):
        left = label.split(" - ")[0]
        h, p = left.split()
        h = int(h)

        if p == "AM":
            return 0 if h == 12 else h
        else:
            return 12 if h == 12 else h + 12

    df['sort_index'] = df['hour_range'].apply(sort_key)
    df = df.sort_values('sort_index')

    heatmap = df.pivot_table(
        index='day_name',
        columns='hour_range',
        values='message',
        aggfunc='count'
    )

    heatmap = heatmap.reindex(columns=df['hour_range'].unique())

    return heatmap