from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app, jsonify,g,abort
from flask_login import current_user, login_required
from . import views
from flask_ckeditor import upload_success, upload_fail
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from .forms import MyForm
from .models import BlogPost, db, Bookmark, Upvote, Devote, BasicPage, Pageadv, Pagemod , User, cpppages, cpages, ContactMessage
from datetime import datetime, timedelta, date
from sqlalchemy.exc import IntegrityError
import os
import re
import bleach
from better_profanity import profanity
import uuid
from .action_utils import (get_number_of_users_saved,get_number_of_users_upvoted,get_number_of_users_devoted,img_unplash,update_streak)
import requests
import asyncio
import aiohttp
from .forms import MyForm 
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()


views = Blueprint("views", __name__)


# Route handling
@views.route("/")
@views.route("/home")
def home():
    f_chars = current_user.username[0].capitalize() if current_user.is_authenticated else None

    return render_template("index.html", user=current_user)



@views.route('/index.html')
def redirect_to_home():
    return redirect('/', code=301)



@views.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # print(name,email,subject,message)
        # Create a new ContactMessage object
        new_message = ContactMessage(name=name, email=email, subject=subject, message=message, created_at=datetime.now())

        # Add the new message to the database session
        
        db.session.add(new_message)
        db.session.commit()
        

        flash("Thank you for your response we we'll contact you soon", 'success' )    
        
    return render_template('contact-us.html',user=current_user)


#------------------------------------------------------rewards---------------------------------------------

@views.route("/rewards")
@login_required
def rewards():
    return render_template("Rewards.html",user=current_user)




#-----------------------------------------------------blog post-------------------------------------------------

@views.route("/posts")
def posts():
    page = request.args.get('page', 1, type=int)  # Get the page number from the query string, default to 1
    per_page = 10  # Number of posts per page
    pagination = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    for post in posts:
        post.content = bleach.clean(post.content, tags=[], strip=True)
    return render_template(
        'Posts.html',
        user=current_user,
        posts=posts,
        pagination=pagination,  # Pass the pagination object to the template
        get_number_of_users_saved=get_number_of_users_saved,
        get_number_of_users_upvoted=get_number_of_users_upvoted,
        get_number_of_users_devoted=get_number_of_users_devoted
    )



#------------------------------------------------------delete blog------------------------------------------

@views.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author != current_user:
        flash("You are not authorized to delete this post.", "error")
        return redirect(url_for('views.posts'))

    try:
        # Delete associated bookmarks, upvotes, and devotes
        Bookmark.query.filter_by(blog_id=post_id).delete()
        Upvote.query.filter_by(blog_id=post_id).delete()
        Devote.query.filter_by(blog_id=post_id).delete()

        # Decrease user's coins by 20
        current_user.coins -= 20

        # Delete the post itself
        db.session.delete(post)
        db.session.commit()

        flash("Post deleted successfully! 20 royal coins deducted from your account.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the post: {str(e)}", "error")

    return redirect(url_for('views.posts'))

#---------------------------------------------------individule blog link-------------------------------------


@views.route('/blog/<post_endpoint>')
def blog(post_endpoint):

    post = BlogPost.query.filter_by(endpoint=post_endpoint).first_or_404()
    return render_template("blog.html", post=post, user=current_user,
                           get_number_of_users_upvoted=get_number_of_users_upvoted,
                           get_number_of_users_devoted=get_number_of_users_devoted,
                           get_number_of_users_saved=get_number_of_users_saved)

    

@views.route("/user/bookmarked")  
@login_required
def bookmarked():    
    saved_posts_id = [bookmark.blog_id for bookmark in current_user.bookmarks]   
    saved_posts = BlogPost.query.filter(BlogPost.id.in_(saved_posts_id)).all()
    for post in saved_posts:
        post.content = bleach.clean(post.content, tags=[], strip=True)  
    return render_template("saveartical.html", user=current_user, posts=saved_posts, get_number_of_users_saved=get_number_of_users_saved)


@views.route('/remove_saved_post/<int:post_id>', methods=['POST'])
@login_required
def remove_saved_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, blog_id=post_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash('Post removed successfully from your saved list.', 'success')
    else:
        flash('Post could not be removed from your saved list.', 'error')
    return redirect(request.referrer or url_for('index'))


@views.route('/upvote/<int:blog_id>', methods=['POST'])
@login_required
def upvote_blog(blog_id):
    user_id = current_user.id

    try:
        
        existing_devote = Devote.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if existing_devote:
            return jsonify({"error": "It seems you've already disliked this blog! First, remove your dislike, then you can like it."}), 400


        existing_upvote = Upvote.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if existing_upvote:
            db.session.delete(existing_upvote)
            db.session.commit()
            num = get_number_of_users_upvoted(blog_id)
            return jsonify({'success': 'Blog unvoted', 'No_upvote': num}), 200
        else:
            upvote = Upvote(user_id=user_id, blog_id=blog_id)
            db.session.add(upvote)
            db.session.commit()
            num = get_number_of_users_upvoted(blog_id)
            return jsonify({'success': 'Blog upvoted', 'No_upvote': num}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@views.route('/devote/<int:blog_id>', methods=['POST'])
@login_required
def devote_blog(blog_id):
    user_id = current_user.id

    try:
        
        existing_upvote = Upvote.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if existing_devote:
            return jsonify({"error": "It seems you've already liked this blog! First, remove your like, then you can dislike it."}), 400


        existing_devote = Devote.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if existing_devote:
            db.session.delete(existing_devote)
            db.session.commit()
            num = get_number_of_users_devoted(blog_id)
            return jsonify({'success': 'Blog undevoted', 'No_devote': num}), 200
        else:
            devote = Devote(user_id=user_id, blog_id=blog_id)
            db.session.add(devote)
            db.session.commit()
            num = get_number_of_users_devoted(blog_id)
            return jsonify({'success': 'Blog devoted', 'No_devote': num}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@views.route('/bookmark/<int:blog_id>', methods=['POST'])
@login_required
def bookmark_blog(blog_id):
    user_id = current_user.id

    try:
        
        existing_bookmark = Bookmark.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if existing_bookmark:
            db.session.delete(existing_bookmark)
            db.session.commit()
            num = get_number_of_users_saved(blog_id)
            return jsonify({'success': 'Blog unbookmarked', 'No_bookmark': num}), 200
        else:
        
            bookmark = Bookmark(user_id=user_id, blog_id=blog_id)
            db.session.add(bookmark)
            db.session.commit()
            num = get_number_of_users_saved(blog_id)
            return jsonify({'success': 'Blog bookmarked', 'No_bookmark': num}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


#----------------------------------------------------courses-------------------------------------

@views.route("/courses")
def courses():
    return render_template("courses.html", user=current_user)




#-----------------------------------------------------memes----------------------------------------------

@views.route("/memes")
@login_required
def memes():
    return render_template("memes.html", user=current_user)







#-------------------------------------------------user public profile-------------------------------------

@views.route("/user/<username>")
@login_required
def public_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Check and set default profile picture if none is provided
    if user.profile_picture is None:
        user.profile_picture = "default_profile.jpeg"
    
    experience = user.experience
    posts = BlogPost.query.filter_by(user_id=user.id).order_by(BlogPost.date_posted.desc()).all()
    
    # Retrieve bookmarked articles for the user
    saved_posts_id = [bookmark.blog_id for bookmark in user.bookmarks]
    saved_posts = BlogPost.query.filter(BlogPost.id.in_(saved_posts_id)).all()
    
    # Sanitize content of saved posts
    for post in saved_posts:
        post.content = bleach.clean(post.content, tags=[], strip=True)
    
    return render_template("user_profile.html", user=user, experience=experience, posts=posts, saved_posts=saved_posts)



@views.route("/profile")
@login_required
def profile():
    posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date_posted.desc()).all()  # Changed to user_id
    if current_user.profile_picture is None:
        current_user.profile_picture = "https://cdn.pixabay.com/photo/2016/11/18/23/38/child-1837375_1280.png"
    else:
        current_user.profile_picture = url_for('static', filename='uploads/images/' + current_user.profile_picture)
    return render_template("user_profile.html", user=current_user, posts=posts)



@views.route("/myblogs")
@login_required
def myblogs():
    posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date_posted.desc()).all()
    for post in posts:
        post.content = bleach.clean(post.content, tags=[], strip=True)  
    return render_template("myblog.html", user=current_user, posts=posts, get_number_of_users_saved=get_number_of_users_saved)


@views.route("/edit_profile")
@login_required
def edit_profile():
    return render_template("edit_profile.html", user=current_user, posts=posts)

@views.route('/updatebio', methods=['POST'])
@login_required
def update_bio():
    bio = request.form.get('bio')
    if bio:
        current_user.bio = bio
        db.session.commit()
        flash('Bio updated successfully!', 'success')
    return redirect(url_for('views.edit_profile')) 




@views.route('/updateinfo', methods=['POST'])
@login_required
def update_info():
    user = current_user
    # user.username = request.form.get('username')
    user.gender = request.form.get('gender')
    user.phone = request.form.get('phone')
    user.university = request.form.get('university')
    user.linkedin = request.form.get('linkedin')
    user.github = request.form.get('github')
    # user.email = request.form.get('email')
    user.birthday = request.form.get('birthday')
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('views.edit_profile'))
    
@views.route('/updateexperience', methods=['POST'])
@login_required
def update_experience():
    user = current_user
    
    # Extracting the new experience data from the form
    new_experience = {
        'position': request.form.get('position'),
        'company': request.form.get('company'),
        'duration': request.form.get('duration')
    }
    
    # Debug statements to check if form data is received correctly
    # print("Received new experience:", new_experience)
    
    # Replace the user's experience with the new experience data
    user.experience = [new_experience]
    
    
    
    # Commit the changes to the database
    db.session.commit()
    flash('Experience updated successfully!', 'success')
    
    return redirect(url_for('views.edit_profile'))




# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/uploadprofilepic', methods=['POST'])
@login_required
def upload_profile_pic():
    f = request.files.get('profile_picture')

    if not f:
        flash('No file selected for profile picture!', 'error')
        return redirect(url_for('views.edit_profile'))
    
    if not allowed_file(f.filename):
        flash('Invalid file format!', 'error')
        return redirect(url_for('views.edit_profile'))

    try:
        # Generate a unique filename and save the file
        extension = os.path.splitext(secure_filename(f.filename))[1]
        filename = f"{uuid.uuid4()}{extension}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        f.save(file_path)

        # Update user's profile picture path in the database
        current_user.profile_picture = filename
        current_user.image_url = url_for('static', filename='uploads/images/' + current_user.profile_picture)
        db.session.commit()

        flash('Profile picture uploaded successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while saving the file: {e}', 'error')

    return redirect(url_for('views.edit_profile'))

# Error handler for Request Entity Too Large
@views.app_errorhandler(413)
def request_entity_too_large(error):
    flash('The file is too large to upload. Maximum file size is 2MB.', 'error')
    return redirect(url_for('views.edit_profile'))

def load_custom_hindi_abusive_words():
    hindi_words_file = os.path.join(os.path.dirname(__file__), 'profanity_words.txt')
    if not os.path.exists(hindi_words_file):
        raise FileNotFoundError(f"File '{hindi_words_file}' not found.")
    
    with open(hindi_words_file, 'r', encoding='utf-8') as f:
        hindi_words = [line.strip() for line in f.readlines() if line.strip()]  # Ensure no empty lines
    return hindi_words

def contains_abusive_words(text):
    hindi_abusive_words = load_custom_hindi_abusive_words()
    for word in hindi_abusive_words:
        if re.search(r'\b{}\b'.format(re.escape(word)), text, re.IGNORECASE):
            return True

    if profanity.contains_profanity(text):
        return True

    return False


def load_custom_hindi_abusive_words():
    hindi_words_file = os.path.join(os.path.dirname(__file__), 'profanity_words.txt')
    if not os.path.exists(hindi_words_file):
        raise FileNotFoundError(f"File '{hindi_words_file}' not found.")
    
    with open(hindi_words_file, 'r', encoding='utf-8') as f:
        hindi_words = [line.strip() for line in f.readlines() if line.strip()]  # Ensure no empty lines
    return hindi_words

def contains_abusive_words(text):
    hindi_abusive_words = load_custom_hindi_abusive_words()
    for word in hindi_abusive_words:
        if re.search(r'\b{}\b'.format(re.escape(word)), text, re.IGNORECASE):
            return True

    if profanity.contains_profanity(text):
        return True

    return False



@views.route("/editor", methods=["GET", "POST"])
@views.route("/editor/<int:post_id>", methods=["GET", "POST"])
@login_required
def editor(post_id=None):
    post = BlogPost.query.get(post_id) if post_id else None

    if post and post.user_id != current_user.id:
        flash("You are not authorized to edit this post.", "error")
        return redirect(url_for("views.posts"))

    form = MyForm(obj=post)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        # Check for abusive words in title and content
        if contains_abusive_words(title) or contains_abusive_words(content):
            flash("Your post contains inappropriate or offensive content. Please remove it.", "error")
            return render_template("editor.html", post=post, user=current_user, form=form)

        # Check if a post with the same title already exists
        existing_post = BlogPost.query.filter_by(title=title).first()
        if existing_post and (not post or existing_post.id != post.id):
            flash("A post with this title already exists. Please choose another title.", "error")
            return render_template("editor.html", post=post, user=current_user, form=form)
            
        word_count = len(content.split()) 
        if word_count < 100: 
            flash("Your blog post should be greater than 100 words. Please write more content.", "error") 
            return render_template("editor.html", post=post, user=current_user, form=form)

        if post:
            # This is an update to an existing post
            form.populate_obj(post)
            if not post.endpoint:
                post.endpoint = re.sub(r'\W+', '-', post.title.lower()).strip('-')
            db.session.commit()
            flash("Your post has been updated!", "success")
            return redirect(url_for("views.blog", post_endpoint=post.endpoint))
        else:
            # This is a new post
            today = date.today()
            # Count the number of posts made by the user today
            posts_today = BlogPost.query.filter(
                BlogPost.user_id == current_user.id,
                db.func.date(BlogPost.date_posted) == today
            ).count()

            # Calculate coins based on posts made today
            if posts_today == 0:
                coins_earned = 10  # First post of the day earns 10 coins
            elif posts_today < 10:
                coins_earned = 1  # Subsequent posts earn 1 coin each, up to 10 posts
            else:
                coins_earned = 0  # No coins earned after 10 posts in a day

            # Update user's coin balance
            if coins_earned > 0:
                current_user.coins += coins_earned
                db.session.commit()
                flash(f'Your post has been created! +{coins_earned} coins added to your account.', 'success')
            else:
                flash('Your post has been created!', 'success')

            new_post = BlogPost(
                title=title,
                content=content,
                author=current_user,
                endpoint=re.sub(r'\W+', '-', title.lower()),
                img_url=img_unplash(title) or url_for('static', filename='/images/default_image_blog.png'),
            )
            db.session.add(new_post)
            db.session.commit()

            # Update the streak and coin rewards after creating a new post
            update_streak(current_user)

            return redirect(url_for('views.posts', post_id=new_post.id))

    return render_template("editor.html", post=post, user=current_user, form=form)



def update_streak(user):
    today = date.today()
    if user.last_post_date is None:
        # Handle case where last_post_date is None (possibly a new user)
        user.last_post_date = today
        user.daily_streak = 1
    elif user.last_post_date == today:
        # User has already posted today, do not update streak
        return
    elif user.last_post_date < today - timedelta(days=1):
        # Reset streak if last post date is not yesterday or today
        user.daily_streak = 0
        user.last_post_date = today
    elif user.last_post_date >= today - timedelta(days=1):
        # Update streak if last post date is within the last 24 hours
        user.daily_streak += 1
        user.last_post_date = today

    # Check streak milestones and update coins accordingly
    if user.daily_streak == 10:
        user.coins += 10
        flash("Congratulations! You've reached a 10-day streak. +10 Extra bonus coins added to your account.", "info")
    elif user.daily_streak == 20:
        user.coins += 20
        flash("Congratulations! You've reached a 20-day streak. +20 Extra bonus coins added to your account.", "info")
    elif user.daily_streak == 30:
        user.coins += 30
        flash("Congratulations! You've reached a 30-day streak. +30 Extra bonus coins added to your account.", "info")

    db.session.commit()


#--------------------------------------------------C pages------------------------------------------------

@views.route('/c')
def c():
    page = cpages.query.filter_by(title="introduction-of-c-programming").first()
    if not page:
        return abort(401, description="Try again")
    return render_template('c.html', page=page, user = current_user)

@views.route('/c/<page_name>')
def c_page(page_name):
    page = cpages.query.filter_by(title=page_name).first()
    if not page:
        abort(404, description="Page not found")
    return render_template('c.html', page=page, user = current_user)

#--------------------------------------------------C++ pages------------------------------------------------
@views.route('/cpp')
def cpp():
    page = cpppages.query.filter_by(title="introduction-of-c++").first()
    if not page:
        page = {'title': 'Default Title', 'content': 'Default Content'}  # Provide a default value
    return render_template('cpp.html', page=page, user=current_user)

@views.route('/cpp/<page_name>')
def cpp_p(page_name):
    page = cpppages.query.filter_by(title=page_name).first()
    if not page:
        page = {'title': 'Default Title', 'content': 'Default Content'}  # Provide a default value
    return render_template('cpp.html', page=page, user=current_user)

#--------------------------------------------------Basoc Practice pages------------------------------------------------


@views.route('/basic-practice-problems')
def basis_ques():
    page = BasicPage.query.filter_by(name="basic-practice-problem").first()
    listofpage = BasicPage.query.filter(BasicPage.name != "basic-practice-problem").all()
    return render_template('pages.html', user=current_user, curr_page=page, pages=listofpage)

@views.route('/basic-practice-problems/<page_name>')
def render_page(page_name):
    page = BasicPage.query.filter_by(name=page_name).first_or_404()
    listofpage = BasicPage.query.filter(BasicPage.name != "basic-practice-problem").all()
    return render_template('pages.html', user=current_user, curr_page=page, pages=listofpage)


    
    
    
#--------------------------------------------------Advance practice pages------------------------------------------------

@views.route('/advance-practice-problems')
def adv_ques():
    page = Pageadv.query.filter_by(name="advance-practice-problems").first()
    listofpage = Pageadv.query.filter(Pageadv.name != "advance-practice-problems").all()
    return render_template('Pageadv.html', user=current_user, curr_page=page, pages=listofpage)  
    
@views.route('/advance-practice-problems/<page_name>')
def render_advpage(page_name):
    page = Pageadv.query.filter_by(name=page_name).first_or_404() 
    listofpage = Pageadv.query.filter(Pageadv.name != "advance-practice-problems").all()
    return render_template('Pageadv.html', user=current_user, curr_page=page, pages=listofpage) 

#--------------------------------------------------Moderate Practice pages------------------------------------------------

 
@views.route('/moderate-practice-problems')
def mod_ques():
    page = Pagemod.query.filter_by(name="moderate-practice-problems").first()
    listofpage = Pagemod.query.filter(Pagemod.name != "moderate-practice-problems").all()
    return render_template('Pagemod.html', user=current_user, curr_page=page, pages=listofpage)   
    
@views.route('/moderate-practice-problems/<page_name>')
def mod_advpage(page_name):
    
    page = Pagemod.query.filter_by(name=page_name).first_or_404()     
    listofpage = Pagemod.query.filter(Pagemod.name != "moderate-practice-problems").all()
    return render_template('Pagemod.html', user=current_user, curr_page=page, pages=listofpage)
    

    
#--------------------------------------------------Upload pages------------------------------------------------

@views.route('/upload', methods=['POST'])
@login_required  # Ensure only logged-in users can upload
def upload():
    f = request.files.get('upload')
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOADED_PATH'], filename))
        url = url_for('views.uploaded_files', filename=filename)
        return upload_success(url)
    return upload_fail('Could not upload file.')


@views.route('/uploads/<filename>')
def uploaded_files(filename):
    return send_from_directory(current_app.config['UPLOADED_PATH'], filename)



    

@views.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', user = current_user), 404

@views.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
