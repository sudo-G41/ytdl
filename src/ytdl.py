import yt_dlp
import time

# URLS = ["https://youtu.be/CupFQnoO_28"]

def download_audio_only(URL):
    now_time = str(int(time.time()*1000000))
        
    def format_selector(ctx):
        formats = ctx.get('formats')[::-1]
        best_audio = None
        best_audio = next(f for f in formats
                        if f['vcodec'] == 'none' and f['acodec'] != 'none')
        
        print(f"{best_audio['acodec']}")
        
        yield {
            'format_id': f'{best_audio["format_id"]}',
            'ext': best_audio['ext'],
            'requested_formats': [best_audio],
            'protocol': f'{best_audio["protocol"]}'
        }

    ydl_opts = {
        'format': format_selector,
        'outtmpl': u'download/%(id)s'+now_time+u'.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)
        
    return now_time

def download_video(URL):
    now_time = str(int(time.time()*1000000))
    def format_selector(ctx):
        """ Select the best video and the best audio that won't result in an mkv.
        NOTE: This is just an example and does not handle all cases """

        # formats are already sorted worst to best
        formats = ctx.get('formats')[::-1]

        # acodec='none' means there is no audio
        best_video = next(f for f in formats
                        if f['vcodec'] != 'none' and f['acodec'] != 'none')
        
        # These are the minimum required fields for a merged format
        yield {
            'format_id': f'{best_video["format_id"]}',
            'ext': best_video['ext'],
            'requested_formats': [best_video],
            # Must be + separated list of protocols
            'protocol': f'{best_video["protocol"]}'
        }

    ydl_opts = {
        'format': format_selector,
        'outtmpl': u'download/%(id)s'+now_time+u'.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)

    return now_time

def ytdl_test():
    print("test success")
