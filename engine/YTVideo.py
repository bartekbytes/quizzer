from pytubefix import YouTube

class YTVideo:
    type = "YouTube Video"

    def __init__(self):
        self.__video_id = None
        self.__title = None
        self.__author = None
        self.__length = None
        self.__keywords = None
        self.__thumbnail_url = None


    def __init__(self, video_id: str, title: str = None, author: str = None, length: int = None, keywords: list[str] = None, thumbnail_url: str = None):
        self.__video_id = video_id
        self.__title = title
        self.__author = author
        self.__length = length
        self.__keywords = keywords
        self.__thumbnail_url = thumbnail_url

    @classmethod
    def video_type(cls):
        return cls.type

    def get_video_id(self):
        return self.__video_id
    
    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def get_length(self):
        return self.__length
    
    def get_keywords(self):
        return self.__keywords
    
    def get_thumbnail_url(self):
        return self.__thumbnail_url
    