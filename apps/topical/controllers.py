from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .models import get_user_email, generate_unique_id, get_time

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
    # # quick way to clear db tables:
    # db.post.truncate()
    # # Empty the 'tag' table
    # db.tag.truncate()
    # # Commit the changes to the database
    # db.commit()

    print("In the get home")

    posts = db().select(orderby=(~db.post.id)).as_list()
    print("Posts: ", posts)
    tags = db().select(orderby=(db.tag.id)).as_list()
    logged_in_email = get_user_email()
    if (not logged_in_email):
        logged_in_email = ''
    print("Tags: ", tags)
    print("Associated email: ", logged_in_email)
    return dict(status = 200, posts = posts, tags = tags, logged_in_email = logged_in_email)

def find_hashtags(text):
    hashtags = []
    # Split the text into words
    words = text.split()
    # Iterate over the words and add hashtags to the list
    for word in words:
        if word.startswith("#"):
            # might have to do additional text cleanup
            hashtag = (word[1:]).strip("!,.?")
            hashtags.append(hashtag)
    return hashtags

@action('/make_post', method='POST')
@action.uses(db, auth.user)
def make_post():
    print("Making a post: ")
    post_content = request.json.get('post_content')
    print("Post to make: ", post_content)
    tags_in_post = find_hashtags(post_content)

    print("Tags extracted: ", tags_in_post)

    post_id = db.post.insert(user_email = get_user_email(), post_id = generate_unique_id(), tags = tags_in_post, content = post_content, timestamp = get_time)
    if not post_id:
        return dict(status = 500, error = "error on post insertion")

    for tag in tags_in_post:
        stored_tag = db(db.tag.name == tag).select().first()
        if stored_tag:
            # previous_amount = stored_tag.amount
            stored_tag.amount += 1
            stored_tag.update_record()
            # print("That tag amount incremented by 1")
            # print("Prior: ", previous_amount)
            # print("New: ", stored_tag.amount)
        else:
            tag_id = db.tag.insert(name = tag, amount = 1)
            if not tag_id:
                return dict(status = 500, error = "error on tag insertion")

    return dict(status = 200)

@action('/delete_post', method='POST')
@action.uses(db, auth.user)
def delete_post():
    postID_to_delete = request.json.get('post_id')
    email = request.json.get('post_email')

    print("Deleting post id: ", postID_to_delete)
    print("Author email: ", email)

    post_to_delete = db(db.post.post_id == postID_to_delete).select().first()

    print("post_to_delete.content: ", post_to_delete.content)

    # print("post_to_delete.tags: ", post_to_delete.tags)

    tags_to_decrement = post_to_delete.tags

    for tag in tags_to_decrement:
        stored_tag = db(db.tag.name == tag).select().first()
        if stored_tag:
            # previous_amount = stored_tag.amount
            stored_tag.amount -= 1
            stored_tag.update_record()
            if(stored_tag.amount <= 0):
                stored_tag.delete_record()
        else:
            return dict(status = 500, error = "error on tag decrementation")
        
    post_to_delete.delete_record()
    db.commit()
        
    return dict(status = 200)