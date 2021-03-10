import string

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import URLType
from wtforms import Form
from wtforms.validators import URL
from wtforms_components import StringField

CHARSET = string.ascii_uppercase + string.ascii_lowercase + string.digits
BASE = len(CHARSET)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.cli.command()
def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Counter())
    db.session.commit()


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False, default=1)

    def encode(self):
        number = self.value
        code = ""
        while number:
            number, remainder = divmod(number - 1, BASE)
            code = CHARSET[remainder] + code
        return code


class Shurt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType, index=True, unique=True, nullable=False)
    code = db.Column(db.String(10), index=True, unique=True, nullable=False)

    @hybrid_property
    def smul(self):
        return request.url_root + self.code

    @classmethod
    def get_or_create(cls, url):
        shurt = cls.query.filter_by(url=url).one_or_none()
        if shurt:
            return shurt
        counter = Counter.query.get_or_404(1)
        code = counter.encode()
        counter.value += 1
        shurt = cls(url=url, code=code)
        db.session.add(shurt)
        db.session.commit()
        return shurt


class URLForm(Form):
    url = StringField(
        validators=[URL()],
        render_kw={"placeholder": "Input your URL", "autofocus": True},
    )


@app.route("/", methods=["GET", "POST"])
def home():
    template = "index.html"
    form = URLForm(request.form)
    if request.method == "POST":
        if not form.validate():
            return render_template(template, form=form)
        smul = Shurt.get_or_create(form.url.data).smul
        return render_template(template, form=form, smul=smul)
    return render_template(template, form=form)


@app.route("/<code>")
def track(code):
    shurt = Shurt.query.filter_by(code=code).first_or_404()
    return redirect(shurt.url)
