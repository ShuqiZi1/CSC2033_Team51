import copy
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from post.forms import PostForm, CharityPostForm
from models import Post, User, Like

post_blueprint = Blueprint('post', __name__, template_folder='templates')

# Returns a stream of posts ordered by post ID


@post_blueprint.route('/post')
def feed():
    posts = Post.query.order_by(desc('post_id')).all()
    return render_template('home.html', posts=posts)
# renders the home page so the user can view

# Creates a post with allocated post information and increases the next post's post ID by 1


@post_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = PostForm()
    if current_user.role == "Charity":
        form = CharityPostForm()

    next_post_id = Post.query.order_by(desc('post_id')).first().post_id + 1

    if form.validate_on_submit():
        new_post = Post(post_id=next_post_id,
                        user_id=current_user.user_id,
                        title=form.title.data,
                        body=form.body.data,
                        post_img=form.image.data)
        if current_user.role == "charity":
            new_post.location = form.location.data

        db.session.add(new_post)
        db.session.commit()

        return feed()
    return render_template('post.html', form=form)
# loads the post template so users can enter post information then submit

# Allows user to update post, if the query returns no post a 500 error is displayed, if the user ID is not equal
# to the post user ID then the option to edit post will not appear, otherwise the user will be able to update
# the title and body of the post and submit it, adding it to the data base


@post_blueprint.route('/<int:post_id>/update', methods=('GET', 'POST'))
def update(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        return render_template('500.html')

    if post.user_id != current_user.user_id:
        return feed()

    form = PostForm()
    if current_user.role == "charity":
        form = CharityPostForm()

    if form.validate_on_submit():
        post.update_post(form.title.data, form.body.data)
        return feed()

    form.title.data = post.title
    form.body.data = post.body

    return render_template('post.html', form=form)
# Loads post template allowing the user to edit

# If there is no post returned by the query or the user ID is not equal to the post user ID then the delete post
# button will not show, otherwise the user will be able to delete the post, removing it from the databse

@post_blueprint.route('/<int:post_id>/delete')
def delete(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post or post.user_id != current_user.user_id:
        return feed()

    Post.query.filter_by(post_id=post_id).delete()
    db.session.commit()

    return feed()

# If a post is returned by the query the user will have an option to like the post


@post_blueprint.route('/<int:post_id>/toggle_like')
def toggle_like(post_id):
    liked_post = Post.query.filter_by(post_id=post_id).first()
    liked_post.toggle_like(current_user.user_id)

    return feed()

