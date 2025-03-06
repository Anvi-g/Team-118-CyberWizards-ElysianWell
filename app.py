from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symptoms.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class UserSymptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), nullable=False)
    symptom = db.relationship('Symptom', backref=db.backref('user_symptoms', lazy=True))
    user = db.relationship('User', backref=db.backref('user_symptoms', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    symptoms = Symptom.query.all()
    return render_template('index.html', symptoms=symptoms)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
            print(f'Error: {e}')  # Debug print
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    selected_symptoms = request.form.getlist('symptoms')
    print("Selected Symptoms:", selected_symptoms)  # Debug print
    user_symptoms = [UserSymptom(user_id=current_user.id, symptom_id=symptom_id) for symptom_id in selected_symptoms]
    db.session.add_all(user_symptoms)
    db.session.commit()
    tips = get_tips(selected_symptoms)
    print("Generated Tips:", tips)  # Debug print
    return render_template('result.html', tips=tips)

@app.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        print("Selected Symptoms:", selected_symptoms)  # Debug print
        user_symptoms = [UserSymptom(user_id=current_user.id, symptom_id=symptom_id) for symptom_id in selected_symptoms]
        db.session.add_all(user_symptoms)
        db.session.commit()
        tips = get_tips(selected_symptoms)
        print("Generated Tips:", tips)  # Debug print
        return render_template('result.html', tips=tips)
    symptoms = Symptom.query.all()
    return render_template('symptoms.html', symptoms=symptoms)

def get_tips(symptoms):
    tips = []
    if '1' in symptoms:
        tips.append('Practice mindfulness and meditation to manage stress.')
    if '2' in symptoms:
        tips.append('Maintain a balanced diet and stay hydrated.')
    if '3' in symptoms or '4' in symptoms:
        tips.append('Maintain a balanced diet with regular meals.')
    if '5' in symptoms:
        tips.append('Practice good sleep hygiene to improve sleep quality.')
    if '6' in symptoms:
        tips.append('Engage in regular physical activities like cardio or weight training.')
    return tips

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
