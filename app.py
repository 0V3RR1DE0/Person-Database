from flask import Flask, render_template, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    is_root = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7, max=80)])  # Changed min to 7
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7, max=80)])
    is_root = BooleanField('Is Root?')
    submit = SubmitField('Register')
    
class ChangePasswordForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)], render_kw={'readonly': True})
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=7, max=80)])
    submit = SubmitField('Change Password')
    
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7, max=80)])
    is_root = BooleanField('Is Root?')
    submit = SubmitField('Update')

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    subject = StringField('Subject', validators=[InputRequired()])
    person_name = StringField('Person Name')
    phone_number = StringField('Person Phone Number')
    age = IntegerField('Person Age')
    email = StringField('Person Email')
    details = StringField('Details', validators=[InputRequired()])
    additional_links = StringField('Additional Links or Social Media Profiles')
    submit = SubmitField('Add')

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    person_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    details = db.Column(db.Text, nullable=False)
    additional_links = db.Column(db.Text)
    creator = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create a root user if it doesn't exist
        root_user = User.query.filter_by(username='root').first()
        if not root_user:
            user = User(username='root', is_root=True)
            user.set_password('default')  # Set a secure password for the root user
            db.session.add(user)
            db.session.commit()
            
@app.route('/')
@login_required
def index():
    entries = Entry.query.all()  # Fetch all entries from the database
    return render_template('index.html', entries=entries)

@app.route('/view/<int:entry_id>')
@login_required
def view(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return "Entry not found", 404
    return render_template('view.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id):
    if not current_user.is_root:
        return "Permission Denied", 403

    entry = Entry.query.get(entry_id)
    if not entry:
        return "Entry not found", 404

    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return "Entry not found", 404

    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('view', entry_id=entry.id))

    return render_template('edit.html', form=form, entry=entry)  # Pass 'entry' to the template

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            title=form.title.data,
            subject=form.subject.data,
            person_name=form.person_name.data,
            phone_number=form.phone_number.data,
            age=form.age.data,
            email=form.email.data,
            details=form.details.data,
            additional_links=form.additional_links.data,
            creator=current_user.username
        )
        db.session.add(entry)
        db.session.commit()
        flash('Entry added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_root:
        return "Permission Denied", 403

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_root=form.is_root.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('manage_users'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(obj=current_user)
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)

@app.route('/manage_users')
@login_required
def manage_users():
    if not current_user.is_root:
        return "Permission Denied", 403

    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_root:
        return "Permission Denied", 403

    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.set_password(form.password.data)
        user.is_root = form.is_root.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', form=form, user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_root:
        return "Permission Denied", 403

    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    create_tables()  # Create the database tables
    app.run(host='0.0.0.0', port=5000)
