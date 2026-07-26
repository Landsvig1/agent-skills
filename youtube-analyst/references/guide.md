# YouTube Analysis Guide

## Metrics Definitions

- **Engagement Rate**: (Likes + Comments) / Views * 100
- **Sentiment Score**: A heuristic based on keyword matching (Positive vs Negative words).
- **Active Rate**: Total Comments / Views * 100

## API Limitations

- **Quota**: YouTube Data API v3 has a daily quota (usually 10,000 units).
- **Search Cost**: 100 units per request.
- **Video/Channel Stats**: 1 unit per request.
- **Comments**: 1 unit per request.

## Workflow Example

1. **Search**: Find relevant videos for a topic.
2. **Filter**: Identify top-performing videos by views/likes.
3. **Analyze**: Retrieve comments for the top videos and run sentiment analysis.
4. **Synthesis**: Compare engagement rates and sentiment across the found set to identify what content resonates most.
