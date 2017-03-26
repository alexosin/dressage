from app import app, db
from flask import render_template, redirect, request, flash, url_for, session
from .models import Chapter, Question, Answer


@app.route('/')
def main():
    session['id'] = 0
    session['max'] = Question.max_id()[0]
    session['chapters'] = Chapter.max_id()[0]
    session['mark'] = 0
    session['rights'] = 0
    return render_template('start.html')


@app.route('/chapter', methods=['GET', 'POST'])
def chapter():
    if request.method == 'GET':
        if 'id' in session:
            session['id'] += 1
            chapter = Chapter.query.filter(Chapter.id == session['id']).first()
            return render_template('chapter.html', chapter=chapter)
        else:
            return redirect(url_for('main'))
    else:
        return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        questions = Question.query.filter(Question.chapter_id == session['id']).all()
        return render_template('quiz.html', questions=questions)
    else:
        forms = request.form
        for key in forms:
            values = forms.getlist(key)
            question = Question.query.filter(Question.id == key).first()
            print(values, question.is_correct_answer(values))
            multiplier = question.is_correct_answer(values)
            session['mark'] += 5 * multiplier
            session['rights'] += int(multiplier)
        if session['id'] == session['chapters']:
            return redirect(url_for('result'))
        return redirect(url_for('chapter'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template('result.html')
    else:
        return redirect(url_for('main'))
