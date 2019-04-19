#!/usr/bin/env python

from flask import Flask, request, redirect, render_template

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


    @app.route('/winery/<i>')
    def winery(i):

        w = Session.query(Winery).filter_by(id=i).first()

        return render_template('winery.html', w=w)

    @app.route('/add/winery', methods=['POST'])
    def add_winery():
        if request.form:

            name = request.form.get('name', '')

            w = Session.query(Winery).filter_by(name=name).first()
            if not w:
                try:
                    w = Winery(name=name)
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
