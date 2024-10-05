from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story')
def storymode():
    return render_template('story/storymode.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/story/begin')
def storybegin():
    return render_template('story/begin.html')

@app.route('/story/1')
def story1():
    return render_template('story/1.html')

@app.route('/story/2')
def story2():
    return render_template('story/2.html')

@app.route('/story/3')
def story3():
    return render_template('story/3.html')

@app.route('/story/4')
def story4():
    return render_template('story/4.html')

@app.route('/story/5')
def story5():
    return render_template('story/5.html')

@app.route('/story/6')
def story6():
    return render_template('story/6.html')


if __name__ == '__main__':
    app.run(debug=True)