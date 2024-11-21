from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to get users from the database
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Function to add a new user
def add_user(username, password,email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username,password,email) VALUES (?, ?, ?)", (username,password,email))
    conn.commit()
    conn.close()

# Home route - displays the users and handles form submission
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get username and password from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        
        # Add user to the database
        add_user(username,password,email)
    
    # Get all users from the database
    users = get_users()
    return render_template('index.html', users=users)

# Route to delete a user
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Delete the user by user_id
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    # Redirect back to the home page after deletion
    return redirect(url_for('home'))

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        # Get updated username and password from the form
        new_username = request.form['username']
        new_email   = request.form['email']
        new_password = request.form['password']
        
        
        # Update user in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username=?,email=?, password=?   WHERE id=?", (new_username,new_email,new_password, user_id))
        conn.commit()
        conn.close()
        
        # Redirect back to the home page
        return redirect(url_for('home'))
    
    # Fetch the user's current data for the form
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Render an update form
    return render_template('edit.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
