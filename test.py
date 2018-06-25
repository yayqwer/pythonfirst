from flask import Flask,render_template,redirect,url_for,request,flash,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from deldata import apt


app = Flask(__name__)
app.register_blueprint(apt)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'abc'
db= SQLAlchemy(app)

class Form(FlaskForm):
    wtf_book = StringField(validators=[DataRequired()])
    wtf_author = StringField(validators=[DataRequired()])
    submit = SubmitField(label='保存')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(22))

    def __repr__(self):
        return '书籍: %s' %self.info


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(22))

    def __repr__(self):
        return '作者: %s' %self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        flash('请添加数据')

    form = Form()
    if form.validate_on_submit():
        wtf_bk = form.wtf_book.data
        wtf_au = form.wtf_author.data
        print(type(wtf_au))
        print(wtf_bk)
        bk = Book(info=wtf_bk)
        au = Author(name=wtf_au)
        db.session.add_all([bk, au])
        db.session.commit()

    book = Book.query.all()
    author = Author.query.all()
    return render_template('test.html', book=book, author=author, form=form)

# @app.route('/del_book/<int:id>')
# def delete_book(id):
#     bk = Book.query.get(id)
#     db.session.delete(bk)
#     db.session.commit()
#     return redirect(url_for('index'))
#
# @app.route('/del_author/<int:id>')
# def delete_author(id):
#     au = Author.query.get(id)
#     db.session.delete(au)
#     db.session.commit()
#     return redirect(url_for('index'))
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    u_xi = Author(name='我吃西红柿')
    au_qian = Author(name='萧潜')
    au_san = Author(name='唐家三少')
    bk_xi = Book(info='吞噬星空')
    bk_xi2 = Book(info='寸芒')
    bk_qian = Book(info='飘渺之旅')
    bk_san = Book(info='冰火魔厨')
    db.session.add_all([u_xi, au_qian, au_san, bk_xi, bk_xi2, bk_qian, bk_san])
    db.session.commit()
    app.run()
