#!/usr/bin/env python

from flask import Flask, request, redirect, render_template, send_from_directory

from db import Session, Base, engine
from models import Winery, WineStyle, User
from utils import json_serial


def main():

    Base.metadata.create_all(engine, checkfirst=True)

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)


    @app.route('/search')
    def search():
        q = request.args.get('q', None)
        ws = []
        if q:
            ws = Session.query(Winery).filter(Winery.name.contains(q)).all()

        return render_template('search.html', ws=ws)


    @app.route('/winery')
    @app.route('/winery/<int:_id>')
    def winery(_id=None):
       if _id:
            w = Session.query(Winery).filter_by(id=_id).first()
            return render_template('winery.html', w=w)

       else:
           return 'show all wineries'


    @app.route('/add/winery', methods=['GET', 'POST'])
    def add_winery():
        if request.method == 'POST':
            if request.form:

                name = request.form.get('name', '')

                w = Session.query(Winery).filter_by(name=name).first()
                if not w:

                    address = request.form.get('address', '')
                    phone = request.form.get('phone', '')
                    url = request.form.get('url', '')
                    desc= request.form.get('description', '')

                    try:
                        w = Winery(name=name,
                                   address=address,
                                   phone=phone,
                                   url=url,
                                   description=desc)

                        Session.add(w)
                        Session.commit()
                    except Exception as e:
                        print('unable to add winery')
                        print(e)

                    return winery(w.id)
                else:
                    print('found winery with the same name')
            return redirect('/')
        else:
            return render_template('wineryformpage.html')


    @app.route('/styles')
    @app.route('/styles/<int:_id>')
    def style(_id=None):
        if _id:
            s = Session.query(WineStyle).filter_by(id=_id).first()
            return render_template('winestyle.html', s=s)

        else:
            return 'render all winestyles'


    @app.route('/add/styles', methods=['POST'])
    def add_style():
        if request.form:

            name = request.form.get('name', '')

            s = Session.query(WineStyle).filter_by(name=name).first()
            if not s:
                try:
                    desc = request.form.get('description', '')
                    s = WineStyle(name=name, description=desc)
                    Session.add(s)
                    Session.commit()
                except Exception as e:
                    print('unable to add WineStyle')
                    print(e)

                return style(s.id)
            else:
               print('found winestyle with the same name')
        return redirect('/')

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    app.run(debug=True)


if __name__ == '__main__':
    main()
