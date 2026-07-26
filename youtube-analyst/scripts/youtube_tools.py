import argparse
import os
import json
import sys
from googleapiclient.discovery import build

def get_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def search_videos(service, query, max_results=5):
    request = service.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video'
    )
    return request.execute()

def get_video_stats(service, video_ids):
    request = service.videos().list(
        part='statistics,snippet,contentDetails',
        id=','.join(video_ids)
    )
    return request.execute()

def get_comments(service, video_id, max_results=50):
    try:
        request = service.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            textFormat='plainText'
        )
        return request.execute()
    except Exception as e:
        return {"error": str(e)}

def analyze_sentiment(comments_data):
    if "error" in comments_data:
        return comments_data
    
    positive_words = {'great', 'awesome', 'excellent', 'good', 'love', 'amazing', 'best', 'informative', 'helpful'}
    negative_words = {'bad', 'terrible', 'worst', 'poor', 'hate', 'boring', 'useless', 'wrong'}
    
    results = []
    for item in comments_data.get('items', []):
        text = item['snippet']['topLevelComment']['snippet']['textDisplay'].lower()
        score = 0
        for word in positive_words:
            if word in text: score += 1
        for word in negative_words:
            if word in text: score -= 1
        
        sentiment = 'neutral'
        if score > 0: sentiment = 'positive'
        elif score < 0: sentiment = 'negative'
        
        results.append({
            'text': text[:100] + '...',
            'sentiment': sentiment,
            'score': score
        })
    
    return results

def main():
    parser = argparse.ArgumentParser(description='YouTube Analyst Tools')
    parser.add_argument('--api-key', required=True, help='YouTube Data API Key')
    parser.add_argument('--action', required=True, choices=['search', 'stats', 'comments', 'analyze'], help='Action to perform')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--ids', help='Comma-separated video IDs')
    parser.add_argument('--video-id', help='Single video ID for comments')
    parser.add_argument('--max-results', type=int, default=5, help='Max results')

    args = parser.parse_args()
    service = get_service(args.api_key)

    try:
        if args.action == 'search':
            result = search_videos(service, args.query, args.max_results)
        elif args.action == 'stats':
            result = get_video_stats(service, args.ids.split(','))
        elif args.action == 'comments':
            result = get_comments(service, args.video_id, args.max_results)
        elif args.action == 'analyze':
            comments = get_comments(service, args.video_id, args.max_results)
            result = analyze_sentiment(comments)
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
