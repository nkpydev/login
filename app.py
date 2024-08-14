from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, ResetForm, SetPreferencesForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '4ccd46d98428a274bc1dc507766c76a7'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://newdeveloper:newdeveloperpwd@localhost/project1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "warning"

csrf = CSRFProtect(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    emailid = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bollywood_preference = db.Column(db.Boolean, default=False)
    hollywood_preference = db.Column(db.Boolean, default=False)
    videosongs_preference = db.Column(db.Boolean, default=False)
    adultcontent_preference = db.Column(db.Boolean, default=False)

def send_email(to_email_id, process):
    print(f"Sent link to {to_email_id}, for resetting {process}")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def check_already_exists(username):
    users = User.query.all()
    usernames = [user.username for user in users]
    if username in usernames:
        return True
    else:
        return False

@app.route("/")
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        emailid = form.emailid.data
        username = form.username.data
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        if check_already_exists(username) == True:
            flash("Username already registered, kindly select another one!", "warning")
        else:
            new_user = User(firstname=firstname, lastname=lastname, emailid=emailid, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful!! You can now log in.", "success")
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('setpreference'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route("/recommended")
@login_required
def recommended():
    return "Recommended Movies/Series as per set profile."

@app.route("/bollywood")
@login_required
def bollywood():
    return render_template('bollywood.html')

@app.route("/hollywood")
@login_required
def hollywood():
    return "Hollywood Movies/Series."

@app.route("/setpreference", methods=["GET", "POST"])
@login_required
def setpreference():
    form = SetPreferencesForm()
    if form.validate_on_submit():
        print("Here")
        current_user.bollywood_preference = form.preferred_category_1.data
        current_user.hollywood_preference = form.preferred_category_2.data
        current_user.videosongs_preference = form.preferred_category_3.data
        current_user.adultcontent_preference = form.adultpreference.data
        db.session.commit()
        flash("Your preferences are now set!", "success")
        return redirect(url_for('recommended'))
    if request.method == "GET":
        form.preferred_category_1.data = current_user.bollywood_preference
        form.preferred_category_2.data = current_user.hollywood_preference
        form.preferred_category_3.data = current_user.videosongs_preference
        form.adultpreference.data = current_user.adultcontent_preference
    return render_template('setpreference.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/reset", methods=["GET", "POST"])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        if form.username.data == "":
            send_email(form.emailid.data, 'reset_username')
        elif form.password.data == "":
            send_email(form.emailid.data, 'reset_password')
    return render_template('reset.html', form=form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.username)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
