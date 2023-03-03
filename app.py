import streamlit as st
import preprocessor
import helperfun
import matplotlib.pyplot as plt
import seaborn as sbn
st.sidebar.title("Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    # No need to show all messages to user



    # st.dataframe(df)


#     Fetching unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall",)
    selected_user=st.sidebar.selectbox("Show Analysis with respect to ",user_list)


    if st.sidebar.button("Show Analysis"):
        num_messages,words,media_message,links =helperfun.fetch_status(selected_user,df)


        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words In Chat")
            st.title(words)


        with col3:
            st.header("Total Media Messages in Chat")
            st.title(media_message)
        with col4:
            st.header("Total Links  in Chat")
            st.title(links)


        if selected_user=='Overall':
            st.title("Most Active User in Group")
            x,newdf=helperfun.most_active_user(df)
            # Is Line Ko dobara padhna hai
            fig , ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color="yellow")
                plt.xticks(rotation='vertical')

                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)


    # TIMELINE TOGETHER
    st.title("Overall TimeLine")
    col1,col2=st.columns(2)
    with col1:
        # TIMELINE OF MESSAGES  ---->MONTHLY

        st.title("Monthly Timeline")
        timeline = helperfun.get_monthly_time_wise_stats(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        # plt.show()

        st.pyplot(fig)
    with col2:
        st.title("Daily  Timeline")
        daily_timeline = helperfun.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date_wise_msg'], daily_timeline['message'], color='blue')
        plt.xticks(rotation='vertical')
        # plt.show()

        st.pyplot(fig)

    # Daily Timeline



    #Activity Map
    st.title("Activity Tracker")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most Active Day")
        bussiest_day=helperfun.most_active_days(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(bussiest_day.index,bussiest_day.values)
        st.pyplot(fig)
    with col2:
        st.header("Most Active Month")
        bussiest_month = helperfun.monthly_activity_chart(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(bussiest_month.index, bussiest_month.values)
        st.pyplot(fig)











    #MOST FREQUENT WORDS
    most_common=helperfun.most_common_words(selected_user,df)
    st.title("Most Frequent Words")
    st.dataframe(most_common)


    fig,ax=plt.subplots()
    ax.bar(most_common[0],most_common[1])
    #      HORIZONTAL BAR PLOTTING
    # ax.barh(most_common[0],most_common[1])
    plt.xticks(rotation='vertical')
    st.pyplot()



    #WORD CLOUD
    df_wc=helperfun.word_cloud_creation(selected_user,df)
    st.title("Word Cloud")
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)




    # Emoji Analysis
    emoji_df = helperfun.get_all_emojisdata(selected_user,df)
    st.title("Most Used Emojis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        # fig,ax=plt.subplots()
        # ax.pie(emoji_df[1],labels=emoji_df[0])

        # st.pyplot(fig)
        fig, ax = plt.subplots()
        ax.bar(emoji_df[0], emoji_df[1])
        plt.xticks(rotation='vertical')
        # ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)






# Heat Map (Daily time (0-24)
    st.title("Activity Heatmap")
    fig,ax=plt.subplots()

    heat_map=helperfun.heat_map_generation(selected_user,df)
    ax=sbn.heatmap(heat_map)
    st.pyplot(fig)
