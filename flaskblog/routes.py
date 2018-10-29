import os
import secrets
# scaling image library
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'James Smith',
        'title': 'Blog Post 1',
        'content': 'First port content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'John Smith',
        'title': 'Blog Post 2',
        'content': 'Second port content',
        'date_posted': 'April 21, 2018'
    }

]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hasing New Users password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # adding New User to the Datbase
        db.session.add(user)
        db.session.commit()
        # success is a bootstrap message
        flash('Your account has been created! Please log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # this will log in the user
            login_user(user, remember=form.remember.data)
            # get next parameter from url
            next_page = request.args.get('next')
            # ternary conditional
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/lougout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    #randomize upload image name
    random_hex = secrets.token_hex(8)
    # grab file extension, _ = unused variable name
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize images
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #set user's profile Picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # will update account info
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated!', 'sucess')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # checks if updated info already belongs to another user
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
