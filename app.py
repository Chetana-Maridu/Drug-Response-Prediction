import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import joblib
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="#####",            # Replace with your MySQL username
        password="######",   # Replace with your MySQL password
        database="drug_responsef"  # Use the drug_response database
    )

# Load the trained model
model = joblib.load('drug_response_model.pkl')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using sessions

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        accuracy = 0.0  # Initial accuracy for new users

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password, accuracy) VALUES (%s, %s, %s)", (username, password, accuracy))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the user is an admin
    if username == 'admin' and password == 'admin':
        session['user'] = 'admin'
        return redirect(url_for('admin_panel'))

    # Check in the user database
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        session['user'] = username
        return redirect(url_for('index'))
    else:
        return render_template('welcome.html', error="Invalid username or password")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        drug_id = int(request.form['drug_id'])
        dosage = float(request.form['dosage'])
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        condition_indicator = int(request.form['condition_indicator'])

        features = np.array([[drug_id, dosage, age, bmi, condition_indicator]])
        prediction = model.predict(features)[0]

        return render_template('result.html', prediction=round(prediction, 2))
    except Exception as e:
        return render_template('result.html', prediction="Error: Invalid input")

@app.route('/admin_panel')
def admin_panel():
    if session.get('user') != 'admin':
        return redirect(url_for('home'))

    # Fetch user data for the admin panel
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT username, accuracy FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('admin_panel.html', users=users)

@app.route('/user_accuracy/<username>')
def user_accuracy(username):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT accuracy FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if not result:
        return jsonify({"error": "No accuracy data found for this user"}), 404

    accuracy = result[0]
    plt.figure(figsize=(6, 4))
    plt.bar([username], [accuracy], color='skyblue')
    plt.xlabel('User')
    plt.ylabel('Accuracy (%)')
    plt.title(f'Accuracy for {username}')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_data = base64.b64encode(img.getvalue()).decode('utf8')
    return jsonify({"img_data": img_data})


# New route: accuracy chart for all users
@app.route('/all_users_accuracy')
def all_users_accuracy():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT username, accuracy FROM users")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    if not results:
        return jsonify({"error": "No accuracy data found"}), 404

    usernames = [row[0] for row in results]
    accuracies = [row[1] for row in results]

    plt.figure(figsize=(10, 6))
    plt.bar(usernames, accuracies, color='skyblue')
    plt.xlabel('Users')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy of All Users')
    plt.xticks(rotation=45, ha='right')

    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_data = base64.b64encode(img.getvalue()).decode('utf8')
    return jsonify({"img_data": img_data})

# New route: render a page showing the graph for all users
@app.route('/show_all_users_accuracy')
def show_all_users_accuracy():
    return render_template('all_users_accuracy.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

