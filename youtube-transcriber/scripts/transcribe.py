import argparse
import os
import requests
import sys
import re

def get_video_id(url_or_id):
    if len(url_or_id) == 11:
        return url_or_id
    # Extract ID from various URL formats
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url_or_id)
    return match.group(1) if match else None

def fetch_transcript(video_id, lang=None):
    url = f"https://youtube-transcript.ai/transcript/{video_id}.txt"
    params = {}
    if lang:
        params['lang'] = lang
    
    headers = {'User-Agent': 'Mozilla/5.0'} 
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Received status code {response.status_code}\n{response.text}"

def save_transcript(content, video_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"transcript_{video_id}.md"
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def find_latest_video(creator_name, api_key):
    # This requires YouTube Data API v3
    if not api_key:
        return None, "Error: YOUTUBE_API_KEY required for video discovery."
    
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': creator_name,
        'type': 'video',
        'order': 'date',
        'maxResults': 1,
        'key': api_key
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        title = data['items'][0]['snippet']['title']
        return video_id, title
    return None, "No videos found."

def main():
    parser = argparse.ArgumentParser(description='YouTube Transcriber')
    parser.add_argument('--video', help='Video ID or URL')
    parser.add_argument('--creator', help='Creator name to find latest video')
    parser.add_argument('--api-key', help='YouTube Data API Key (required for --creator)')
    parser.add_argument('--lang', help='Language code (e.g. en, da)')
    parser.add_argument('--output-dir', default='.', help='Output directory')

    args = parser.parse_args()

    video_id = None
    title = "Unknown Video"

    if args.creator:
        api_key = args.api_key or os.environ.get('YOUTUBE_API_KEY')
        video_id, result = find_latest_video(args.creator, api_key)
        if not video_id:
            print(result)
            sys.exit(1)
        title = result
        print(f"Found latest video for {args.creator}: {title} ({video_id})")
    elif args.video:
        video_id = get_video_id(args.video)
        if not video_id:
            print("Error: Invalid Video ID or URL.")
            sys.exit(1)
    else:
        print("Error: Either --video or --creator must be provided.")
        sys.exit(1)

    print(f"Fetching transcript for {video_id}...")
    transcript = fetch_transcript(video_id, args.lang)
    
    if transcript.startswith("Error:"):
        print(transcript)
        sys.exit(1)
    
    saved_path = save_transcript(transcript, video_id, args.output_dir)
    print(f"Transcript saved to: {saved_path}")

if __name__ == '__main__':
    main()
