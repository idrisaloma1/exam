from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Admin
admin = Admin(app, name='Admin', template_mode='bootstrap3')

# In-memory database to store users (for demonstration purposes)
users_db = {}

# Define a model for exam submissions
class ExamSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    question1 = db.Column(db.String(150), nullable=False)
    question2 = db.Column(db.String(150), nullable=False)
    question3 = db.Column(db.String(150), nullable=False)
    question4 = db.Column(db.String(150), nullable=False)
    question5 = db.Column(db.String(150), nullable=False)

admin.add_view(ModelView(ExamSubmission, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            flash('Username already exists! Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        
        users_db[username] = password
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and users_db[username] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('exam', username=username))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/exam', methods=['GET', 'POST'])
def exam():
    if request.method == 'POST':
        username = request.args.get('username')
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        question4 = request.form['question4']
        question5 = request.form['question5']
        
        # Store the exam submission in the database
        submission = ExamSubmission(
            username=username,
            question1=question1,
            question2=question2,
            question3=question3,
            question4=question4,
            question5=question5
        )
        db.session.add(submission)
        db.session.commit()
        
        flash('Exam submitted successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('exam.html')

if __name__ == '__main__':
    app.run(debug=True)

