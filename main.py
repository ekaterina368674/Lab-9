import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)


class StepsNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)

    def __init__(self, steps, date):
        self.steps = steps
        self.date = date


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html', steps=list(reversed(StepsNote.query.all())))


@app.route('/add_step', methods=['POST'])
def add_book():
    steps = flask.request.form['step']
    date = flask.request.form['date']
    db.session.add(StepsNote(steps, date))
    db.session.commit()

    return flask.redirect(flask.url_for('index'))


@app.route('/delete_all', methods=['GET'])
def delete_all():
    for step in StepsNote.query.all():
        db.session.delete(step)
    db.session.commit()

    return flask.redirect(flask.url_for('index'))


with app.app_context():
    db.create_all()
app.run()
