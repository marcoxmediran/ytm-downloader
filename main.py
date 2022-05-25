# requires youtube-dl, ffmpeg, and curl installed locally

from subprocess import getoutput
from os import system

def main():
    LINK = '"' + input("YTM Song Link: ") + '"'
    ID = LINK[35:46]

    # download song and save name
    NAME = getoutput("youtube-dl --restrict-filenames --get-filename --no-playlist -o '%(title)s' " + LINK)
    system("youtube-dl -q -x --restrict-filenames --audio-format mp3 --audio-quality 0 --add-metadata --no-playlist -o '~/music/%(title)s.%(ext)s' " + LINK)

    # download album art
    IMG = '"' + "https://i.ytimg.com/vi_webp/" + ID + "/maxresdefault.webp" + '"' + " --output ~/music/art.png"
    system("curl -s " + IMG)

    # crop image
    system("ffmpeg -hide_banner -i ~/music/art.png -vf crop=720:720:280:0 ~/music/crop.png")

    # add album art
    system("mv ~/music/" + NAME + ".mp3 ~/music/raw.mp3")
    system("ffmpeg -hide_banner -i ~/music/raw.mp3 -i ~/music/crop.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Album Cover' ~/music/new.mp3")

    # cleanup
    system("mv ~/music/new.mp3 ~/music/" + NAME + ".mp3")
    system("rm ~/music/raw.mp3")
    system("rm ~/music/*.png")

    print("Downloaded " + NAME)

if __name__ == "__main__":
    main()
