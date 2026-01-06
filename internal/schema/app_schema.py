from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    query = StringField('query', validators=[
        DataRequired('用户的提问是必填'),
        Length(max=2000, message="用户的提问最大长度是 2000")
    ])