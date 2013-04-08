from flask.ext.wtf import Form, TextField, PasswordField, validators, SelectField
from pychecker.models import User
from pychecker.scraper import valid_product
from pychecker.database import db_session
from pychecker import models


class LoginForm(Form):
    username = TextField(label='username',
                         validators=[validators.Required()],
                         description='Username')
    password = PasswordField(label='password',
                             validators=[validators.Required()],
                             description='Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = db_session.query(models.User).filter(
            models.User.username == self.username.data).first()

        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ProductForm(Form):
    url = TextField(label='url',
                    validators=[validators.Required()],
                    description="URL To Product")
    notify_price = TextField(label='Price to Notify',
                             validators=[validators.Required()],
                             description="$")
    brand = SelectField('Brand', choices=[
        ('amz', 'Amazon'), ('new', 'Newegg'), ('gap', 'GAP'),
        ('old', 'Old Navy'), ('urb', 'Urban Outfitters'),
        ('mac', 'Macy\'s'), ('stm', 'Steam')
    ])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not valid_product(self.url.data):
            return False

        return True
