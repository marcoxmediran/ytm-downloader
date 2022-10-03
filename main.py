import sys
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from os import remove
from PIL import Image
from requests import get
from sys import argv
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
    while True:
        try:
            # extract song ID from song link
            LINK = input("LINK: ") 
            ID_START = LINK.find('=') + 1
            ID_END = ID_START + 11
            ID = LINK[ID_START:ID_END]

            # download song and save name
            with YoutubeDL(opts) as ydl:
                ydl.download([ID])
                info = ydl.extract_info(ID, download=False)
                NAME = ydl.prepare_filename(info)[:-4] + "mp3"

            # download album art
            cover = get('https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(ID))
            open("cover.jpg","wb").write(cover.content)

            # crop image
            cover = Image.open(r"cover.jpg")
            cover = cover.crop((280, 0, 1000, 720))
            cover = cover.save("cover.jpg")

            # add album art
            song = MP3(NAME, ID3 = ID3)
            song.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open('cover.jpg','rb').read()))
            song.save()

            # cleanup
            remove('cover.jpg')
            print("Downloaded {}".format(NAME))
        
        except EOFError:
            print()
            print("Program exit")
            exit(0)

if __name__ == "__main__":
    main()
