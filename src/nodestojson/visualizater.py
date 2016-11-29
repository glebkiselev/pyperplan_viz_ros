#!/usr/bin/env python3
import networkx as nx
import json

from flask import request, redirect, url_for, session
from networkx.readwrite import json_graph
import flask
import os
import os.path
import pickle
import multiprocessing.dummy as multiprocessing
from nodestojson.dbconnection import Rosrecall, s, Graph

app = flask.Flask(__name__)
g = nx.Graph()
states = []
send_nodes = []
i = 0

def solviz():
    pass


def graph_constructor(plan_nodes):
    #creating vertices and saving states
    for x in plan_nodes:
        states.append(x.state)
        # vertex is not a plan node, because nx can't serialize to json an object
        g.add_node(str(x.state)[11:-2])
    # this d3 uses the name attribute for the mouse-hover value,
    # so add a name to each node
    for n in g:
        g.node[n]['name'] = n
        # g.node[n]['type'] = "typeofnode"

    #creating edges
    for node in plan_nodes:
        if node.parent:
            for nd in g.nodes():
                if nd == str(node.state)[11:-2]:
                    finish = nd
                if nd == str(node.parent.state)[11:-2]:
                    start = nd
            g.add_edge(start, finish)

    return g


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
    def runsh():
        nonlocal s
        if s:
            os.system("bash ../../run.sh")
        return "Nodes have been updated"
    p = multiprocessing.Pool()
    #map_async need to call iterable object - not function name
    p.map_async(lambda iter_for_proc: iter_for_proc(), [runsh])
    p.close()
    p.join()
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
    for graph in s.query(Graph):
        send_nodes.append(pickle.loads(graph.tree.encode()))
    if len(send_nodes) == 0:
        print("SEND_NODES ARE EMPTY!")
    else:
        g = graph_constructor(send_nodes[len(send_nodes)-1])
        d = json_graph.node_link_data(g)  # node-link format to serialize
        # write json
        with open('data.json', 'w') as outfile:
            json.dump(d, outfile)
        return json.dumps(d)

def app_creater():
    port = 8011

    # Open a web browser pointing at the app.
    os.system("google-chrome --incognito http://localhost:{0}/".format(port))

    # Set up the development server on port 8000.
    app.debug = False
    app.run(port=port)


if __name__ == "__main__":
    app_creater()


