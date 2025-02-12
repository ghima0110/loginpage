from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Mock database for users (you can later connect this to a real database)
users = {
    'admin': generate_password_hash('admin123')  # Hashed password for the 'admin' user
}

# Route for the login page (renders the login form)
@app.route('/')
def home():
    return render_template('login.html')

# Route to handle the login form submission
@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the form
    username = request.form['username']
    password = request.form['password']

    # Check if the user exists and the password is correct
    if username in users and check_password_hash(users[username], password):
        # Set session variables to track the logged-in user
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the  dashboard
    else:
        flash('Invalid login credentials', 'danger')
        return redirect(url_for('home'))

# Route for the dashboard (after login)
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in (i.e., session contains username)
    if 'username' in session:
        return f"Welcome, {session['username']}! This is the AI prediction dashboard."
    else:
        flash('Please login first.', 'danger')
        return redirect(url_for('home'))

# Route to log out the user
@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
    # Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

