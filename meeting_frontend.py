import streamlit as st
import modal
import json
import os

def main():
    st.title("Meeting Insights")

    # Left section - Input fields
    st.sidebar.header("Meetings")

    available_meetings_info = create_dict_from_json_files('/content/meetings/')

    # Dropdown box
    st.sidebar.subheader("Available Meetings")
    selected_meetings = st.sidebar.selectbox("Select Meeting", options=available_meetings_info.keys())

    if selected_meetings:

        meeting_info = available_meetings_info[selected_meetings]

        # Right section - Newsletter content
        st.header("Newsletter Content")

        # Display the meeting title
        st.write(meeting_info['meeting_details'])

        # Display the meeting summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the meeting summary
            st.subheader("Meeting Session Summary")
            st.write(meeting_info['meeting_summary'])

        with col2:
            import random
            images = ["https://picsum.photos/300?random=6", "https://picsum.photos/300?random=5", "https://picsum.photos/300?random=4", "https://picsum.photos/300?random=3"]
            st.image(random.choice(images), caption="Podcast Cover", width=300, use_column_width=True)


        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = meeting_info['meeting_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Meeting link")
    url = st.sidebar.text_input("Link to meeting")

    process_button = st.sidebar.button("Process Meeting")
    st.sidebar.markdown("**Note**: Meeting processing can take upto 5 mins, please be patient.")

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        meeting_info = process_meeting_info(url)

        # Right section - Newsletter content
        st.header("Newsletter Content")

        # Display the meeting title
        st.subheader("Meeting Title")
        st.write(meeting_info['meeting_details']['meeting_title'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Meeting Summary")
            st.write(meeting_info['Meetng_summary'])

        with col2:
            st.image(meeting_info['meeting_details']['meeting_image'], caption="Meeting Cover", width=300, use_column_width=True)


        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = meeting_info['meeting_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            meeting_info = json.load(file)
            meeting_name = meeting_info['meeting_details']['meeting_title']
            # Process the file data as needed
            data_dict[meeting_name] = meeting_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("stackup-meeting-project", "process_meeting")
    output = f.call(url, '/content/meetings/')
    return output

if __name__ == '__main__':
    main()
