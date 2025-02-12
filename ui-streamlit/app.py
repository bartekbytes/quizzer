import streamlit as st
from pytubefix import YouTube
from math import floor

def seconds_to_text(seconds: int) -> str:
    final = ""
    minutes = floor(seconds/60.0)
    if minutes == 1:
        final = str(minutes) + " minute, "
    else:
        final = str(minutes) + " minutes, "
    rest_of_seconds = seconds - minutes*60
    return final + str(rest_of_seconds) + " seconds"

@st.cache_data
def get_video_details():
    video = YouTube(f'https://www.youtube.com/watch?v={st.session_state.video_id}')
    st.session_state['v_author'] = video.author
    st.session_state['v_title'] = video.title
    st.session_state['v_length'] = video.length
    st.session_state['v_keywords'] = video.keywords
    st.session_state['v_thumbnail_url'] = video.thumbnail_url


if 'v_author' not in st.session_state:
    st.session_state['v_author'] = ''
if 'v_title' not in st.session_state:
    st.session_state['v_title'] = ''
if 'v_length' not in st.session_state:
    st.session_state['v_length'] = ''
if 'v_keywords' not in st.session_state:
    st.session_state['v_keywords'] = ''
if 'v_thumbnail_url' not in st.session_state:
    st.session_state['v_thumbnail_url'] = ''


st.title("QuiZZer")


video_id = st.text_input("Provide a YT video id", key="video_id")
st.button(label="Get Info", on_click=get_video_details)

wht, val  = st.columns(2, vertical_alignment="bottom")
with wht:
    st.write("Author:")
    st.write("Title:")
    st.write("Length:")
    #st.write("Keywords:")
with val:
    st.write(st.session_state.v_author)
    st.write(st.session_state.v_title)
    st.write(seconds_to_text(st.session_state.v_length))
    #st.write([x for x in st.session_state.v_keywords])


#st.write(f"Info about movie, Author {st.session_state.v_author}, Title {st.session_state.v_title}, Length {st.session_state.v_length}, Keywords {st.session_state.v_keywords}")
st.image(image=st.session_state.v_thumbnail_url)