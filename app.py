import streamlit as st

# Set up navigation using a sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("",options = ["Game Upload", "Analytics"])


# Game Upload Page
if page == "Game Upload":
    st.title("Upload a Game")
    
    # Game upload form
    # Create form
    with st.form("match_form"):
        # Date played - Calendar widget
        date_played = st.date_input("Date Played")
        
        # Home captain - Single select widget
        home_captain = st.selectbox("Home Captain", ["Vishnu Rao-Sharma", "Brian Culbert", "Sam Boese", "Micah Bergman"])
        
        # Away captain - Single select widget
        away_captain = st.selectbox("Away Captain",  [ "Brian Culbert", "Sam Boese", "Micah Bergman", "Vishnu Rao-Sharma"])
        
        # Series - Text input with default value
        series = st.text_input("Series", "Exhibition")
        
        # Stadium - Single select widget with default value
        stadium = st.selectbox("Stadium", ["Mario Stadium", "Peach Gardens", "Wario Stadium","Yoshi Park", "DK Jungle", "Bowser Stadium"], index=0)
        
        # Add a image file uploader
        image = st.file_uploader("Upload Home Images", type=['png', 'jpg', 'jpeg'],accept_multiple_files=True)

        # Submit button
        submit = st.form_submit_button("Submit")

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
