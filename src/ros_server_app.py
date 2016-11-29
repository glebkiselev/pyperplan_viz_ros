#!/usr/bin/env python3
try:
    from visualization.srv import *
    import rospy
except ImportError:
    pass
from nodestojson.dbconnection import graphplan, solution, Rosrecall, s

def handle_nodes(req):
    graphplan(req.nodes)
    solution(req.solution)
    a = 0
    while a != 1:
        rospy.sleep(1)
        for recall in s.query(Rosrecall):
            a = recall.iterater
    s.query(Rosrecall).delete()
    s.commit()
    print("responce was sent")
    return PlanNodesResponse(a)

def nodes_creater_server():
    rospy.init_node('nodes_server')
    s = rospy.Service('draw_some_nodes', PlanNodes, handle_nodes)
    print('ready to draw nodes')
    rospy.spin()

if __name__ == "__main__":
    nodes_creater_server()