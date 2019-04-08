import marshmallow as ma
from flask_rest_api import Api
from marshmallow import ValidationError

api = Api()


@api.definition('Category')
class CategorySchema(ma.Schema):
    class Meta:
        strict = True
        ordered = True

    category_id = ma.fields.Int(dump_only=True)
    parent_category_id = ma.fields.Int(default=None,
                                       load_from='parent_id',
                                       dump_to='parent_id')
    title = ma.fields.String(required=True)
    description = ma.fields.String(required=True, load_only=True)
    subcategories_count = ma.fields.Int(dump_only=True)
    products_count = ma.fields.Int(dump_only=True)


def positive_price(price):
    if price <= 0:
        raise ValidationError('Price must be positive and non-null')


@api.definition('Product')
class ProductSchema(ma.Schema):
    class Meta:
        strict = True
        ordered = True

    product_id = ma.fields.Int(dump_only=True)
    owner_id = ma.fields.Int(dump_only=True)
    category_id = ma.fields.Int(required=True)
    title = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    photo_url = ma.fields.String(default='')
    price = ma.fields.Float(required=True, validate=positive_price)
    views = ma.fields.Int(dump_only=True)
    added_at = ma.fields.DateTime(dump_only=True)


def order_by_validate(order):
    if order not in ('price', 'views', 'added_at'):
        raise ValidationError('Incorrect sort filter (possible \"price\", \"views\", \"added_at\"')


def order_dir_validate(direction):
    if direction not in ('asc', 'desc'):
        raise ValidationError('Incorrect sort direction (possible \"asc\", \"desc\"')


@api.definition('ProductQuery')
class ProductQuerySchema(ma.Schema):
    class Meta:
        strict = True
        ordered = True

    sort_by = ma.fields.String(validate=order_by_validate)
    sort_dir = ma.fields.String(validate=order_dir_validate)
    owner_id = ma.fields.Integer()
    category_id = ma.fields.Integer()


@api.definition('User')
class UserSchema(ma.Schema):
    class Meta:
        strict = True,
        ordered = True

    username = ma.fields.String(required=True)
    password = ma.fields.String(required=True)
