from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .models import get_user_email, generate_unique_id

# Complete. 
@action('index')
@action.uses('index.html', db, auth.user)
def index():
    print("In the topical")
    return dict(
        get_home_url = URL('/get_home')
        # Complete. 
    )

@action('/get_home')
@action.uses(db, auth.user)
def get_home():
    print("In the get home")
    return dict(status = 200, posts = [], tags = [])

def find_hashtags(text):
    hashtags = []
    # Split the text into words
    words = text.split()
    # Iterate over the words and add hashtags to the list
    for word in words:
        if word.startswith("#"):
            hashtags.append(word)
    return hashtags

@action('/make_post', method='POST')
@action.uses(db, auth.user)
def make_post():
    print("Making a post: ")
    post_content = request.json.get('post_content')
    print("Post to make: ", post_content)
    print("Tags extracted: ", find_hashtags(post_content))


    return dict(status = 200)