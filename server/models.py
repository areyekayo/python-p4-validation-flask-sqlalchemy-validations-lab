from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, author_name):
        author_names = [author.name for author in Author.query.with_entities(Author.name).all()]

        if author_name in author_names:
            raise ValueError("Author has the same name as another author.")
        if not author_name:
            raise ValueError("Author must have a name.")
        return author_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        phone_pattern = re.compile(r'^[0-9]{10}$')
        match = phone_pattern.search(number)
        if match:
            return number
        else:
            raise ValueError("Phone number must be 10 digits.")

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        clickbait = re.compile(r"Won't Believe|Secret|Top|Guess")
        match = clickbait.search(title)
        if not title:
            raise ValueError("Post must have a title.")
        if not match:
            raise ValueError("Post title must be clickbaity and should contain 'Won't Believe', 'Secret', 'Top', or 'Guess'")
        return title
        
    @validates('content')
    def validate_content(self, key, content):
        if len(content) >= 250:
            return content
        else:
            raise ValueError("Post content must be at least 250 characters long.")
        
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary is too long and must be less than 250 characters.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
