import streamlit as st
from pytubefix import YouTube
from math import floor
from helpers import convert_seconds_to_text, extract_video_id, check_video_existence





def clean_text(text):
    text = text.lower()  # Normalize text to lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading/trailing spaces
    return text


# begin class Engine

from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube

from transformers import pipeline
import re
import string

from openai import OpenAI


from dotenv import load_dotenv
import os

from sklearn.feature_extraction.text import TfidfVectorizer
import re

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class Engine:

    @staticmethod
    def extract_transcript(video_id: str) -> str | None:
        if video_id is None:
            return None
    
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
        
        if transcripts is not None:
            #print(transcripts)
            transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['en'])
            transcript_text = " ".join([entry['text'] for entry in transcript])
            return transcript_text
        else:
            print("Transcripts don't exist")
            return None
        
    @staticmethod
    def clean_transcript(text: str) -> str:
        text = text.lower()
        text = text.split()
        text = " ".join(text)
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        return text

    @staticmethod
    def summary_transcript(text: str) -> str | None:
        try:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary = summarizer(text, max_length=150, min_length=40, do_sample=False) 
            return summary[0]['summary_text']
        except RuntimeError as re:
            print(f"Summarization Runtime Error: {re}")
        except:
            print("Other Error")

    @staticmethod
    def generate_quiz(text: str, number_questions: int, keywords: list[str]) -> str:
    
        prompt = f"""
        You are an assistant that generates a quiz based on the given text.
        Based on the given text that you find in section that starts with [TEXT],
        generate {str(number_questions)} quiz questions to this text.
        Pay attention to main keywords: {keywords}

        For each question, generate between 2 to 5 answers. Make the answers realistically.
        Please make sure that only one answer for each question is true.
        Make possible answers for the given question realistically between rach other.

        This is the text
        [TEXT]
        {text}

        Please, generate the output in a tabular form, but without any borders. It must be a csv format:
        Question1,Possible Answer1 to Question1|Possible Answer2 to Question1|...|Possible AnswerN to Question1,Correct answer to Question1
        Question2,"Possible Answer1 to Question2|Possible Answer2 to Question2|...|Possible AnswerN to Question2,Correct answer to Question2
        """
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            store=False,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                 }
            ]
        )

        res = str(completion.choices[0].message.content)
        return res
    

    @staticmethod
    def tf_idf(text: str) -> list[str]:
        ### TF-IDF

        vectorizer = TfidfVectorizer(stop_words='english', preprocessor=clean_text)
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray().flatten()
        word_scores = list(zip(feature_names, scores))
        sorted_word_scores = sorted(word_scores, key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, score in sorted_word_scores[:5]]  # Top 5 keywords
        
        return top_keywords


# end class Engine


# session state
if 'video_loaded' not in st.session_state:
    st.session_state['video_loaded'] = False
if 'video_transcribed' not in st.session_state:
    st.session_state['video_transcribed'] = False
if 'quiz_generated' not in st.session_state:
    st.session_state['quiz_generated'] = False



if 'v_video_id' not in st.session_state:
    st.session_state['v_video_id'] = ''
if 'v_video_url' not in st.session_state:
    st.session_state['v_video_url'] = ''


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

if 'tfidf_keywords' not in st.session_state:
    st.session_state['tfidf_keywords'] = None
if 'whole_text' not in st.session_state:
    st.session_state['whole_text'] = ""
    

if 'smalled' not in st.session_state:
    st.session_state['smalled'] = False


@st.dialog("YouTube Video")
def video_status(status: bool):
    if status:
        st.write("YouTube video :green[has been found] :sunglasses:")
    else:
        st.write("YouTube video :red[not found] :imp:")


def get_video_details():
    ext_video_id, ext_url = extract_video_id(st.session_state.video_id)
    video_exists = check_video_existence(ext_url)

    if video_exists:
        video_status(True)
        st.session_state['v_video_id'] = ext_video_id
        st.session_state['v_video_url'] = ext_url
        st.session_state['video_loaded'] = True

        video = YouTube(f'https://www.youtube.com/watch?v={ext_video_id}')
        st.session_state['v_author'] = video.author
        st.session_state['v_title'] = video.title
        st.session_state['v_length'] = video.length
        st.session_state['v_keywords'] = video.keywords
        st.session_state['v_thumbnail_url'] = video.thumbnail_url
    else:
        video_status(False)
        st.session_state.video_id = ''



def generate_quiz():
    print("lol")
    print(st.session_state['qg_name'])
    print(st.session_state['qg_type'])
    print(st.session_state['qg_keywords'])
    print(st.session_state['qg_noquestions'])
    quiz = Engine.generate_quiz(text=st.session_state['whole_text'], number_questions=st.session_state['qg_noquestions'], keywords=st.session_state['qg_keywords'])

    f = open("quiz.csv", "w")
    f.write(quiz)
    f.close()

    st.session_state['quiz_generated'] = True






st.title("QuiZZer")


url, btn = st.columns([0.9, 0.1], vertical_alignment="bottom")
with url:
    video_id = st.text_input("Provide a YT video id", key="video_id", value="Rtrqb-FgKCs")
with btn:
    st.button(label="Go!", on_click=get_video_details)


if st.session_state['video_loaded']  == True:
    with st.expander("YouTube Video Details", icon=":material/movie:"):
        wht, val  = st.columns(2, vertical_alignment="top")
        with wht:
            st.write("Author:")
            st.write("Title:")
            st.write("Length:")
            st.write("Keywords:")
    
        with val:
            st.write(st.session_state.v_author)
            st.write(st.session_state.v_title)
            st.write(convert_seconds_to_text(st.session_state.v_length, language='en'))
            
            temp_k = ""
            for k in st.session_state.v_keywords:
                temp_k = temp_k + k + ", "
            
            st.write(temp_k[:-2])

        st.image(image=st.session_state.v_thumbnail_url)

    

        ### Engine - get video transcript, transcript summary, extract keywords
        video_transcript = Engine.extract_transcript(st.session_state['v_video_id'])
        print("Video Transcript:")
        print(video_transcript)
        
        
        

        #video_transcript_summary = Engine.summary_transcript(video_transcript)
        video_transcript_summary = "Bitcoins are digital coins you can send through the internet compared to other Alternatives Bitcoins have a number of advantages Bitcoins are transferred directly from person to person via the net without going through a bank or Clearing House. Bitcoins are a great way for small businesses and Freelancers to get noticed it doesn't cost anything to start accepting them there are no chargebacks or fees."
        print("Video Transcript Summary")
        print(video_transcript_summary)
        st.session_state['whole_text'] = video_transcript_summary
        
        
        key_words = Engine.tf_idf(video_transcript_summary)
        print("TF-Idf Keywords")
        print(key_words)
        print("Video Keywords")
        print(st.session_state['v_keywords'])

        st.session_state['tfidf_keywords'] = key_words
        st.session_state['video_transcribed'] = True

if st.session_state['video_transcribed']:
    with st.expander("Quizz Details", icon=":material/quiz:"):
        
        st.text_input(label="Please, provide your Quiz name", placeholder="Quiz Name", key='qg_name')
        quiz_type = st.selectbox(label="Type of Answers", options=("Single", "Multi"), index=None, placeholder="Select answers type",key='qg_type')

        #list = ["Bitcoin", "Crypto", "History"]
        #list = st.session_state['tfidf_keywords']
        
        # merge list of keywords
        list = st.session_state['v_keywords'] + st.session_state['tfidf_keywords']
        #options = st.multiselect("Select Quiz Topics", list, [])
        #print(options)
        
        
        selected_keywords = st.pills("Select Quiz Topics", list, selection_mode="multi", key='qg_keywords')
        #print(selected_keywords)
        #for x in range(0, len(list)):
            #st.checkbox(label=list[x], key=f"c_{x}")
            #print(f"{list[x]}, {x}")
        number_of_questions = st.slider(label="Number of Questions", min_value=1, max_value=25, value = 5,key='qg_noquestions')
        #print(number_of_questions)
        st.button(label="Generate QuiZZ! :shocked_face_with_exploding_head:", on_click=generate_quiz)

if st.session_state['quiz_generated']:
    with st.expander("Quizz Share/Download", icon=":material/quiz:"):
        share, print, savepdf, beer = st.columns(spec=4,gap="small", vertical_alignment='bottom')
        with share:
            st.button(label="Share Quiz :heartpulse:")
        with print:
            st.button(label="Print Quiz :printer:")
        with savepdf:
            st.button(label="Save Quiz :page_with_curl:")
        with beer:
                st.button(label="Buy me a :beer:")






