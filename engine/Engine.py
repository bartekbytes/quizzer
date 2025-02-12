from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube

from transformers import pipeline
import re
import string

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
