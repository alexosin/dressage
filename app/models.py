from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func



class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    text = Column(Text, nullable=False)
    question = relationship('Question', backref='chapter', cascade='save-update, delete')

    @classmethod
    def max_id(cls):
        return db.session.query(func.max(Chapter.id)).first()

    def __repr__(self):
        return '<Chapter(id {}, text {})>'.format(self.id, self.text[:10])


class Question(db.Model):
    TYPES = [
        ('radio', 'radio'),
        ('checkbox', 'checkbox')
    ]

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text = Column(String, nullable=False)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    type = Column(ChoiceType(TYPES), nullable=False)
    answer = relationship('Answer', backref='question', cascade='save-update, delete')
    mark_id = Column(Integer, ForeignKey('marks.id'), nullable=False)

    @classmethod
    def max_id(cls):
        return db.session.query(func.max(Question.id)).first()

    @property
    def correct_answers(self):
        return db.session.query(Answer.id).filter(Answer.question_id == self.id)\
                .filter(Answer.status).all()

    @property
    def answers(self):
        return Answer.query.filter(Answer.question_id == self.id).order_by(func.random()).all()

    def is_correct_answer(self, user_answers):
        corrects = [i[0] for i in self.correct_answers]
        answers = list(map(int, user_answers))
        if self.type == 'radio':
            return 1 if answers[0] in corrects else 0
        elif self.type == 'checkbox':
            count_correct_answers = len(corrects)
            count_user_answers = 0
            for answer in answers:
                if answer in corrects:
                    count_user_answers += 1
            return count_user_answers * 100 / count_correct_answers / 100

    def __str__(self):
        return '<Question(id {}, chapter {})>'.format(self.id, self.chapter_id)


class Answer(db.Model):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    @classmethod
    def count(cls):
        db.session.query(func.count(Answer.id))

    def __str__(self):
        return '<Answer(id {}, question_id {}, status {})>'.format(
            self.id, self.question_id, self.status
        )


class Mark(db.Model):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    mark = Column(Integer)
    question = relationship('Question', backref='mark')

    def __str__(self):
        return '<Mark(id {}, mark {})>'.format(
            self.id, self.mark
        )
