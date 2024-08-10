from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random

app = Flask(__name__)
app.secret_key = 'xxx'  # Replace with a secure key

# Load the data from the CSV file
def load_data():
    with open('data/students.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    return data

data = load_data()

def reset_game():
    session['turns_left'] = 10
    session['score'] = 0
    session['correct_name'] = None

@app.route('/')
def index():
    # Initialize the session variables if not already set
    if 'turns_left' not in session:
        reset_game()

    # If the game is over, redirect to the score page
    if session['turns_left'] == 0:
        return redirect(url_for('score'))

    # Select a random gender for this turn
    selected_gender = random.choice(['M', 'F'])

    # Filter data by the selected gender
    filtered_data = [entry for entry in data if entry['Gender'] == selected_gender]
    
    # Select a random entry from the filtered data
    correct_entry = random.choice(filtered_data)

    # Generate a list of possible name options, including the correct one
    all_names = [entry['Name'] for entry in filtered_data]
    name_options = random.sample(all_names, 3)
    
    # Ensure the correct name is in the options
    if correct_entry['Name'] not in name_options:
        name_options[random.randint(0, 2)] = correct_entry['Name']

    random.shuffle(name_options)

    # Store the correct answer in the session
    session['correct_name'] = correct_entry['Name']

    return render_template('index.html', image_name=correct_entry['Image'], name_options=name_options)

@app.route('/check', methods=['POST'])
def check():
    selected_name = request.form['name']
    correct_name = session['correct_name']
    
    if selected_name == correct_name:
        session['score'] += 1

    session['turns_left'] -= 1

    return redirect(url_for('index'))

@app.route('/score')
def score():
    return render_template('score.html', score=session['score'])

@app.route('/reset')
def reset():
    reset_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
