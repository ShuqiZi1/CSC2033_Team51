import logging
from flask import Blueprint, render_template, flash, redirect, url_for, request
from datetime import datetime

from sqlalchemy import desc

from app import requires_roles
from post.forms import PostForm
from models import User, Follow, Post, Like, db
from flask_login import login_required, current_user, logout_user

profile_blueprint = Blueprint('profiles', __name__, template_folder='templates')

# If user query returns a user then a profile page is displayed for that user with their allocated data.
# If no user is returned then a 404 error is displayed.


@profile_blueprint.route('/profiles/<username>', methods=['GET', 'POST'])
def profiles(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('errors/404.html'), 404
    followers_count = Follow.query.filter_by(following_id=user.user_id).count()
    following_count = Follow.query.filter_by(follower_id=user.user_id).count()
    post_count = Post.query.filter_by(user_id=user.user_id).count()
    user_posts = Post.query.filter_by(user_id=user.user_id).all()
    liked_posts = Like.query.filter_by(user_id=user.user_id).all()
    form = PostForm()

    # view my post
    my_posts = Post.query.filter_by(user_id=user.user_id).order_by(desc('post_id')).all()
    my_post_days = list()
    my_post_years_months = list()
    # set format for date
    if my_posts:
        for my_post in my_posts:
            date = datetime.strptime(str(my_post.post_time), '%Y-%m-%d %H:%M:%S')
            my_post_days.append(datetime.strftime(date, '%d'))
            my_post_years_months.append(datetime.strftime(date, '%B %Y'))

    # view liked post
    liked_posts_by_id = Like.query.filter_by(user_id=user.user_id).order_by(desc('post_id')).all()
    liked_posts = list()
    for i in liked_posts_by_id:
        liked_posts.append(Post.query.filter_by(post_id=i.post_id).first())
    liked_post_days = list()
    liked_post_years_months = list()
    # set format for date
    if liked_posts:
        for liked_post in liked_posts:
            date = datetime.strptime(str(liked_post.post_time), '%Y-%m-%d %H:%M:%S')
            liked_post_days.append(datetime.strftime(date, '%d'))
            liked_post_years_months.append(datetime.strftime(date, '%B %Y'))

    return render_template('user.html', form=form,
                           user=user,
                           posts=user_posts,
                           likes=liked_posts,
                           counts=[post_count, followers_count, following_count],
                           my_posts=my_posts,
                           my_post_days=my_post_days,
                           my_post_years_months=my_post_years_months,
                           liked_posts=liked_posts,
                           liked_post_days=liked_post_days,
                           liked_post_years_months=liked_post_years_months)

# If the query doesn't return a user, they cannot be followed as they don't exist, user is then redirected to the
    # profile page. If a user is returned, a new follow relationship is added to the database, then the profile page
    # is displayed again to show the new follow


@profile_blueprint.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Could not follow user!")
        return redirect(url_for("profiles.profiles", username=username))

    new_follow = Follow(follower_id=current_user.user_id, following_id=user.user_id)
    db.session.add(new_follow)
    db.session.commit()
    return redirect(url_for("profiles.profiles", username=username))

# If the query returns no user, the user doesn't exist so cannot be unfollowed, if old_follow returns a follow
# relationship then it will be deleted from the database.


@profile_blueprint.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Could not unfollow user!")
        return redirect(url_for("profiles.profiles", username=username))

    old_follow = Follow.query.filter_by(follower_id=current_user.user_id, following_id=user.user_id).first()
    if not old_follow:
        flash("Already no following user '" + username + "'")
        return redirect(url_for("profiles.profiles", username=username))

    db.session.delete(old_follow)
    db.session.commit()

    return redirect(url_for("profiles.profiles", username=username))
    # Profile page is then reloaded so the user can see their change


# view logout
@profile_blueprint.route('/logout')
@login_required
def logout():
    # log for log out
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.user_id, current_user.email, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))
    # Displays homepage with no User information
