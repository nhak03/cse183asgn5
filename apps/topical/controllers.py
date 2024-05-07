from py4web import action, request, URL
from yatl.helpers import A
from .common import auth
from .models import db

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