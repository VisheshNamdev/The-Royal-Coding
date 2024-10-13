from .models import  Bookmark , Upvote , Devote
import os
import requests
from datetime import timedelta, date
from flask import flash
from .models import db

def get_number_of_users_saved(blog_id):

    bookmarks = Bookmark.query.filter_by(blog_id=blog_id).all()
    user_ids = set(bookmark.user_id for bookmark in bookmarks)   
    num_users_saved = len(user_ids)
    return num_users_saved

def get_number_of_users_upvoted(blog_id):

    upvotes = Upvote.query.filter_by(blog_id=blog_id).all()
    user_ids = set(upvote.user_id for upvote in upvotes)   
    num_users_upvoted = len(user_ids)
    return num_users_upvoted

def get_number_of_users_devoted(blog_id):

    devotes = Devote.query.filter_by(blog_id=blog_id).all()
    user_ids = set(devote.user_id for devote in devotes)   
    num_users_devoted = len(user_ids)
    return num_users_devoted


def img_unplash(title):
    query = f"{title} programming"
    access_key = os.getenv("UNPLASH_ACCESS_KEY")
    url = f'https://api.unsplash.com/search/photos?query={query}&client_id={access_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            return image_url
        else:
            return None
    else:
        return None



def update_streak(user):
    if user.last_post_date == date.today():
        # If the user has already posted today, do not update the streak
        return

    # Update streak if last post date is not today
    if user.last_post_date == date.today() - timedelta(days=1):
        user.daily_streak += 1  # Increment streak if last post was yesterday
    else:
        user.daily_streak = 1  # Reset streak if last post was not yesterday or earlier

    user.last_post_date = date.today()
    
    # Check streak milestones and update coins accordingly
    if user.daily_streak == 7:
        user.coins += 3
        flash("Congratulations! You've reached a 7-day streak. +3 coins added to your account.", "info")
    elif user.daily_streak == 15:
        user.coins += 6
        flash("Congratulations! You've reached a 15-day streak. +6 coins added to your account.", "info")
    elif user.daily_streak == 30:
        user.coins += 10
        flash("Congratulations! You've reached a 30-day streak. +10 coins added to your account.", "info")
    
    db.session.commit()