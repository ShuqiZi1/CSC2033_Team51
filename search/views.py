from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from models import User, Post
from search.forms import SearchForm
from app import db

# CONFIG
search_blueprint = Blueprint('search', __name__, template_folder='templates')


# VIEWS
@search_blueprint.route('/search', methods=('GET', 'POST'))
@login_required
def search():

    form = SearchForm()

    if form.validate_on_submit():

        # get the accounts with the searched for username
        user_results = User.query.filter_by(username=form.search.data).all()
        # get the posts with the searched for title
        post_results = Post.query.filter_by(title=form.search.data).all()

        # get the count of each of these, when using count() on user_results it would have an argument error
        user_count = User.query.filter_by(username=form.search.data).count()
        post_count = Post.query.filter_by(title=form.search.data).count()
        # get the total count
        result_count = user_count + post_count
        # do the function to render the template
        return search_result(user_results, post_results, result_count)

    return render_template('search.html', form=form)


@search_blueprint.route('/search_result', methods=('GET', 'POST'))
@login_required
def search_result(user_results, post_results, result_count):
    form = SearchForm()

    return render_template('search_results.html', form=form,
                           user_results=user_results, post_results=post_results, count=result_count)
# Displays the search result template so the user can select their desired result
