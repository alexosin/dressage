from app import app
from flask import render_template, redirect, request, flash, url_for, session
from .models import Chapter, Question, User


@app.route('/')
def main():
    session['id'] = 0
    session['max'] = Question.max_id()[0]
    session['chapters'] = Chapter.max_id()[0]
    session['mark'] = 0
    session['rights'] = 0
    return render_template('start.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = User.query.filter(
            User.username.in_([username]),
                              User.password.in_([password])
        ).first()

        if query:
            session['logged_in'] = True
            session['user'] = username
        else:
            flash(u'Invalid login or password', 'danger')
            return redirect(url_for('login'))
        return redirect(url_for('main'))
    elif request.method == 'GET':
        if session.get('logged_in'):
            flash(u'You have already logged in.', 'info')
            return redirect(url_for('main'))
        return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash(u'Signed out successfully.', 'success')
    return redirect(url_for('main'))


@app.route('/chapter', methods=['GET', 'POST'])
def chapter():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        if 'id' in session:
            session['id'] += 1
            chapter = Chapter.query.filter(Chapter.id == session['id']).first()
            return render_template('chapter.html', chapter=chapter)
        else:
            return redirect(url_for('main'))
    elif request.method == 'POST':
        return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        questions = Question.query.filter(Question.chapter_id == session['id']).all()
        return render_template('quiz.html', questions=questions)
    else:
        forms = request.form
        rights = 0
        marks = 0
        for key in forms:
            values = forms.getlist(key)
            question = Question.query.filter(Question.id == key).first()
            multiplier = question.is_correct_answer(values)
            marks += 5 * multiplier
            rights += int(multiplier)
        if rights < (len(forms) / 2):
            flash(u'You should get 50% of points', 'danger')
            session['id'] -= 1
            return redirect(url_for('chapter'))
        session['mark'] += marks
        session['rights'] += rights
        if session['id'] == session['chapters']:
            return redirect(url_for('result'))
        return redirect(url_for('chapter'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template('result.html')
    else:
        return redirect(url_for('main'))
