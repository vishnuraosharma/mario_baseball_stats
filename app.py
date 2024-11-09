import streamlit as st
import mysql.connector
import pandas as pd


# Connect to the MySQL database using secrets
conn = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    port=st.secrets["mysql"]["port"]
)

# Query the MSSB.games table
query = "SELECT game_id, date_played, home_user, away_user, home_captain, away_captain, series, stadium FROM MSSB.games"
games_df = pd.read_sql(query, conn)

# Display the data in the Streamlit app
st.write("Sample Data from database:")
st.dataframe(games_df)

# Close the connection
conn.close()


# Set up navigation using a sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("",options = ["Game Upload", "Analytics"])


# Game Upload Page
if page == "Game Upload":
    st.title("Upload a Game")

# Create form
with st.form("match_form"):
    # Date played - Calendar widget
    date_played = st.date_input("Date Played")
    
    # Home player - Single select widget
    home_player = st.selectbox("Home Player", ["Vishnu Rao-Sharma", "Brian Culbert", "Sam Boese", "Micah Bergman", "Joe N-R", "Kobe Darko"])
    
    # Home captain - Single select widget with captain options
    home_captain = st.selectbox("Home Captain", ["Mario", "Wario", "Peach", "Yoshi", "DK", "Bowser", "Waluigi", "Birdo", "Diddy", "Daisy", "Luigi", "Bowser Jr."])

    # Away player - Single select widget
    away_player = st.selectbox("Away Player", ["Brian Culbert", "Sam Boese", "Micah Bergman", "Vishnu Rao-Sharma", "Joe N-R", "Kobe Darko"])
    
    # Away captain - Single select widget with captain options
    away_captain = st.selectbox("Away Captain", ["Mario", "Wario", "Peach", "Yoshi", "DK", "Bowser", "Waluigi", "Birdo", "Diddy", "Daisy", "Luigi", "Bowser Jr."])

    # Series - Text input with default value
    series = st.text_input("Series", "Exhibition")
    
    # Stadium - Single select widget with default value
    stadium = st.selectbox("Stadium", ["Mario Stadium", "Peach Gardens", "Wario Stadium", "Yoshi Park", "DK Jungle", "Bowser Stadium"], index=0)

    # Drafting method - Text input with default value
    drafting_method = st.text_input("Drafting Method", "CTDRP1")
    
    # Image file uploader - Allow multiple images
    image = st.file_uploader("Upload Home Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

    # Submit button
    submit = st.form_submit_button("Submit")

# Display submitted form data
if submit:
    st.write("Match Details Submitted:")
    st.write("Date Played:", date_played)
    st.write("Home Player:", home_player)
    st.write("Home Captain:", home_captain)
    st.write("Away Player:", away_player)
    st.write("Away Captain:", away_captain)
    st.write("Series:", series)
    st.write("Stadium:", stadium)
    st.write("Drafting Method:", drafting_method)
    st.write("Uploaded Images:", image)


# Display results upon form submission
if submit:
    st.write("Match Details:")
    st.write("Date Played:", date_played)
    st.write("Home Captain:", home_captain)
    st.write("Away Captain:", away_captain)
    st.write("Series:", series)
    st.write("Stadium:", stadium)

# Analytics Page
elif page == "Analytics":
    st.title("Analytics")
    st.write("Use this page to view analytics data.")
    
    # Placeholder for analytics charts
    st.write("Display your analytics charts or tables here.")
    
    # Example of simple data visualization (replace with real analytics data)
    import pandas as pd
    import numpy as np

    # Sample data
    data = pd.DataFrame({
        'Games': ['Game 1', 'Game 2', 'Game 3', 'Game 4'],
        'Users': np.random.randint(100, 1000, size=4),
        'Playtime (hrs)': np.random.randint(20, 200, size=4)
    })

    st.write("Game Analytics Data")
    st.dataframe(data)

    st.bar_chart(data.set_index('Games'))

# Run the app
# Execute this script in terminal: streamlit run app.py
