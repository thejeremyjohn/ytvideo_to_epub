from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import requests
import subprocess
import tempfile


def video_attrs(yt_url: str) -> dict:
    url = 'https://www.youtube.com/oembed'
    querystring = {'url': yt_url}
    r = requests.get(url, params=querystring)
    return r.json()


def filename_safe(s: str) -> str:
    return ''.join(x if (x.isalnum() or x in "._- ") else '_' for x in s)


def image_url_to_file(image_url: str, dir=Path('.')) -> Path:
    image_file = dir.joinpath(f"image{Path(image_url).suffix}")
    r = requests.get(image_url)
    with image_file.open('wb') as f:
        f.write(r.content)
    return image_file


YT_URL = 'https://www.youtube.com/watch?v=09PICbN1A-c'
attrs = video_attrs(YT_URL)
channel = attrs['author_name']
title = attrs['title']
title_filename = filename_safe(f"{channel} - {title}")
v_id = parse_qs(urlparse(YT_URL).query)['v'][0]

print(f"video {channel=} {title=} {v_id=}")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp = Path(tmpdir)

    print('fetching transcript text ...')
    text = f"-\n( {YT_URL= } )\n"
    transcript_list = YouTubeTranscriptApi().list(v_id)
    for transcript in transcript_list:
        fetched_transcript = transcript.fetch()
        for snippet in fetched_transcript:
            if snippet.text.startswith('>>'):  # another voice chimed in
                text += '\n'
            text += snippet.text + ' '
        text += f"\n*** END OF {transcript.language.upper()} TRANSCRIPT ***\n"

    print(f"saving transcript to (temporary) text_file ...")
    text_file = tmp.joinpath(f"{title_filename}.txt")
    text_file.write_text(text)

    print(f"saving thumbnail to (temporary) image file ...")
    thumbnail_file = image_url_to_file(attrs['thumbnail_url'], dir=tmp)

    print('converting text_file to epub ...')
    epub_file = tmp.joinpath(f"{title_filename}.epub")
    subprocess.run([
        'txt2epub', 'convert',
        '-i', f"{text_file.absolute()}",
        '-o', f"{epub_file.absolute()}",
        '-t', f"{title}",
        '-a', f"{channel}",
        '-c', f"{thumbnail_file.absolute()}",
    ])

    print(f'moving epub to google drive ( ebooks/yt_transcripts/{title_filename}.epub ) ...')
    destination = Path('/run/user/1000/gvfs/google-drive:host=gmail.com,user=thejeremyjohn/') \
        .joinpath('My Drive/ebooks/yt_transcripts/')  # ^^^ gvfs-mounted google drive
    subprocess.run(f'mv "{epub_file}" "{destination}"', shell=True)
