import sys
import requests
import os
from yt_dlp import YoutubeDL
from PIL import Image

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
    # get song link via command line argument
    arguments = len(sys.argv)
    if (arguments != 2):
        print("Usage: python main.py LINK")
        exit(1)

    # extract song ID from song link
    LINK = sys.argv[1]
    ID = LINK[LINK.find('=') + 1:LINK.find('&')]

    # download song and save name
    with YoutubeDL(opts) as ydl:
        ydl.download([ID])
        info = ydl.extract_info(ID, download=False)
        NAME = ydl.prepare_filename(info)[:-4] + "mp3"

    # download album art
    art = requests.get('https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(ID))
    open("art.jpg","wb").write(art.content)

    # crop image
    cover = Image.open(r"art.jpg")
    cover.crop((280, 0, 1000, 720))
    cover.save("art.jpg")

    # add album art
    os.system("ffmpeg -loglevel 8 -i {} -i crop.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Album Cover' new.mp3".format(NAME))

    # cleanup
    os.system("mv new.mp3 ~/music/{}".format(NAME))
    os.system("rm {}".format(NAME))
    os.system("rm *.jpg")

    print("Downloaded {}".format(NAME))

if __name__ == "__main__":
    main()
