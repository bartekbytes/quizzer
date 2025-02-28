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
    def clean_text(text):
        text = text.lower()  # Normalize text to lowercase
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = text.strip()  # Remove leading/trailing spaces
        return text

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