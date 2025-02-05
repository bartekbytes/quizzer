from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

def extract_transcript(video_id: str) -> str:
    if video_id is None:
        return None
    
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
    if transcripts is not None:
        print(transcripts)
        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['en'])
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    else:
        print("Transcripts dont exist")
        return None
    

def clean_transcript(s: str) -> str:
    s = s.lower()
    s = s.split()
    s = " ".join(s)
    s = re.sub(f'[{re.escape(string.punctuation)}]', '', s)
    return s


def summary_transcript(text: str):
    print("Summarized")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False) 
    return summary[0]['summary_text']


if __name__ == '__main__':
    par = { 
        'video_id': 'Rtrqb-FgKCs' # '71rDL2Q3jvw' 
        }

    txt = extract_transcript(**par)
    print("Full text")
    print(txt)
    txts = summary_transcript(text=txt)
    print("summary")
    print(txts)
