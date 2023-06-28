from fastapi import FastAPI
from instaloader import Instaloader, Profile

app = FastAPI()

# Function to calculate engagement rate
def calculate_engagement_rate(likes, comments, followers, posts):
    # Check to avoid ZeroDivisionError
    if followers * posts == 0:
        engagement_rate = 0
    else:
        engagement_rate = (likes + comments) / (followers * posts) * 100
    return engagement_rate

# API endpoint to get Instagram stats
@app.get("/instagram-stats/{username}")
def get_instagram_stats(username: str, top_posts_count: int = 5):
    loader = Instaloader()
    profile = Profile.from_username(loader.context, username)

    num_followers = profile.followers
    total_likes = 0
    total_comments = 0
    total_posts = 0
    top_posts = []

    # Iterate through posts for stats and top posts
    for post in profile.get_posts():
        total_likes += post.likes
        total_comments += post.comments
        total_posts += 1
        if len(top_posts) < top_posts_count:
            top_posts.append({'url': post.url, 'likes': post.likes, 'comments': post.comments})

    engagement_rate = calculate_engagement_rate(total_likes, total_comments, num_followers, total_posts)

    # Check to avoid ZeroDivisionError
    if total_posts == 0:
        estimated_reach = 0
        average_likes_per_post = 0
    else:
        estimated_reach = (total_likes + total_comments) / total_posts
        average_likes_per_post = total_likes / total_posts

    potential_impact = engagement_rate * num_followers
    potential_reach = estimated_reach * num_followers
    influence = potential_impact + potential_reach

    # Return all computed values and stats
    return {
        'username': username,
        'posts': total_posts,
        'followers': num_followers,
        'engagement_rate': engagement_rate,
        'estimated_reach': estimated_reach,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'potential_impact': potential_impact,
        'potential_reach': potential_reach,
        'influence': influence,
        'average_likes_per_post': average_likes_per_post,
        'top_posts': top_posts
    }

# To run, install necessary packages and use uvicorn:
# pip install fastapi uvicorn instaloader
# uvicorn yourscript:app --reload
