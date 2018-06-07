# coding:utf-8
from . import main
from .forms import NameForm
from ..models import User
from .. import db
from flask import session, redirect, url_for
from ..email import send_email


@main.route('/', methods=['GET', 'POST'])
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
