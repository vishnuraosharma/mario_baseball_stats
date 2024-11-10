import streamlit as st
import mysql.connector
import pandas as pd
import batting_extraction as b_ext
import plotly.express as px


# Initialize session state variables if not already done
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Set up navigation using a sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("",options = ["Game Upload", "Analytics"])


# Game Upload Page
if page == "Game Upload":
    st.title("Upload a Game")
    container = st.container(border=True)
    # if form is not submitted, display the form
    if not st.session_state.form_submitted:
        # Create form
        with st.form("match_form"):
            # First row - Match details
            col1, col2 = st.columns(2)
            
            with col1:
                date_played = st.date_input("Date Played")
                stadium = st.selectbox("Stadium", 
                    ["Mario Stadium", "Peach Gardens", "Wario Stadium", 
                    "Yoshi Park", "DK Jungle", "Bowser Stadium"], 
                    index=0)
            with col2:
                series = st.text_input("Series", "Exhibition")
                drafting_method = st.text_input("Drafting Method", "CTDRP1")

                

            # Second row - Player and captain selection
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Home Team")
                home_player = st.selectbox("Home Player", 
                    ["Vishnu Rao-Sharma", "Brian Culbert", "Sam Boese", 
                    "Micah Bergman", "Joe N-R", "Kobe Darko"])
                home_captain = st.selectbox("Home Captain", 
                    ["Mario", "Wario", "Peach", "Yoshi", "DK", "Bowser",
                    "Waluigi", "Birdo", "Diddy", "Daisy", "Luigi", "Bowser Jr."])
                hits_home = st.number_input("Hits for Home Team", min_value=0, value=0)
                runs_home = st.number_input("Runs for Home Team", min_value=0, value=0)
            
            with col2:
                st.subheader("Away Team")
                away_player = st.selectbox("Away Player", 
                    ["Brian Culbert", "Sam Boese", "Micah Bergman",
                    "Vishnu Rao-Sharma", "Joe N-R", "Kobe Darko"])
                away_captain = st.selectbox("Away Captain", 
                    ["Mario", "Wario", "Peach", "Yoshi", "DK", "Bowser",
                    "Waluigi", "Birdo", "Diddy", "Daisy", "Luigi", "Bowser Jr."])
                hits_away = st.number_input("Hits for Away Team", min_value=0, value=0)
                runs_away = st.number_input("Runs for Away Team", min_value=0, value=0)
            
            # Image upload section
            st.subheader("Match Images")
            home_offense_images = st.file_uploader(
                "Upload Home Batting Images", 
                type=['png', 'jpg', 'jpeg'], 
                accept_multiple_files=True
            )
            away_offense_images = st.file_uploader(
                "Upload Away Batting Images", 
                type=['png', 'jpg', 'jpeg'], 
                accept_multiple_files=True
            )


            # Submit button
            submit = st.form_submit_button("Submit")
            if submit:
                st.session_state.date_played = date_played
                st.session_state.home_player = home_player
                st.session_state.home_captain = home_captain
                st.session_state.away_player = away_player
                st.session_state.away_captain = away_captain
                st.session_state.series = series
                st.session_state.stadium = stadium
                st.session_state.drafting_method = drafting_method
                st.session_state.runs_home = runs_home
                st.session_state.hits_home = hits_home
                st.session_state.runs_away = runs_away
                st.session_state.hits_away = hits_away

                # Images
                # --| Home Offense
                st.session_state.home_offense_images = home_offense_images
                st.session_state.home_offense_df = b_ext.process_batting_images_into_df(home_offense_images)

                # --| Away Offense
                st.session_state.away_offense_images = away_offense_images
                st.session_state.away_offense_df = b_ext.process_batting_images_into_df(away_offense_images)

                st.session_state.form_submitted = True
                st.rerun()

    # Display submitted form data
    if st.session_state.form_submitted:
    
        with container:
            st.header("Match Details Submitted")
            
            # General match information
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Game Information")
                st.write(f"**Date Played**: {st.session_state.date_played}")
                st.write(f"**Series**: {st.session_state.series}")
                st.write(f"**Stadium**: {st.session_state.stadium}")
                st.write(f"**Drafting Method**: {st.session_state.drafting_method}")
            
            # Team details in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Home Team")
                st.write(f"**Player**: {st.session_state.home_player}")
                st.write(f"**Captain**: {st.session_state.home_captain}")
                st.metric(
                    label="Runs",
                    value=st.session_state.runs_home,
                    delta=st.session_state.runs_home - st.session_state.runs_away
                )
                st.metric(
                    label="Hits",
                    value=st.session_state.hits_home,
                    delta=st.session_state.hits_home - st.session_state.hits_away
                )
            
            with col2:
                st.subheader("Away Team")
                st.write(f"**Player**: {st.session_state.away_player}")
                st.write(f"**Captain**: {st.session_state.away_captain}")
                st.metric(
                    label="Runs",
                    value=st.session_state.runs_away
                )
                st.metric(
                    label="Hits",
                    value=st.session_state.hits_away
                )

            # Add a visual separator
            st.divider()

        with container.expander("Home Batting Data", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.home_offense_images[0], caption="Home Batting Img 1")    
            with col2:
                st.image(st.session_state.home_offense_images[1], caption="Home Batting Img 2")    
            st.session_state.actual_home_batting_data = st.data_editor(st.session_state.home_offense_df)
        
        st.divider()
        with container.expander("Away Batting Data", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.away_offense_images[0], caption="Away Batting Img 1")    
            with col2:
                st.image(st.session_state.away_offense_images[1], caption="Away Batting Img 2")    
            st.session_state.actual_away_batting_data = st.data_editor(st.session_state.away_offense_df, )

        # add a button to save the data to the database
        if container.button("Save to Database"):
            # Connect to the MySQL database using secrets
            conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                port=st.secrets["mysql"]["port"]
            )

            # Insert the form data into the MSSB.games table
            cursor = conn.cursor()
            cursor.execute("INSERT INTO MSSB.games (date_played, home_user, away_user, home_captain, away_captain, series, stadium, drafting_method, runs_home, hits_home, runs_away, hits_away) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (st.session_state.date_played, st.session_state.home_player, st.session_state.away_player, 
                            st.session_state.home_captain, st.session_state.away_captain, st.session_state.series, st.session_state.stadium, st.session_state.drafting_method,
                            st.session_state.runs_home, st.session_state.hits_home, st.session_state.runs_away, st.session_state.hits_away))
            
            # grab the game_id from the last insert
            game_id = cursor.lastrowid

            # Iterate through the rows of the DataFrame
            for index, row in st.session_state.actual_home_batting_data.iterrows():
                character = row['Character']
                hits = row['Hits']
                rbis = row['RBI']
                home_runs = row['Home Runs']
                bases_stolen = row['Bases Stolen']
                special_hits = row['Special']
                avg = row['Batting Avg']
                player_name = st.session_state.home_player

                # Insert batting data into the database
                cursor.execute("""
                    INSERT INTO MSSB.player_performance 
                    (player_name, `character`, game_id, hits, rbis, home_runs, bases_stolen, special_hits, batting_avg)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                    (player_name, character, game_id, hits, rbis, home_runs, bases_stolen, special_hits, avg)
                )
            
            # Iterate through the rows of the DataFrame
            for index, row in st.session_state.actual_away_batting_data.iterrows():
                character = row['Character']
                hits = row['Hits']
                rbis = row['RBI']
                home_runs = row['Home Runs']
                bases_stolen = row['Bases Stolen']
                special_hits = row['Special']
                avg = row['Batting Avg']
                player_name = st.session_state.away_player

                # Insert batting data into the database
                cursor.execute("""
                    INSERT INTO MSSB.player_performance 
                    (player_name, `character`, game_id, hits, rbis, home_runs, bases_stolen, special_hits, batting_avg)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                    (player_name, character, game_id, hits, rbis, home_runs, bases_stolen, special_hits, avg)
                )

            
            conn.commit()
            cursor.close()
            conn.close()

            # Display a success message
            st.write("Match data saved successfully!")
        # add a button to clear the form and reset the form_submitted state
        if container.button("Go Back"):
            del st.session_state.form_submitted
            st.rerun()

        



# Analytics Page
else:
    st.title("Game Analytics")
    # Connect to the MySQL database using secrets
    conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                port=st.secrets["mysql"]["port"]
            )
    
    # Query the database for the games
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MSSB.games")
    games = cursor.fetchall()
    conn.close()
    games_df = pd.DataFrame(games, columns=cursor.column_names)


    # Display the games in a data table
    st.write("Recent Games")
    st.write(games_df)

    conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                port=st.secrets["mysql"]["port"]
            )
    # Display the average number of hits per game
    st.write("Average Hits per Game")

    # Run the query
    query = """
    SELECT 
        pp.character as Mario_Character, avg(pp.hits) as avg_hits_per_game
    
    FROM 
        MSSB.player_performance pp
    group by pp.`character` 
;
    """

    cursor = conn.cursor()
    cursor.execute(query)
    chars = cursor.fetchall()
    conn.close()
    chars_df = pd.DataFrame(chars, columns=cursor.column_names)

    st.write(chars_df)

    # Create the bar plot using Plotly
    fig = px.bar(chars_df, x='Mario_Character', y='avg_hits_per_game',
                title='Average Hits Per Game for Each Player',
                labels={'Mario_Character': 'Player Name', 'avg_hits_per_game': 'Average Hits per Game'},
                color='avg_hits_per_game')

    # Show the plot
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
