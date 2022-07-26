import sys
from os import system
from yt_dlp import YoutubeDL

opts = {
    'noplaylist': True,
    'restrictfilenames': True,
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    },{
        'key': 'FFmpegMetadata',
    }]
}

def main():
    arguments = len(sys.argv)
    if (arguments != 2):
        print("Usage: python main.py ID")
        exit(1)
    
    ID = sys.argv[1]

    # download song and save name
    with YoutubeDL(opts) as ydl:
        ydl.download([ID])
        info = ydl.extract_info(ID, download=False)
        NAME = ydl.prepare_filename(info)[:-4] + "mp3"

    # download album art
    system("curl -s 'https://i.ytimg.com/vi_webp/{}/maxresdefault.webp' --output art.png".format(ID))

    # crop image
    system("ffmpeg -loglevel 8 -i art.png -vf crop=720:720:280:0 crop.png")

    # add album art
    system("ffmpeg -loglevel 8 -i {} -i crop.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Album Cover' new.mp3".format(NAME))

    # cleanup
    system("mv new.mp3 ~/music/{}".format(NAME))
    system("rm {}".format(NAME))
    system("rm *.png")

    print("Downloaded {}".format(NAME))

if __name__ == "__main__":
    main()
