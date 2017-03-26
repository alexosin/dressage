from app import db
from app.models import Chapter, Question, Answer

db.session.add_all([
    Chapter(title='first chapter', text='dog'),
    Chapter(title='second chapter', text='cat'),
    Chapter(title='third chapter', text='parrot'),
    Question(text='first question', chapter_id=2, type='radio'),
    Question(text='second question', chapter_id=2, type='checkbox'),
    Question(text='third question', chapter_id=2, type='radio'),
    Answer(text='answer one', question_id=1, status=True),
    Answer(text='answer two', question_id=1),
    Answer(text='answer three', question_id=1),
    Answer(text='answer four', question_id=2, status=True),
    Answer(text='answer five', question_id=2, status=True),
    Answer(text='answer six', question_id=2),
    Answer(text='answer seven', question_id=3, status=True),
    Answer(text='answer eight', question_id=3),
    Answer(text='answer nine', question_id=3)
])

db.session.commit()
