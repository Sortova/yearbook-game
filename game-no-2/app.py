from flask import Flask, render_template, request,session
import random
import csv

app = Flask(__name__)
app.secret_key = "xxx"
# Load student data from CSV file
students = []
with open('data/students.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append(row)

@app.route('/', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        # Get the user's guess from the form
        guess = request.form.get('guess')
        correct_image = session.get('correct_image')
        correct_name = session.get('correct_name')
        
        # Check if the guess is correct
        if guess == correct_image:
            return render_template('success.html', correct_name=correct_name, correct_image=correct_image)
        else:
            return render_template('game.html', students=session.get('random_students'), correct_name=correct_name, error='Incorrect guess! Try again.')

    # For GET request: Generate a new game
    genders = set(student['Gender'] for student in students)
    selected_gender = random.choice(list(genders))

    # Select four random students with the selected gender
    random_students = [student for student in students if student['Gender'] == selected_gender]
    
    # Check if there are enough students with the selected gender
    if len(random_students) < 4:
        return 'Not enough students with the selected gender.'

    random_students = random.sample(random_students, 4)
    
    # Select one of the random students as the correct answer
    correct_student = random.choice(random_students)
    
    # Store relevant data in session
    session['correct_image'] = correct_student['Image']
    session['correct_name'] = correct_student['Name']
    session['random_students'] = random_students

    return render_template('game.html', students=random_students, correct_name=correct_student['Name'])

if __name__ == '__main__':
    app.run(debug=True)
