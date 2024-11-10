import streamlit as st
import pandas as pd
from openai import OpenAI
import base64

# Initialize the OpenAI API with your key
api_key = host=st.secrets["openai"]["key"]


# Initialize OpenAI client with your API key
client = OpenAI(api_key=api_key)

def process_image(image_bytes):
    """Process a single image and return the extracted data"""
    # Encode the image bytes to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Send the image to OpenAI and extract text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please extract the Mario baseball player data from this image. Return it as structured JSON ready to be turned into a dataframe. For each character there will be the following columns in this order: [Character, Hits, RBI, Home Runs, Bases Stolen, Special, Batting Avg]. DO NOT ADD ANY ADDITIONAL COLUMNS. If you don't know which Character is in the first column, guess a character from Mario. DO NOT wrap the json codes in JSON markers"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1000
    )
    
    return response

def extract_dataframe(all_json_data):
    """Convert combined JSON responses to a single DataFrame"""
    try:
        # Combine all player data into a single list
        all_player_data = []
        
        for json_str in all_json_data:
            # Convert string JSON to Python dictionary
            try:
                # Try to evaluate the string as a Python literal
                import ast
                player_data = ast.literal_eval(json_str)
                
                # If the data is a list, extend all_player_data
                if isinstance(player_data, list):
                    all_player_data.extend(player_data)
                # If the data is a dict, append it
                elif isinstance(player_data, dict):
                    all_player_data.append(player_data)
                    
            except (ValueError, SyntaxError):
                # If ast.literal_eval fails, try json.loads
                import json
                player_data = json.loads(json_str)
                
                # Handle both list and dict formats
                if isinstance(player_data, list):
                    all_player_data.extend(player_data)
                elif isinstance(player_data, dict):
                    all_player_data.append(player_data)
        
        # Create DataFrame from combined data
        df = pd.DataFrame(all_player_data)
        return df
        
    except Exception as e:
        st.error(f"Error processing JSON data: {str(e)}")
        return None

    
def process_batting_images_into_df(home_offense_images):
    all_json_data = []
    
    # Process each image and collect JSON data
    for idx, uploaded_file in enumerate(home_offense_images):
        st.subheader(f"Processing Image {idx + 1}: {uploaded_file.name}")
        
        # Display the uploaded image
        image_bytes = uploaded_file.read()
        st.image(image_bytes, caption=f"Box Score Image {idx + 1}")
        
        # Process the image
        with st.spinner('Processing image...'):
            try:
                # Process image and get response
                response = process_image(image_bytes)
                
                # Extract JSON data
                json_data = response.choices[0].message.content
                all_json_data.append(json_data)
                
                
            except Exception as e:
                st.error(f"Error processing image {idx + 1}: {str(e)}")
                continue
    
    if all_json_data:
        st.subheader("Combined Data Processing")
        try:
            # Process all JSON data into a single DataFrame
            combined_df = extract_dataframe(all_json_data)
            
            if combined_df is not None:
                # Add download button for combined CSV
                csv = combined_df.to_csv(index=False)
                return combined_df

        except Exception as e:
            st.error(f"Error combining data: {str(e)}")