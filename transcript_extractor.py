from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube

from transformers import pipeline
import re

class YTVideo():
    video_id: int
    ULR: str

    def __init__(self):
        self.video_id = None
        pass

    def __init__(self, video_id: int = None, URL: str = None):
        self.video_id = video_id
        self.URL = URL

    #@staticmethod
    #def get_details() -> dict:


def get_video_details(video_id: str):
    video = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    print(video.author)
    print(video.captions)
    print(video.caption_tracks)
    print(video.channel_id)
    print(video.channel_url)
    print(video.chapters)
    print(video.description)
    print(video.keywords)
    print(video.length)
    print(video.likes)
    print(video.metadata)
    print(video.thumbnail_url)
    print(video.title)
    print(video.replayed_heatmap)
    print(video.publish_date)
    print(video.views)
    #print(video.vid_details)
    #print(video.vid_info)

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

    #get_video_details(**par)

    from engine.helpers import convert_seconds_to_text

    t = convert_seconds_to_text(61, language="pl")
    print(t)
    t = convert_seconds_to_text(61, language="zh")
    print(t)

    t = convert_seconds_to_text(8645, language="pl")
    print(t)
    t = convert_seconds_to_text(8645, language="zh")
    print(t)



    #txt = extract_transcript(**par)
    #print("Full text")
    #print(txt)
    #txts = summary_transcript(text=txt)
    #print("summary")
    #print(txts)
