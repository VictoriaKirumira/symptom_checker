from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Symptom
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and if the password matches
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')



@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    symptoms = [
        request.form.get('symptom1'),
        request.form.get('symptom2'),
        request.form.get('symptom3'),
        request.form.get('symptom4'),
        request.form.get('symptom5'),
        request.form.get('symptom6')
    ]

    # Filter out empty symptom entries
    symptoms = [symptom.lower() for symptom in symptoms if symptom]

    # Check if there are at least 3 symptoms entered
    if len(symptoms) < 3:
        return render_template('results.html', conditions=[], message="Please enter at least 3 symptoms.")
    
    new_symptom = Symptom(symptom_list=', '.join(symptoms), user_id=current_user.id)
    db.session.add(new_symptom)
    db.session.commit()

    # Analyze the symptoms and determine possible conditions
    possible_conditions = []

    if 'fever' in symptoms and 'headache' in symptoms and 'joint pains' in symptoms:
        possible_conditions.append("Malaria")
    if 'fever' in symptoms and 'headache' in symptoms and 'stomach pain' in symptoms:
        possible_conditions.append("Typhoid")
    if 'running nose' in symptoms and 'fever' in symptoms and 'headache' in symptoms:
        possible_conditions.append("Cold")
    if 'nausea' in symptoms and 'stomach pain' in symptoms and 'heartburn' in symptoms:
        possible_conditions.append("Peptic Ulcer Disease")
    if 'fever' in symptoms and 'lower abdominal pain' in symptoms and 'pain on urinating' in symptoms:
        possible_conditions.append("Urinary Tract Infection")
    if 'cough' in symptoms and 'sore throat' in symptoms and 'flu' in symptoms:
        possible_conditions.append("Upper Respiratory Tract Infection")
    if 'chest pain' in symptoms and 'shortness of breath' in symptoms and 'cough' in symptoms:
        possible_conditions.append("Pneumonia")

    # Display a default message if no conditions are matched
    if not possible_conditions:
        message = "No matching conditions found based on the entered symptoms. Please consult a healthcare provider."
    else:
        message = "Based on the symptoms you entered, the possible conditions are:"

    return render_template('results.html', conditions=possible_conditions, message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
