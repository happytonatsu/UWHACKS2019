#!/usr/bin/env python

import json

from flask import Flask, jsonify, request, redirect

from db import Session, Base, engine
from models import Winery, WineStyle, User
from utils import json_serial


def main():

    Base.metadata.create_all(engine, checkfirst=True)

    app = Flask(__name__)

    @app.route('/')
    def index():
        w = Session.query(Winery).first()
        if w:

            return json_serial(w)
        else:
            return 'Nothing'

    @app.route('/add/winery', methods=['POST'])
    def add_winery():
        if request.form:

            name = request.form.get('name', '')
            latitude = request.form.get('latitude', None)
            longitude = request.form.get('longitude', None)

            w = Session.query(Winery).filter_by(name=name).first()
            if not w:
                try:
                    w = Winery(name=name,
                               latitude=latitude,
                               longitude=longitude)
                    Session.add(w)
                    Session.commit()
                except Exception as e:
                    print('unable to add winery')
                    print(e)
            else:
                print('found winery with the same name')
        return redirect('/')

    @app.route('/add/styles', methods=['POST'])
    def add_style():
        if request.form:

            name = request.form.get('name', '')
            desc = request.form.get('description', '')

            s = Session.query(WineStyle).filter_by(name=name).first()
            if not s:
                try:
                    s = WineStyle(name=name, description=desc)
                    Session.add(s)
                    Session.commit()
                except Exception as e:
                    print('unable to add WineStyle')
                    print(e)
           else:
               print('found winestyle with the same name')
        return redirect('/')


    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    app.run()


if __name__ == '__main__':
    main()
