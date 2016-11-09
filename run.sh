#!
source /home/gleb/strl_local/devel/setup.bash
roscore & sleep 1
rosrun visualization ros_server_app.py & sleep 1
rosrun visualization pyperplan.py /home/gleb/strl_local/src/visualization/scripts/pyperplan_viz_ros/benchmarks/blocks/domain.pddl /home/gleb/strl_local/src/visualization/scripts/pyperplan_viz_ros/benchmarks/blocks/task01.pddl -s astar & sleep 1



