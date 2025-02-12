from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube

from transformers import pipeline
import re

from YTVideo import YTVideo
from utils.helpers import convert_seconds_to_text


def get_video_details(video_id: str) -> YTVideo:
    video = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    #print(video.author)
    #print(video.captions)
    #print(video.caption_tracks)
    #print(video.channel_id)
    #print(video.channel_url)
    #print(video.chapters)
    #print(video.description)
    #print(video.keywords)
    #print(video.length)
    #print(video.likes)
    #print(video.metadata)
    #print(video.thumbnail_url)
    #print(video.title)
    #print(video.replayed_heatmap)
    #print(video.publish_date)
    #print(video.views)

    params = {
        "video_id": video_id,
        "title": video.title,
        "author": video.author,
        "description": video.description,
        "length": video.length,
        "keywords": video.keywords,
        "thumbnail_url": video.thumbnail_url
    }

    ytv = YTVideo(**params)
    return ytv


#def extract_transcript(video_id: str) -> str | None:
#    if video_id is None:
#        return None
#    
#    transcripts = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
#    if transcripts is not None:
#        print(transcripts)
#        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['en'])
#        transcript_text = " ".join([entry['text'] for entry in transcript])
#        return transcript_text
#    else:
#        print("Transcripts dont exist")
#        return None
    

#def clean_transcript(s: str) -> str:
#    s = s.lower()
#    s = s.split()
#    s = " ".join(s)
#    s = re.sub(f'[{re.escape(string.punctuation)}]', '', s)
#    return s



#def summary_transcript(text: str):
#    print("Summarized")
#    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#    summary = summarizer(text, max_length=150, min_length=40, do_sample=False) 
#    return summary[0]['summary_text']


if __name__ == '__main__':
    
    par = { 
        'video_id': 'Rtrqb-FgKCs' # '71rDL2Q3jvw' 
        }

    ytv = get_video_details(**par)

    print("Info about video")
    print(f"Title: {ytv.get_title()}")
    print(f"Author: {ytv.get_author()}")
    print(f"Description: {ytv.get_description()}")
    print(f"Length: {convert_seconds_to_text(int(ytv.get_length()))}")
    print(f"Keywords : {ytv.get_keywords()}")



    from engine.Engine import Engine

    #transcript = extract_transcript(**par)
    #print(transcript)
    video_transcript = Engine.extract_transcript(ytv.get_video_id())
    print("Video Transcript")
    print(video_transcript)

    
    print("Video Transcript Summary")
    #print(summary_transcript(transcript))
    video_transcript_summary = Engine.summary_transcript(video_transcript)
    print(video_transcript_summary)

