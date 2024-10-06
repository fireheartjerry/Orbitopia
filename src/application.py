from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import requests
from pprint import pprint
import logging

app = Flask(__name__)

# Load the secret key from an environment variable for production, with a fallback for development
API_KEY = "ymdfGVOxRpM9kSqP4TJGM4ETfamnJ5h96AvP45sT"

app.config.from_object('settings')

LOG_HANDLER = logging.FileHandler(app.config['LOGGING_FILE_LOCATION'])
LOG_HANDLER.setFormatter(
    logging.Formatter(fmt="[TOPSOJ] [{section}] [{levelname}] [{asctime}] {message}",
                      style='{'))
logger = logging.getLogger("TOPSOJ")
logger.addHandler(LOG_HANDLER)
logger.propagate = False
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    filename=app.config['LOGGING_FILE_LOCATION'],
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
)
logging.getLogger().addHandler(logging.StreamHandler())

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
    apod = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}").json()
    return render_template('index.html', apod=apod)

@app.route('/story')
def storymode():
    return render_template('story/storymode.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/starmap')
def starmap():
    return render_template('starmap.html')

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

@app.route('/story/6.1')
def story6_1():
    return render_template('story/6.1.html')

@app.route('/story/6.2')
def story6_2():
    return render_template('story/6.2.html')

@app.route('/story/6.3')
def story6_3():
    return render_template('story/6.3.html')

@app.route('/story/6.4')
def story6_4():
    return render_template('story/6.4.html')

@app.route('/story/6.5')
def story6_5():
    return render_template('story/6.5.html')

@app.route('/story/6.6')
def story6_6():
    return render_template('story/6.6.html')

@app.route('/story/6.7')
def story6_7():
    return render_template('story/6.7.html')

@app.route('/discovery')
def discovery():
    return render_template('discovery.html')

@app.route('/resources')
def resources():
    links = [
        {
            "description": {
                "title": "NASA - Homepage",
                "summary": "Explore NASA’s official site for the latest in space exploration, missions, and science."
            },
            "link": "https://www.nasa.gov/"
        },
        {
            "description": {
                "title": "NASA - Exoplanets",
                "summary": "Learn about exoplanets, their discoveries, and the science behind finding worlds beyond our solar system."
            },
            "link": "https://science.nasa.gov/exoplanets/"
        },
        {
            "description": {
                "title": "Exoplanet Discoveries Dashboard",
                "summary": "Explore the latest exoplanet discoveries, statistics, and mission data using NASA’s Discoveries Dashboard."
            },
            "link": "https://science.nasa.gov/exoplanets/discoveries-dashboard/"
        },
        {
            "description": {
                "title": "NASA Exoplanet Archive",
                "summary": "A comprehensive archive hosted by Caltech containing data on confirmed exoplanets, candidate exoplanets, and more."
            },
            "link": "https://exoplanetarchive.ipac.caltech.edu/index.html"
        },
        {
            "description": {
                "title": "NASA - Exoplanet Facts",
                "summary": "Discover fascinating facts and figures about exoplanets and the search for life beyond Earth."
            },
            "link": "https://science.nasa.gov/exoplanets/facts/"
        },
        {
            "description": {
                "title": "Types of Exoplanets",
                "summary": "Learn about the various types of exoplanets discovered, from gas giants to Earth-like rocky worlds."
            },
            "link": "https://science.nasa.gov/exoplanets/planet-types/"
        },
        {
            "description": {
                "title": "Exoplanet Watch - NASA",
                "summary": "Discover how NASA’s Exoplanet Watch helps amateur astronomers participate in planetary science."
            },
            "link": "https://exoplanets.nasa.gov/exoplanet-watch/about-exoplanet-watch/overview/"
        },
        {
            "description": {
                "title": "Strange New Worlds - NASA",
                "summary": "Immerse yourself in NASA’s 3D experiences to explore newly discovered, strange exoplanets."
            },
            "link": "https://science.nasa.gov/exoplanets/immersive/strange-new-worlds/"
        },
        {
            "description": {
                "title": "NASA - Exoplanet Catalog",
                "summary": "This exoplanetary encyclopedia offers interactive 3D models and data on over 5,600 confirmed exoplanets, with filters for type, discovery method, and the mission or facility that found them."
            },
            "link": "https://science.nasa.gov/exoplanets/exoplanet-catalog/"
        }
    ]

    return render_template('resources.html', links=links)

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
