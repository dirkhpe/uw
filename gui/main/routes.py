from gui import db
from gui.lib import elastic
# from gui.lib.guidb import User
from gui.main.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from . import main


el = elastic.Elastic()


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/indices')
@login_required
def indices():
    res = el.get_indices()
    flash("Ready to show indices", "info")
    return render_template("indices.html", reslist=res.json())


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html", title="ElasticSearch")


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route('/search/<indexname>', methods=['GET', 'POST'])
@login_required
def search(indexname):
    """
    This method allows to search on specific fields in an index.

    :param indexname: Name of the index that need to be searched.
    :return:
    """
    if request.method == 'POST':
        form = Search()
        res = el.search_for(indexname, form.itemlist.data, form.term.data)
        flash("Search in field {}".format(form.itemlist.data))
        flash("Search for term {}".format(form.term.data))
        flash("Result: {}".format(res.json()))
        return redirect(url_for('main.search', indexname=indexname))
    else:
        res = el.get_mapping(indexname)
        indexmap = elastic.map2list(res.json())
        form = Search(itemlist=indexmap[0][0])
        form.itemlist.choices = indexmap
        return render_template('search.html', title='Search Index *{}*'.format(indexname), form=form)


@main.route('/select_index', methods=['GET', 'POST'])
@login_required
def select_index():
    if request.method == 'POST':
        form = RadioList()
        indexname = form.itemlist.data
        return redirect(url_for('main.search', indexname=indexname))
    else:
        res = el.get_indices(purpose='forSelect')
        form = RadioList(itemlist=res[0][0])
        form.itemlist.choices = res
        return render_template('radioList.html', title="Select Index", form=form)
