__author__ = 'claesmathias'


import cherrypy
from Cheetah.Template import Template
import os, json
import matplotlib.pyplot as plt, mpld3

fig_json = ""

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        global fig_json
        t = Template(file="index.tmpl")
        t.title = "CherryPy Cheetah mpld3 Demo"
        t.figure = fig_json
        return str(t)

def main():
    global fig_json

    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8888,
            'server.thread_pool': 8
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    fig = plt.figure()
    plt.plot([3, 1, 4, 1, 5])
    fig_json = json.dumps(mpld3.fig_to_dict(fig))

    cherrypy.config.update({'server.socket_port': 8888})
    cherrypy.quickstart(HelloWorld(), '/', conf)


if __name__ == "__main__":
    main()