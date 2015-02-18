__author__ = 'claesmathias'


import cherrypy
from Cheetah.Template import Template
import os, json
from yahoo_finance import Share
import matplotlib.pyplot as plt, mpld3
import numpy as np

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

    #fig = plt.figure()
    vdsi = Share('VDSI')
    historical = vdsi.get_historical('2014-12-01', '2015-01-31')

    adj_close = []
    width = 0.5

    for i in range(0, len(historical)):
        adj_close = np.append(adj_close, float(historical[i]['Adj_Close']))

    #plt.plot(adj_close)
    fig, ax = plt.subplots()
    x = range(0, len(adj_close))
    bars = ax.bar(x, adj_close, width)
    fig_json = json.dumps(mpld3.fig_to_dict(fig))

    cherrypy.config.update({'server.socket_port': 8888})
    cherrypy.quickstart(HelloWorld(), '/', conf)


if __name__ == "__main__":
    main()