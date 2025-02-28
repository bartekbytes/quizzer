from math import floor

def convert_seconds_to_text(seconds: int, language="en") -> str:
    
    translations = {
        "en": {"hour": "hour", "hours": "hours", "minute": "minute", "minutes": "minutes", "second": "second", "seconds": "seconds"},
        "es": {"hour": "hora", "hours": "horas", "minute": "minuto", "minutes": "minutos", "second": "segundo", "seconds": "segundos"},
        "fr": {"hour": "heure", "hours": "heures", "minute": "minute", "minutes": "minutes", "second": "seconde", "seconds": "secondes"},
        "pl": {"hour": "godzina", "hours": "godziny", "minute": "minuta", "minutes": "minuty", "second": "sekunda", "seconds": "sekundy"},
        "zh": {"hour": "小时", "hours": "小时", "minute": "分钟", "minutes": "分钟", "second": "秒", "seconds": "秒"}
        # You can add more languages here
    }

    # Fallback to English if language is not recognized
    lang_dict = translations.get(language, translations["en"])
    

    hours = seconds // 3600  # 1 hour = 3600 seconds
    minutes = (seconds % 3600) // 60  # 1 minute = 60 seconds
    remaining_seconds = seconds % 60  # Remaining seconds after minutes are accounted for
    
    time_parts = []

    if hours > 0:
        time_parts.append(f"{hours} {lang_dict['hour']}" if hours == 1 else f"{hours} {lang_dict['hours']}")
    if minutes > 0:
        time_parts.append(f"{minutes} {lang_dict['minute']}" if minutes == 1 else f"{minutes} {lang_dict['minutes']}")
    if remaining_seconds > 0 or (hours == 0 and minutes == 0):  # Show seconds if no hours or minutes
        time_parts.append(f"{remaining_seconds} {lang_dict['second']}" if remaining_seconds == 1 else f"{remaining_seconds} {lang_dict['seconds']}")

    # Join the parts and return as a string
    return ', '.join(time_parts)

def extract_video_id(text: str):
    if text.startswith("http://youtube.com") or text.startswith("https://youtube.com") or text.startswith("www.youtube.com") or text.startswith("youtube.com"):
        video_id = text.split('/').pop()
        url = text
    else:
        video_id = text
        url = f"https://www.youtube.com/watch?v={video_id}"

    return video_id, url

def check_video_existence(url: str) -> bool:
    import requests
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 200:
        return True
    else:
        return False
    