from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    role = db.Column(db.String(16))
    products = db.relationship('Product', backref='owner', lazy=True)

    @property
    def rolenames(self):
        return [self.role] if self.role else []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, user_id):
        return cls.query.get(user_id)

    @property
    def identity(self):
        return self.user_id


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id', ondelete='CASCADE'))
    subcategories = db.relationship('Category')
    products = db.relationship('Product', backref='category', lazy=True)

    @property
    def subcategories_count(self) -> int:
        """
        Get count of direct subcategories for this category
        :return: count of subcategories
        """
        count = len(self.subcategories)

        for sub in self.subcategories:
            count += sub.subcategories_count

        return count

    @property
    def products_count(self) -> int:
        """
        Recursively get count of products in the category
        :return: count of products
        """
        count = len(self.products)

        for sub in self.subcategories:
            count += sub.products_count
        return count


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float)
