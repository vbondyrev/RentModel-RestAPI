import flask_praetorian
from flask.views import MethodView
from sqlalchemy import desc, asc

from app.models import *
from flask_rest_api import Blueprint, abort, Page
from app.schemes import *
from app.config import Config
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
db.create_all(app=app)
api.init_app(app)

guard = flask_praetorian.Praetorian(app, User)

category_blp = Blueprint('categories', 'categories', url_prefix='/categories',
                         description='Get categories list or create category(subcategory)')
product_blp = Blueprint('products', 'products', url_prefix='/products',
                        description='Get products list or create product')
user_blp = Blueprint('users', 'users', url_prefix='',
                     description='Register user or auth(get token)')


@user_blp.route('register')
class RegisterUser(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(code=201)
    def post(self, new_data):
        """
        Register new user
        """
        user = User.query.filter_by(username=new_data['username']).first()
        if user:
            abort(400, message='User with this username is already registered')
        user = User(username=new_data['username'], password=guard.encrypt_password(new_data['password']), role='user')
        db.session.add(user)
        db.session.commit()


@user_blp.route('auth')
class AuthUser(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(code=200)
    def post(self, data):
        """
        Get access token for existing user
        """
        user = guard.authenticate(data['username'], data['password'])
        ret = {'access_token': guard.encode_jwt_token(user)}
        return jsonify(ret), 200


class CursorPage(Page):
    @property
    def item_count(self):
        return self.collection.count()


@category_blp.route('')
class Categories(MethodView):
    @category_blp.response(CategorySchema(many=True))
    @category_blp.paginate(CursorPage)
    def get(self):
        """
        Get all categories
        """
        return Category.query

    @category_blp.arguments(CategorySchema)
    @category_blp.response(CategorySchema, code=201)
    @category_blp.doc(security=[{'jwt': []}])
    @flask_praetorian.roles_required('admin')
    def post(self, new_data):
        """
        Add new category
        """
        category = Category(**new_data)
        db.session.add(category)
        db.session.commit()

        return category


@category_blp.route('/<category_id>')
class CategoryById(MethodView):
    @category_blp.response(CategorySchema)
    def get(self, category_id):
        """
        Get category by id
        """
        category = Category.query.get(category_id)
        if not category:
            abort(404, message='Category not found')

        return category

    @category_blp.response(code=204)
    @category_blp.doc(security=[{'jwt': []}])
    @flask_praetorian.roles_required('admin')
    def delete(self, category_id):
        """
        Delete empty category
        """
        category = Category.query.get(category_id)
        if not category:
            abort(404, message='Category not found')

        if category.products_count > 0:
            abort(405, message='Category non empty')
        db.session.delete(category)
        db.session.commit()


@product_blp.route('')
class Products(MethodView):
    @product_blp.arguments(ProductQuerySchema, location='query')
    @product_blp.response(ProductSchema(many=True))
    @product_blp.paginate(CursorPage)
    def get(self, args):
        """
        Get all products
        """
        query = Product.query
        if 'owner_id' in args:
            query = query.filter_by(owner_id=args['owner_id'])
        if 'category_id' in args:
            query = query.filter_by(category_id=args['category_id'])
        if 'sort_by' in args:
            sort = args['sort_by']
            dir = asc
            if 'sort_dir' in args and args['sort_dir'] == 'desc':
                dir = desc
            query = query.order_by(dir(sort))

        return query

    @product_blp.arguments(ProductSchema)
    @product_blp.response(ProductSchema, code=201)
    @product_blp.doc(security=[{'jwt': []}])
    @flask_praetorian.auth_required
    def post(self, new_data):
        """
        Add new product
        """
        category = Category.query.get(new_data['category_id'])
        if not category:
            abort(400, message='Category not found')
        product = Product(**new_data, owner_id=flask_praetorian.current_user().user_id)
        db.session.add(product)
        db.session.commit()

        return product


@product_blp.route('/<product_id>')
class ProductByID(MethodView):
    @product_blp.response(ProductSchema)
    def get(self, product_id):
        """
        Get product by id
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message='Product not found')
        product.views += 1
        db.session.commit()

        return product

    @product_blp.response(code=204)
    @product_blp.doc(security=[{'jwt': []}])
    @flask_praetorian.auth_required
    def delete(self, product_id):
        """
        Delete product
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message='Product not found')
        if product.owner_id != flask_praetorian.current_user().user_id and \
                flask_praetorian.current_user().role != 'admin':
            abort(400, message='You are not owner of this product')
        db.session.delete(product)
        db.session.commit()


api.register_blueprint(category_blp)
api.register_blueprint(product_blp)
api.register_blueprint(user_blp)

# JWT authorization OpenAPI
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
api.spec.components.security_scheme("jwt", jwt_scheme)


