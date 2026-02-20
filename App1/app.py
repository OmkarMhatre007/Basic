from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "formula1_secret" # A little nod to your interest!

# Initialize CSV files if they don't exist
def init_files():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame([
            ['subject_teacher', '123', 'Subject Teacher', 'Operating System'],
            ['class_teacher', 'pass', 'Class Teacher', 'AIML'],
            ['hod_sir', 'admin', 'HOD', 'All']
        ], columns=['username', 'password', 'role', 'subject'])
        df.to_csv('users.csv', index=False)
    
    if not os.path.exists('data.csv'):
        df = pd.DataFrame(columns=['student_name', 'attendance', 'ut_marks', 'sem_marks', 'subject'])
        df.to_csv('data.csv', index=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    df = pd.read_csv('users.csv')
    user = df[(df['username'] == username) & (df['password'].astype(str) == password)]
    
    if not user.empty:
        session['user'] = user.to_dict('records')[0]
        return redirect(url_for('dashboard'))
    return "Invalid Credentials. Please go back and try again."

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('index'))
    user = session['user']
    
    # Logic for HOD vs Teacher cards
    if user['role'] == 'HOD':
        subjects = ['Data Science', 'AIML', 'Computer Engg', 'Robotics & Automation']
    elif user['role'] == 'Class Teacher':
        subjects = [user['subject'], 'DBMS'] # His class + others
    else:
        subjects = [user['subject']]
        
    return render_template('dashboard.html', user=user, subjects=subjects)

@app.route('/input/<sub_name>')
def input_page(sub_name):
    return render_template('input.html', subject=sub_name)

@app.route('/submit', methods=['POST'])
def submit():
    new_entry = {
        'student_name': request.form['student_name'],
        'attendance': request.form['attendance'],
        'ut_marks': request.form['ut_marks'],
        'sem_marks': request.form['sem_marks'],
        'subject': request.form['subject']
    }
    df = pd.DataFrame([new_entry])
    df.to_csv('data.csv', mode='a', index=False, header=False)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_files()
    app.run(debug=True)