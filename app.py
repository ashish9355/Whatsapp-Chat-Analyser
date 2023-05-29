
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pip
# import emoji
# pip.main(['install','emoji'])
pip.main(['install','seaborn'])
st.sidebar.title("Whatsapp-Chat-Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    # fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('SHOW ANALYSIS WRT', user_list)

    if st.sidebar.button('show analysis'):
        # stats anlysis
        st.title("Top Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        num_messages, total_words, num_media_shared, num_links, num_emoji = helper.fetch_stats(selected_user, df)

        with col1:
            st.header('Total Message')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(total_words)
        with col3:
            st.header('Media shared')
            st.title(num_media_shared)
        with col4:
            st.header('Links shared')
            st.title(num_links)
        with col5:
            st.header('Emojis shared')
            st.title(num_emoji)
    # daily timeline
        st.title('Daily timeline')
        daily_timeline = helper.daily_user_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['active_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    # monthly timeline
        st.title('Monthly timeline')
        timeline = helper.month_user_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    # activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day= helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month= helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title('Weekly Activity Map')
        user_heat= helper.activity_heat_map(selected_user, df)
        fig ,ax=plt.subplots()
        ax=sns.heatmap(user_heat)
        st.pyplot(fig)

    # finding the buisest user in the group(grouplevel)
        if selected_user=='Overall':
            st.title('Most busy User')
            x , new_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 =st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='blue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
         # creating word cloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # most common df
        st.title('Most 20 used words')
        most_common_df=helper.most_20_used_words(selected_user,df)
        fig, ax =plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)
        # emoji analysis
        # emoji_df = helper.emoji_help(selected_user, df)
        # col1, col2 = st.columns(2)
        # with col1:
        #     fig, ax = plt.subplots()
        #     ax.pie(emoji_df[1],labels= emoji_df[0])
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)
        #
        # st.dataframe(emoji_df)
        # #

