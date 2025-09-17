# usage:
# python ytvideo_to_epub.py https://www.youtube.com/watch?v=gtBIPF2aMys

from dotenv import load_dotenv; load_dotenv()
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
import io
import os
import requests
import subprocess
import sys
import tempfile


def video_attrs(yt_url: str) -> dict:
    url = 'https://www.youtube.com/oembed'
    r = requests.get(url, params={'url': yt_url})
    return r.json()


def filename_safe(s: str) -> str:
    def is_safe(c): return c.isalnum() or c in '._- '
    return ''.join(x if is_safe(x) else '_' for x in s)


def image_url_to_file(image_url: str, dir=Path('.')) -> Path:
    image_file = dir.joinpath(f"image{Path(image_url).suffix}")
    r = requests.get(image_url)
    with image_file.open('wb') as f:
        f.write(r.content)
    return image_file


def fetch_transcript_text(YT_URL: str) -> str:
    text = f"-\n( {YT_URL= } )\n"
    v_id = parse_qs(urlparse(YT_URL).query)['v'][0]

    proxy_config = None if not os.environ.get('PROXY_URL') \
        else GenericProxyConfig(https_url=os.environ['PROXY_URL'])
    transcript_list = YouTubeTranscriptApi(proxy_config).list(v_id)

    for transcript in transcript_list:
        fetched_transcript = transcript.fetch()
        for snippet in fetched_transcript:
            if snippet.text.startswith('>>'):  # another voice chimed in
                text += '\n'
            text += snippet.text + ' '
        text += f"\n*** END OF {transcript.language.upper()} TRANSCRIPT ***\n"
    return text


def ytvideo_to_epub(YT_URL: str, mv_to_gdrive=True) -> (tuple[str, io.BytesIO] | None):
    attrs = video_attrs(YT_URL)
    channel = attrs['author_name']
    title = attrs['title']
    title_filename = filename_safe(f"{channel} - {title}")
    print(f"video {channel=} {title=}")

    print('fetching transcript text ...')
    text = fetch_transcript_text(YT_URL)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        print(f"saving transcript to (temporary) txt file ...")
        text_file = tmp.joinpath(f"{title_filename}.txt")
        text_file.write_text(text)

        print(f"saving thumbnail to (temporary) image file ...")
        thumbnail_file = image_url_to_file(attrs['thumbnail_url'], dir=tmp)

        print('converting text_file to epub ...')
        epub_file = tmp.joinpath(f"{title_filename}.epub")
        subprocess.run([
            sys.executable, '-m',
            'txt2epub', 'convert',
            '-i', f"{text_file.absolute()}",
            '-o', f"{epub_file.absolute()}",
            '-t', f"{title}",
            '-a', f"{channel}",
            '-c', f"{thumbnail_file.absolute()}",
        ], capture_output=True, text=True)

        if mv_to_gdrive:
            print(
                f'moving epub to google drive ( ebooks/yt_transcripts/{title_filename}.epub ) ...')
            destination = Path('/run/user/1000/gvfs/google-drive:host=gmail.com,user=thejeremyjohn/') \
                .joinpath('My Drive/ebooks/yt_transcripts/')  # ^^^ gvfs-mounted google drive
            subprocess.run(f'mv "{epub_file}" "{destination}"', shell=True)
        else:
            return (epub_file.name, io.BytesIO(epub_file.read_bytes()))


if __name__ == '__main__':
    assert len(sys.argv) > 1, "expected yt_url positional argument"
    ytvideo_to_epub(sys.argv[1])
