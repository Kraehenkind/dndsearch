import os
import json

from flask import (Flask, render_template, redirect, url_for, request, session, g)

from monsters.db import db_connect
from monsters.datacollector import gather_data

def create_app():
    # application factory function
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        MONGO_CLIENT = 'localhost',
        MONGO_PORT = 27017
        )
    
    # create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/", methods=('GET', 'POST'))
    def index():
        export_list = []
        if request.method == 'POST':
            fields = ["index", "name"]
            data=gather_data(request.form, fields)
            for stat in data:
                stat.pop("_id")
                export_list.append(stat)
            export_data = json.dumps(export_list)
        else:
            export_data = json.dumps(export_list)
            
        return render_template('index.html', monster_data = export_data)

    from . import stats
    app.register_blueprint(stats.bp)

    @app.route('/confirm_running')
    def confirm_running():
        return 'RUNNING confirmed'
    
    return app