import streamlit as st
import google.generativeai as genai
import PIL.Image
from difflib import SequenceMatcher

# Custom CSS styles 
st.markdown(
    """
    <style>
        /* CSS for the title */
        .title-text {
            font-size: 48px;
            font-weight: bold;
            color: #336699; /* Adjust color as needed */
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Add a text shadow */
            margin-bottom: 15px; /* Adjust spacing as needed */
        }
        
        /* CSS for clear button */
        /* CSS for the clear button */
        button[data-testid="clear_button"] {
            background-color: #FF474C; /* Red color for clear button */
            color: white; /* Text color */
            border-radius: 5px; /* Rounded corners */
            border: none; /* Remove border */
            padding: 10px 20px; /* Padding */
            margin-top: 10px; /* Adjust spacing as needed */
            cursor: pointer; /* Cursor style */
            transition: background-color 0.3s; /* Smooth transition */
        }

        /* Hover effect for clear button */
        button[data-testid="clear_button"]:hover {
            background-color: #FF6B6E; /* Lighter red on hover */
            transform: scale(1.05); /* Increase button size on hover */
        }

        
    </style>
    """,
    unsafe_allow_html=True
)

# Main function
def main():
    st.markdown("<p class='title-text'>MovieBuff - Know more about Movies Before Wasting 2hrs</p>", unsafe_allow_html=True)
 # Sidebar for inputs
    with st.sidebar:   
        st.write("Please insert the Movie Name (with release year if possible) below or upload an image of movie poster and we'll provide you with information about the movie/tv series. Happy Binging!!!")
        
        # Set Google API key
        genai.configure(api_key = "AIzaSyDzjiNgzTf95qF5gA7F76MCpcVDUI7JVcA")

        model = genai.GenerativeModel("gemini-pro")

        # Accept user input
        
        query = st.text_input("Insert  Movie Name and year here:")
        uploaded_file = st.file_uploader("Upload an image of the movie poster", type=["jpg", "jpeg", "png"], accept_multiple_files=False)


        search_clicked = st.button("🔍 Search")
        clear_clicked = st.button("🗑️ Clear my search" , key="clear_button")

    # Main area for displaying outputs
    st.markdown("---")

    with st.container():
        if clear_clicked:
            query = ""
            uploaded_file = None


        elif search_clicked:
          with st.spinner(" We're fetching movie plot, please standby...."):
            # Check if both query and uploaded_file are empty
            if not query and not uploaded_file:
                return  # Do nothing and wait for user input

            # Calling the Function when Input is Provided
            if query:
                # Process the query and generate response
                prompt = f"""
                
                ### Movie Plot Summary (No Spoiler):
                Based on '{query}', provide a summary of the Movie. Try to avoid spoliers as much as possible.

                ### Director and year:
                Who is the director . Also, provide the year it was made.

                ### Genre and Theme:
                Identify the genre and theme of the story in the movie.

                ## Main Conflict 
                Identify the main conflict of the plot and brief description

                ### Setting of the Story:
                Describe where the movie plot is set and provide a brief description of the setting.

                ### Expectations for Viewers:
                What should readers expect while watching the movie?

                ### Characters:
                List the characters and provide a description if possible.

                ### Trivia:
                Hos long is the movie and what are the interesting things people like about the movie?

                ### Series Information:
                Is this part of a series? What are the other movies in the series? Where does it fit in?

                ### Similar Movies:
                Recommend four other movies that are similar to '{query}' based on genre and theme.
                """



                response = model.generate_content([prompt])

                
                st.markdown(response.text)
                
            
            
            elif uploaded_file is not None:

                image = PIL.Image.open(uploaded_file)

                vision_model = genai.GenerativeModel('gemini-pro-vision')

                prompt = f"""
                ### **Please list all my requirements based on the image provided:**

                ### Movie Name:
                What is the movie name recognised based on the image
                
                ### Movie Summary(No Spoilers):
                Based on the image, , provide a summary of the Movie. Try to avoid spoliers as much as possible.

                ### Author and Publisher:
                Who is the director . Also, provide the year it was made.

                ### Genre and Theme:
                Identify the genre and theme of the story in the movie.

                ## Main Conflict 
                Identify the main conflict of the plot and brief description

                ### Setting of the Story:
                Describe where the movie plot is set and provide a brief description of the setting.

                ### Expectations for Viewers:
                What should readers expect while watching the movie?

                ### Characters:
                List the characters and provide a description if possible.

                ### Trivia:
                Hos long is the movie and what are the interesting things people like about the movie?

                ### Series Information:
                Is this part of a series? What are the other movies in the series? Where does it fit in?

                ### Similar Movies:
                Recommend four other movies that are similar to '{query}' based on genre and theme.
                """

                # Generate content using the prompt and the image
                response = vision_model.generate_content([prompt, image])

                # Check if the response contains the expected Movie title
                if query.lower() in response.text.lower():
                    # Display response
                    st.markdown(response.text)
                else:
                    # Movie not found error message
                    st.error(f"The context you provided does not mention the Movie '{query}'. Therefore, I cannot extract the requested data from the provided context. Please try again with another Movie.")

if __name__ == "__main__":
    main()
