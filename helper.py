# from nbconvert import export
# import emoji
from urlextract import URLExtract

import re

from wordcloud import WordCloud

import pandas as pd

from collections import Counter

import string
# import pip
# import emoji
# pip.main(['install','emoji'])

# import emoji
extract = URLExtract()
# export DJANGO_SETTINGS_MODULE= whatsapp-chat-anlyser.settings
# export DJANGO_SETTINGS_MODULE=mysite.settings
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch number of messages
    num_messages = df.shape[0]
    # fetch the total no of words
    word = []
    for message in df['message']:
        word.extend(message.split())
    total_words = len(word)
    # fetch number of media messages
    num_media_shared = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    # fetch number of emoji's
    new_list_emoji = []
    pattern = '[^\w\s,.]'
    for message in df['message']:
        new_list_temp = re.findall(pattern, message)
        new_list_emoji.append(new_list_temp)
    return num_messages, total_words, num_media_shared, len(links), len(new_list_emoji)


def most_busy_users(df):
    x = df['user'].value_counts()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'percent', 'user': 'name'})

    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    tagwords = []
    for message in temp['message']:
        list1 = re.findall('\W\d\d\d\d\d\d\d\d\d\d\d\d', message)
        tagwords.append(list1)
    ls = pd.DataFrame(tagwords)
    ls1 = ls[0].unique()

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words and word not in ls1:
                words.append(word)
        return " ".join(words)

    def remove_punctuation(message):
        x = re.sub('[%s]' % re.escape(string.punctuation), '', message)
        return x
    wc = WordCloud(width=500, height=500, min_font_size=15, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)  # remove stopwords
    temp['message'] = temp['message'].apply(remove_punctuation)  # remove punctuations
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_20_used_words(selected_user, df):
    # remove stop words
    # remove group message
    # remove media omitted message
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    tagwords = []
    for message in temp['message']:
        list1 = re.findall('\W\d\d\d\d\d\d\d\d\d\d\d\d', message)
        tagwords.append(list1)
    ls = pd.DataFrame(tagwords)
    ls1 = ls[0].unique()
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in ls1:
                words.append(word)

    #     words.extend((message.split()))
    from collections import Counter
    x = Counter(words).most_common(20)
    most_common_df = pd.DataFrame(x)
    return most_common_df
    # emoji analysis
# def emoji_help(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#     emojis = []
#     for message in df['message']:
#         data = re.findall(r'\X', message)
#         for word in data:
#             if any(char in emoji.UNICODE_EMOJI['en'] for char in word):
#                 emojis.append(word)
        # for j in message:
        #     if j in emoji.EMOJI_DATA:
        #         emojis.append(j)
    # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    # import emoji
    # import regex

    # def split_count(text):
    #
    #     emoji_list = []
    #     data = regex.findall(r'\X', text)
    #     for word in data:
    #         if any(char in emoji.UNICODE_EMOJI['en'] for char in word):
    #             emoji_list.append(word)
    #
    #     return emoji_list
    # return emoji_df
def month_user_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        temp = timeline['month'][i] + "-" + str(timeline['year'][i])
        time.append(temp)
    timeline['time'] = time
    return timeline
def daily_user_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['active_date']).count()['message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heat = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heat