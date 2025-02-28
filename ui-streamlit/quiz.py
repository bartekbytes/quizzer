import streamlit as st
from pytubefix import YouTube
from math import floor
from helpers import convert_seconds_to_text, extract_video_id, check_video_existence

from dotenv import load_dotenv
import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure




class AtlasClient():
    
    def __init__(self, atlas_uri: str, dbname: str):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def ping_server(self) -> bool:
        try:
            self.mongodb_client.admin.command('ping')
            return True
        except Exception as e:
            print(e)
            return False
        
    def drop_collection(self, collection_name: str) -> bool:

        # drop the collection in case it already exists
        try:
            self.database[collection_name].drop()
            return True

        except OperationFailure:
            print("An authentication error was received. Are your username and password correct in your connection string?")
            return False

    def insert(self, collection_name, operation: str, docs) -> bool:
        try: 
            if operation == "many":
                result = self.database[collection_name].insert_many(docs)
            elif operation == "one":
                result = self.database[collection_name].insert_one(docs)

        except OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
            return False
        else:
            if operation == "many":
                inserted_count = len(result.inserted_ids)
                print("I inserted %x documents." %(inserted_count))
            elif operation == "one":
                print("I inserted a document.")
            return True
        
    def get_quizes(self, collection_name: str):
        docs = self.database[collection_name].find()
        return docs
    
    def get_quiz(self, collection_name: str, criteria: dict):
        doc = self.database[collection_name].find_one(criteria)

        if doc is not None:
            return doc
        else:
            return None


load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DBNAME = os.getenv('MONGODB_DBNAME')
MONGODB_COLLECTIONNAME = os.getenv('MONGODB_COLLECTIONNAME')

# session state


#if 'quiz_name' not in st.session_state:
#    st.session_state['quiz_name'] = ''
if 'quiz_prepared' not in st.session_state:
    st.session_state['quiz_prepared'] = ''
if 'quiz_assessed' not in st.session_state:
    st.session_state['quiz_assessed'] = ''
if 'res' not in st.session_state:
    st.session_state['res'] = ''


def prepare_quiz():
    ac = AtlasClient(atlas_uri=MONGODB_URI, dbname=MONGODB_DBNAME)
    criteria = {"name": st.session_state['quiz_name']}
    res = ac.get_quiz(collection_name=MONGODB_COLLECTIONNAME, criteria=criteria)

    st.session_state['res'] = res
    st.session_state['quiz_prepared'] = True
    st.session_state['quiz_assessed'] = False
    
def assess_quiz():
    st.session_state['quiz_assessed'] = True


st.title("QuiZZer - Solve Your Quiz!")


url, btn = st.columns([0.9, 0.1], vertical_alignment="bottom")
with url:
    video_id = st.text_input("Provide a Quiz Name", key="quiz_name", value="Quiz Viz")
with btn:
    st.button(label="Go!", on_click=prepare_quiz)


if st.session_state['quiz_prepared']  == True:
    with st.expander("Quizz Details", icon=":material/quiz:"):
        q = st.session_state['res']
        st.write(q['name'])

        what, value  = st.columns(2, vertical_alignment="bottom")
        with what:
            st.write("Quiz Name:")
            st.write("Video Id:")
            st.write("Quiz Type:")
            st.write("Number of Q:")
    
        with value:
            st.write(q['name'])
            st.write(q['video_id'])
            st.write(q['type'])
            st.write(q['number_questions'])

        questions = q['questions']
        q_iter = 1
        for x in range(0, len(questions)):
            if x % 2 == 0:
                st.write(f":red[Question {q_iter}]: {questions[x]}")
                q_iter = q_iter + 1
            elif x % 2 != 0:
                answers = questions[x]
                st.write(f":red[Answers]:")
                if q['type'] == 'single':
                    selection = st.pills("", answers, selection_mode="single", key=f"a_{q_iter}")
                elif q['type'] == 'multiple':
                    selection = st.pills("", answers, selection_mode="multi", key=f"a_{q_iter}")

        st.markdown("----", unsafe_allow_html=True)
        columns = st.columns((2, 1, 2))
        button_pressed = columns[1].button(label='Finish Quiz!', on_click=assess_quiz)
        st.markdown("----", unsafe_allow_html=True)
        

        if st.session_state['quiz_assessed']:
            import random
            st.markdown("<h3 style='text-align: center; color: white;'>Your score</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: red;'>{random.randrange(1, q_iter-1, 1)}<span style='color:white'>/{q_iter-1}</span></h1>", unsafe_allow_html=True)
            st.markdown("----", unsafe_allow_html=True)
            share, print, savepdf, beer = st.columns(spec=4, gap="small", vertical_alignment='bottom')
            with share:
                st.button(label="Share Result :heartpulse:")
            with print:
                st.button(label="Print Result :printer:")
            with savepdf:
                st.button(label="Save Result :page_with_curl:")
            with beer:
                st.button(label="Buy me a :beer:")



