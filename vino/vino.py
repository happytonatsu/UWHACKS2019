#!/usr/bin/env python

from flask import Flask


def main():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Vino'

    app.run()


if __name__ == '__main__':
    main()
