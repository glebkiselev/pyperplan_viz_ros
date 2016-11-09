#!/usr/bin/env python3
import networkx as nx
import json

from flask import request, redirect, url_for, session
from networkx.readwrite import json_graph
import flask
import os
import os.path

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pickle

from random import choice

engine = create_engine('sqlite:////tmp/visualizer.db', echo=True)
Base = declarative_base(bind=engine)


class Graph(Base):
    __tablename__ = 'graphs'
    step = Column(Integer, primary_key=True)
    tree = Column(String())

    def __init__(self, step, tree):
        self.step = step
        self.tree = tree
class Rosrecall(Base):
    __tablename__ = 'rosrecalls'
    iterater = Column(Integer, primary_key=True)
    def __init__(self, iterater):
        self.iterater = iterater

Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()

app = flask.Flask(__name__)
g = nx.Graph()
states = []
send_nodes = []
i = 0

def solviz(list_nodes, pop_node):
    pass


def graph_constructor(plan_nodes):
    #creating vertices and saving states
    for x in plan_nodes:
        states.append(x.state)
        # vertex is not a plan node, because nx can't serialize to json an object
        g.add_node(str(x.state))
    # this d3 example uses the name attribute for the mouse-hover value,
    # so add a name to each node
    for n in g:
        g.node[n]['name'] = n

    #creating edges
    for node in plan_nodes:
        if node.parent:
            for nd in g.nodes():
                if nd == str(node.state):
                    finish = nd
                if nd == str(node.parent.state):
                    start = nd
            g.add_edge(start, finish)

    return g
#TODO перенести в сервер
def graphplan(nodes):
    step = 0
    for graph in s.query(Graph):
        step = graph.step + 1
    g = Graph(step, nodes)
    s.add_all([g])
    s.commit()

@app.route("/")
def index():
    s.query(Graph).delete()
    for graph in s.query(Graph):
        print(type(graph), graph.step, pickle.loads(graph.tree.encode()))
    s.commit()
    return flask.render_template("headpiece.html")

@app.route('/signup', methods=['POST'])
def signup():
    s = request.form['nodes']
    if s:
        os.system("bash /home/gleb/strl_local/src/visualization/scripts/pyperplan_viz_ros/run.sh")
    return redirect(url_for('nodes'))


@app.route("/nodes")
def nodes():
    n = request.args.get('next', '')
    if n:
        req = Rosrecall(int(n))
        s.add_all([req])
        s.commit()

    return flask.render_template("graph.html")



@app.route("/data")
def data():
    # global i
    # i = 0
    for graph in s.query(Graph):
        send_nodes.append(pickle.loads(graph.tree.encode()))
    if len(send_nodes) == 0:
        print("SEND_NODES ARE EMPTY!")
    else:
        #TODO kill i!
        g = graph_constructor(send_nodes[len(send_nodes)-1])
        d = json_graph.node_link_data(g)  # node-link format to serialize
        # write json
        return json.dumps(d)

def app_creater():
    port = 8011

    # Open a web browser pointing at the app.
    os.system("gnome-open http://localhost:{0}/".format(port))

    # Set up the development server on port 8000.
    app.debug = False
    app.run(port=port)


if __name__ == "__main__":
    app_creater()


