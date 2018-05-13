import os
from pathlib import Path
from datetime import datetime
from threading import Thread
from flask import Flask, render_template, redirect, url_for, session, flash

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

# os.environ['BLOG_FLASK_ADMIN'] = "18489969713@163.com"




migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<username {}>".format(self.username)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<role {}>".format(self.name)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASK_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        form_data = form.name.data
        user = User.query.filter_by(username=form_data).first()
        if not user:
            user = User(username=form_data)
            db.session.add(user)
            # db.session.commit()
            session['known'] = False
            if app.config['FLASK_ADMIN']:
                send_email(app.config['FLASK_ADMIN'], 'new subject', 'mail/new_user', user=user)
        else:
            session['known'] = True
        old_name = session.get('name')
        if old_name != form_data:
            flash('Looks like you have changed your name!')
        session['name'] = form_data
        return redirect(url_for('index'))
    return render_template('index.html', **{'current_time': datetime.utcnow(), 'form': form,
                                            'name': session.get('name'), 'known': session.get('known')})


@app.route('/user/<name>')
def user(name):
    # return render_template('user.html', **{'name': name})
    return render_template('user.html', name=name)


@app.shell_context_processor
def make_shell():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
