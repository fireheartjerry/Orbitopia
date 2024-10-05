from flask import Flask, render_template, request, redirect, url_for, session
import os
import random

app = Flask(__name__)

# Load the secret key from an environment variable for production, with a fallback for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_development_fallback_key')

# Game questions and character data about the Sun
questions = {
    1: 'Is it a star?',
    2: 'Does it emit light?',
    3: 'Is it located at the center of our solar system?',
    4: 'Can it support life on its own?',
    5: 'Is it composed mainly of hydrogen and helium?',
    6: 'Is it responsible for the changing seasons?'
}

characters = [
    {'name': 'The Sun',         'answers': {1: 1, 2: 1, 3: 1, 4: 0, 5: 1, 6: 0}},
    {'name': 'A Solar Flare',   'answers': {1: 1, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0}},
    {'name': 'A Black Hole',    'answers': {1: 1, 2: 0, 3: 0, 4: 0, 5: 0.5, 6: 0}},
    {'name': 'Earth',           'answers': {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1}}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story')
def storymode():
    return render_template('story/storymode.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Initialize session data if not present
    if 'questions_so_far' not in session:
        session['questions_so_far'] = []
    if 'answers_so_far' not in session:
        session['answers_so_far'] = []

    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
    else:
        question = request.args.get('question')
        answer = request.args.get('answer')

    # Process answers and questions
    if question and answer:
        session['questions_so_far'].append(int(question))
        session['answers_so_far'].append(float(answer))
        session.modified = True  # Mark session as modified to ensure data is saved

    # Calculate probabilities based on answers so far
    probabilities = calculate_probabilities(session['questions_so_far'], session['answers_so_far'])

    questions_left = list(set(questions.keys()) - set(session['questions_so_far']))

    if len(questions_left) == 0:
        # Return the most probable character
        result = probabilities[0]
        return render_template('game.html', result=result['name'])
    else:
        # Ask another question
        next_question = random.choice(questions_left)
        return render_template('game.html', question=next_question, question_text=questions[next_question])

@app.route('/reset')
def reset():
    # Clear the session data to reset the game
    session.pop('questions_so_far', None)
    session.pop('answers_so_far', None)
    return redirect(url_for('game'))

@app.route('/story/begin')
def storybegin():
    return render_template('story/begin.html')

@app.route('/story/1.1')
def story1_1():
    return render_template('story/1.1.html')

@app.route('/story/1.2')
def story1_2():
    return render_template('story/1.2.html')

@app.route('/story/1.3')
def story1_3():
    return render_template('story/1.3.html')

@app.route('/story/2.1')
def story2_1():
    return render_template('story/2.1.html')

@app.route('/story/2.2')
def story2_2():
    return render_template('story/2.2.html')

@app.route('/story/3.1')
def story3_1():
    return render_template('story/3.1.html')

@app.route('/story/3.2')
def story3_2():
    return render_template('story/3.2.html')

@app.route('/story/4.1')
def story4_1():
    return render_template('story/4.1.html')

@app.route('/story/4.2')
def story4_2():
    return render_template('story/4.2.html')

@app.route('/story/5.1')
def story5_1():
    return render_template('story/5.1.html')

@app.route('/story/5.2')
def story5_2():
    return render_template('story/5.2.html')

@app.route('/story/6')
def story6():
    return render_template('story/6.html')

# Calculate the probabilities for all characters based on given answers
def calculate_probabilities(questions_so_far, answers_so_far):
    probabilities = []
    for character in characters:
        similarity_score = calculate_similarity_score(character, questions_so_far, answers_so_far)
        probabilities.append({
            'name': character['name'],
            'probability': similarity_score
        })
    
    # Sort characters by similarity score (higher score means more similar)
    probabilities = sorted(probabilities, key=lambda x: x['probability'], reverse=True)
    return probabilities

# Calculate similarity score for a single character based on answers
def calculate_similarity_score(character, questions_so_far, answers_so_far):
    score = 0
    for question, answer in zip(questions_so_far, answers_so_far):
        character_answer_value = character_answer(character, question)
        # Calculate similarity as inverse of the absolute difference
        score += 1 - abs(answer - character_answer_value)
    return score

# Helper function to get a character's answer to a question
def character_answer(character, question):
    if question in character['answers']:
        return character['answers'][question]
    return 0.5  # Default neutral answer if no answer exists

if __name__ == '__main__':
    app.run(debug=True)
