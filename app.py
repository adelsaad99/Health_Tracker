from flask import Flask, render_template, request, redirect, url_for  # Import Flask and helpers
import psycopg2  # Import PostgreSQL connector
import psycopg2.extras  # For dictionary cursor
from dotenv import load_dotenv  # To load environment variables from .env
import os  # To access environment variables

app = Flask(__name__)  # Initialize Flask app

# Connect to PostgreSQL database
load_dotenv()  # Load .env variables
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Use dictionary cursor for easy access

# Home page showing summary and last 3 records
@app.route('/')
def index():
    cursor.execute("SELECT * FROM \"Health_Tracker\".health_data ORDER BY date")  # Get all records ordered by date
    data = cursor.fetchall()  # Fetch all data
    total_exercise = sum(row['exercise'] for row in data)  # Sum of exercise
    avg_meditation = round(sum(row['meditation'] for row in data)/len(data),1) if data else 0  # Average meditation
    avg_sleep = round(sum(row['sleep'] for row in data)/len(data),1) if data else 0  # Average sleep
    last_records = data[-3:] if len(data)>=3 else data  # Get last 3 records
    return render_template('index.html', total_exercise=total_exercise, avg_meditation=avg_meditation, avg_sleep=avg_sleep, last_records=last_records)  # Render home page

# Add new health data
@app.route('/form', methods=['GET','POST'])
def add_data():
    if request.method=='POST':  # Check if form submitted
        date = request.form['date']  # Get date from form
        exercise = request.form['exercise']  # Get exercise
        meditation = request.form['meditation']  # Get meditation
        sleep = request.form['sleep']  # Get sleep
        sql = "INSERT INTO \"Health_Tracker\".health_data (date, exercise, meditation, sleep) VALUES (%s,%s,%s,%s)"  # SQL query
        cursor.execute(sql,(date,exercise,meditation,sleep))  # Execute query
        conn.commit()  # Commit changes
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    return render_template('form.html')  # Show form if GET request

# Dashboard showing all records and chart
@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM \"Health_Tracker\".health_data ORDER BY date")  # Get all records
    data = cursor.fetchall()  # Fetch data
    dates = [d['date'].strftime("%Y-%m-%d") for d in data]  # Format dates
    exercise_data = [d['exercise'] for d in data]  # List of exercise
    meditation_data = [d['meditation'] for d in data]  # List of meditation
    sleep_data = [d['sleep'] for d in data]  # List of sleep
    return render_template('dashboard.html', data=data, dates=dates, exercise_data=exercise_data, meditation_data=meditation_data, sleep_data=sleep_data)  # Render dashboard

# Edit a health record
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_data(id):
    cursor.execute("SELECT * FROM \"Health_Tracker\".health_data WHERE id=%s",(id,))  # Get record by id
    record = cursor.fetchone()  # Fetch record
    if request.method=='POST':  # Check if form submitted
        date = request.form['date']  # Get updated date
        exercise = request.form['exercise']  # Get updated exercise
        meditation = request.form['meditation']  # Get updated meditation
        sleep = request.form['sleep']  # Get updated sleep
        sql = "UPDATE \"Health_Tracker\".health_data SET date=%s, exercise=%s, meditation=%s, sleep=%s WHERE id=%s"  # SQL update query
        cursor.execute(sql,(date,exercise,meditation,sleep,id))  # Execute update
        conn.commit()  # Commit changes
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    return render_template('edit.html', record=record)  # Show edit form

# Delete a health record
@app.route('/delete/<int:id>')
def delete_data(id):
    cursor.execute("DELETE FROM \"Health_Tracker\".health_data WHERE id=%s",(id,))  # Delete record by id
    conn.commit()  # Commit deletion
    return redirect(url_for('dashboard'))  # Redirect to dashboard

# Run Flask app
if __name__=='__main__':
    app.run(debug=True)  # Start server in debug mode
