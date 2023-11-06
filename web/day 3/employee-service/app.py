from flask import Flask

import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = None
session = None
Base = None

def init_app():
    global app
    app = Flask(__name__)
    from views.employee import app_employee
    app.register_blueprint(app_employee)

def init_db():
    global session
    global Base

    engine = db.create_engine("sqlite:///employees.sqlite")
    conn = engine.connect() 
    metadata = db.MetaData()

    Employee = db.Table('Employee', metadata,
                    db.Column('id', db.Integer(), primary_key=True),
                    db.Column('name', db.String(255), nullable=False),
                    db.Column('address', db.String(1024), default="Nammane"),
                    db.Column('pic_id', db.String(1024), default="default")
                )

    metadata.create_all(engine)

    Base = declarative_base()
    session = sessionmaker(bind=engine)()

init_db()
init_app()