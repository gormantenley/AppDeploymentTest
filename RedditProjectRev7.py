

from google import genai
#use reddit api to get posts from a subreddit
import praw
import pandas as pd
import streamlit as st
import altair as alt
import json

#SETUP
#GEMINI API SETUP
#Password = config['password']
GEMINI_API_KEY = "AIzaSyAKq9tcihQTvaO-qPZ2wVy8F28aci1qZO8"
client = genai.Client(api_key=GEMINI_API_KEY)
#REDDIT API SETUP
reddit = praw.Reddit(
     client_id="tBUSBV7v5JEUasL3p5XERQ",
    client_secret="JIMsy_BAKR8KABBKPvXkd3aucsmZ4A",
    user_agent="MyRedditApp/0.1 by appliedmlproj",
)

#BEGINNING OF STREAMLIT APP
st.title('Welcome to BrandWhispers!')
st.write('Not from surveys—straight from gossip forums.') #Tagline 
subreddit_name = st.text_input('Enter the brand name you are here to inquiry about. And get hot takes that are so good they are whispered:', 'Nike')
#ADDING A KEYWORD INPUT
keyword = st.text_input('Now enter a product you want to snoop on:', 'Shoe')

#post limit CHANGE HERE
#post limit: change later so that its always a sufficient amount, maybe an if statement based on number of total posts
#post_limit = st.number_input('Number of posts to retrieve:', min_value=1, max_value=100, value=10)
#for now i am just setting post_limit to 5
post_limit = 20


#CACHE SYSTEM SETUP
@st.cache_data

#get_top_posts FUNCTION SETUP
def get_top_posts(subreddit_name, post_limit, keyword):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []
    for submission in subreddit.top(limit=post_limit * 2):  # get extra in case many are filtered out
        #this line will filter for keywords in JUST the title
        #if keyword.lower() in submission.title.lower():
        #this line changes it so the keyword is filtered in title AND body
        if keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower():
            top_posts.append([submission.title, submission.score, submission.url, submission.created_utc])
        if len(top_posts) >= post_limit:
            break
    df = pd.DataFrame(top_posts, columns=['Title', 'Score', 'URL', 'Created'])
    df['Created'] = pd.to_datetime(df['Created'], unit='s')
    return df

#get_top_posts2 FUNCTION SETUP
def get_top_posts2(subreddit_name, post_limit, keyword):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []
    for submission in subreddit.top(limit=post_limit * 2):
       # if keyword.lower() in submission.title.lower():    #filters for keyword JUST in title
        if keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower():
            top_posts.append([submission.title, submission.score, submission.url, submission.created_utc])
        if len(top_posts) >= post_limit:
            break
    return top_posts


#FUNCTION SETUP for analyze_sentiment
#function to analyze sentiment of the posts using the Gemini API
def analyze_sentiment(text_to_analyze, subreddit_name):
    sentiment_prompt = (
        "Tell me how the Title of the post relates to "
            f"'{subreddit_name}'.\n"
            "You can find the posts here:\n"
            f"{text_to_analyze}")
    gemini_response = client.models.generate_content(model="gemini-1.5-pro-latest", contents=[sentiment_prompt])
    if gemini_response and hasattr(gemini_response, 'text'):
        text_content = gemini_response.text
    else:
        text_content = "No response from Gemini API."


    return text_content


#FUNCTION SETUP for 
#this function gets the general sentiment of the for this keyword of brand























# New function to get general insights on a keyword in a specific subreddit
def general_insights(subreddit_name, keyword, post_limit):
    # Get top posts containing the keyword
    df = get_top_posts(subreddit_name, post_limit, keyword)
    
    if df.empty:
        return "No posts found with that keyword."

    # Collect sentiment analysis results for each post
    sentiments = []
    for index, row in df.iterrows():
        text_to_analyze = f"Title: {row['Title']}\nScore: {row['Score']}\n\n{row['Title']}"
        sentiment = analyze_sentiment(text_to_analyze, subreddit_name)
        sentiments.append(sentiment)
    
    # Aggregate sentiment results (positive, negative, neutral)
    positive_posts = sum([1 for sentiment in sentiments if "positive" in sentiment.lower()])
    negative_posts = sum([1 for sentiment in sentiments if "negative" in sentiment.lower()])
    neutral_posts = len(sentiments) - positive_posts - negative_posts

    # Prepare a general insight summary
    general_opinion = (
        f"### General opinions on {keyword} by the brand r/{subreddit_name}:\n"
        f"- **Positive Posts**: {positive_posts}\n"
        f"- **Negative Posts**: {negative_posts}\n"
        f"- **Neutral Posts**: {neutral_posts}\n\n"
        "Based on these posts, it seems people are generally more [positive/negative/neutral] "
        "about this product.\n\n"
        "Here are some insights from the top posts:"
    )
    
    return general_opinion

# Button to start the process
if st.button('Start Eavesdropping'):
    #Displays start below this line------------------------------------------
#print a statement that says "Listen in on what people are saying about {keyword} from {subreddit_name}..."
    st.write(f"### Listen in on what people are saying about {keyword} from r/{subreddit_name}...")

    # Get the general insights first
    general_opinion = general_insights(subreddit_name, keyword, post_limit)
    st.write(general_opinion)

    df = get_top_posts(subreddit_name, post_limit, keyword)
    df1 = get_top_posts2(subreddit_name, post_limit, keyword)
    
    if df.empty:
        st.warning("No posts found with that keyword.")
    else:
        text_to_analyze = "\n\n".join(
            [f"Title: {row[0]}\nScore: {row[1]}" for row in df1]
        )
        sentiment = analyze_sentiment(text_to_analyze, subreddit_name)

        # The rest of your logic stays the same











# Display the chart in the Streamlit app
#S    st.altair_chart(chart, use_container_width=True)
   
    # Create a text output of the top posts with the title and score
    st.write(f"### Top {post_limit} Posts On r/{subreddit_name}")
    for index, row in df.iterrows():
        st.markdown(f"###  **[{row['Title']}]({row['URL']})**")
        st.markdown(f"**Score:** {row['Score']:,}")
        st.write(sentiment)
        st.write("---")  # Separator line for readability


    st.write("### Top Posts by Score")
    st.write(df)




st.write('BrandWhispers is here to democratize consumer insights by making unfiltered brand sentiment instantly accessible to everyone—without the noise.')
