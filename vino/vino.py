#!/usr/bin/env python

from flask import Flask
from db import Session, Base, engine
from models import Winery


def main():

    Base.metadata.create_all(engine, checkfirst=True)

    app = Flask(__name__)

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
