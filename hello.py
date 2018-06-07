import os

# migrate = Migrate(app, db)

from app import create_app
from app import db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
# os.environ['BLOG_FLASK_ADMIN'] = "18489969713@163.com"


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
