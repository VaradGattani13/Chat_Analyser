from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
import emoji
from collections import Counter

urlx=URLExtract()

def fetch_status(selected_user,df):
    # CODE KI SAAF SAFAI KRDI

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
        # Fetching the number of messages
    num_messages=df.shape[0]


        # Fetching number of words
    words=[]
    for message in df['message']:
            # Words ko tukdo mai baat dia yaha se
        words.extend(message.split())

    #     Fetching thr number of media messages
    media_message=df[df['message']=='<Media omitted>\n'].shape[0]




    # Fetching the total Number of Links
    links=[]
    for message in df['message']:
        links.extend(urlx.find_urls(message))








    return num_messages , len(words),media_message,len(links)

    # Getting the Most Active Users in Group

def most_active_user(df):
    x = df['user'].value_counts().head()
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df








# MOST FREQUENT WORDS/


def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stopwords.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df=pd.DataFrame(Counter(words).most_common(40))
    return return_df


    # Word Cloud
def word_cloud_creation(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stopwords.txt', 'r')
    stop_words = f.read()
    def remove_stopwrods(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stopwrods)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


    # EMOJI FUNCTION
def get_all_emojisdata(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return  emoji_df


def get_monthly_time_wise_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        #     print(timeline['month'][i]+"-"+str(timeline['year'][i]))
        #     print(timeline['month'][i] + "-" + str(timeline['year'][i]))

        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline




def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    daily_message_timeline = df.groupby('date_wise_msg').count()['message'].reset_index()
    return daily_message_timeline







def most_active_days(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()







def monthly_activity_chart(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()






def heat_map_generation(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_heatmap

    # if selected_user=='Overall':
    #     # Fetching the number of messages
    #     num_messages=df.shape[0]
    #
    #
    #     # Fetching number of words
    #     words=[]
    #     for message in df['message']:
    #         # Words ko tukdo mai baat dia yaha se
    #         words.extend(message.split())
    #     return num_messages,len(words)
    #
    #
    #
    #
    #     # return df.shape[0]
    # else:
    #     # Naya dataframe bana dia else condition ke liye
    #     new_df=df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #
    #     # Fetching number of words
    #     words = []
    #     for message in new_df['message']:
    #         # Words ko tukdo mai baat dia yaha se
    #         words.extend(message.split())
    #     return num_messages, len(words)
    #     # Masking
    #
    #
    #
    #
    #
    #
    #     # upa function sabko tukdo mai baatde ga
    #
    #     # return df[df['user']==selected_user].shape[0]

