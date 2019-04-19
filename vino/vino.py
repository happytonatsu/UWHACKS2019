#!/usr/bin/env python

from flask import Flask
from sqlalchemy_utils import database_exists, create_database
from db import Session, engine
from models import Winery


def main():

    app = Flask(__name__)

    if not database_exists(engine.url):
        create_database(engine.url)

    @app.route('/')
    def index():
        Session.query(Winery).all()
        return 'Vino'

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    app.run()


if __name__ == '__main__':
    main()
