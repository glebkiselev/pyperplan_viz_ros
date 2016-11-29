#!
source ../../../../../../devel/setup.bash
roscore & sleep 1
rosrun visualization ros_server_app.py & sleep 1
rosrun visualization pyperplan.py ../../benchmarks/blocks/domain.pddl ../../benchmarks/blocks/task01.pddl -s astar & sleep 1


