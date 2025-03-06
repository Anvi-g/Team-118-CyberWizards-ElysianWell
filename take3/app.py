from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import google.generativeai as genai
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
app.config["SECRET_KEY"] = "supersecretkey"

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configure Gemini API
genai.configure(api_key="AIzaSyC6y4wisGIhFzvoXA4OYowPsQQeRYwqKcA")

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Symptom Model
class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tip = db.Column(db.String(255), nullable=True)

# UserSymptom Model
class UserSymptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), nullable=False)
    symptom = db.relationship('Symptom', backref=db.backref('user_symptoms', lazy=True))
    user = db.relationship('User', backref=db.backref('user_symptoms', lazy=True))

# Conversation Model
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Content Route (Newly Added)
@app.route("/content")
def content():
    return render_template("content.html")

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")

# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Chatbot Route
@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    return render_template("chat.html")

# Process Chat
@app.route("/chatbot", methods=["POST"])
@login_required
def chatbot():
    user_message = request.json["message"]

    # Generate AI response
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(user_message)
    bot_response = response.text if response.text else "I'm here to help. Can you provide more details?"

    # Store conversation
    new_chat = Conversation(user_id=current_user.id, user_message=user_message, bot_response=bot_response)
    db.session.add(new_chat)
    db.session.commit()

    # Emergency Helpline Suggestions
    if "suicide" in user_message.lower() or "self-harm" in user_message.lower():
        bot_response += " 🚨 If you are in crisis, please reach out to an emergency helpline immediately."

    return jsonify({"response": bot_response})

# Retrieve Conversation History
@app.route("/history")
@login_required
def history():
    chats = Conversation.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", chats=chats)

# Symptoms Route
@app.route('/symptoms')
@login_required
def symptoms():
    symptoms = Symptom.query.all()
    return render_template('symptoms.html', symptoms=symptoms)

# Submit Symptoms Route
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

def get_tips(symptoms):
    tips = []
    for symptom_id in symptoms:
        symptom = Symptom.query.get(symptom_id)
        if symptom:
            print(f"Symptom found: {symptom.name}, Tip: {symptom.tip}")  # Debug print
            if symptom.tip:
                tips.append(symptom.tip)
        else:
            print(f"Symptom ID {symptom_id} not found")  # Debug print
    print("Tips in get_tips function:", tips)  # Debug print
    return tips

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
