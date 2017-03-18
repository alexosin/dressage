from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, backref


class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    question = relationship('Question', backref='chapter', cascade='save-update, delete')

    def __str__(self):
        return '<Chapter(id {}, text {})>'.format(self.id, self.text[:10])


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    answer = relationship('Answer', backref='question', cascade='save-update, delete')


class Answer(db.Model):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)



