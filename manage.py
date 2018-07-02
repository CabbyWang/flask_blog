import os

from app import create_app
from app import db
from flask_script import Manager
from app.models import User, Role


app = create_app(os.getenv('FLASK_CONFIG', 'default'))
# os.environ['BLOG_FLASK_ADMIN'] = "18489969713@163.com"
manage = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


if __name__ == '__main__':
    # db.create_all()
    # app.run(debug=True)
    manage.run()
