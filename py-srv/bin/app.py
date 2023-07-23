import cherrypy
import json
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin

import settings
from model import Base, DogModel

class App:
    @property
    def db(self):
        return cherrypy.request.db

    @cherrypy.expose
    def index(self):
        dogs = self.db.query(DogModel).all()
        results = [
            {
                "id": dog.id,
                "breed": dog.breed,
                "color": dog.color
            } for dog in dogs]

        return json.dumps(results)

def run():
    cherrypy.tools.db = SQLAlchemyTool()

    global_config = {
        'global' : {
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : 8080
        }
    }

    app_config = {
        '/' : {
            'tools.db.on': True
        }
    }

    cherrypy.config.update(global_config)

    cherrypy.tree.mount(App(), '/', config=app_config)

    sqlalchemy_plugin = SQLAlchemyPlugin(
        cherrypy.engine, Base,
            '{engine}://{username}:{password}@{host}/{db_name}'.format(
                **settings.SQLSERVER
            ),
        echo=True
    )

    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    run()
