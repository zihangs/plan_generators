# Documentation built with MkDocs

(set absolute path)

export DIVERSE_SCORE_COMPUTATION_PATH=/home/zihang/plan_generators/diversescore 

(if permission denied)

sudo chmod +x *.sh

sudo chmod +x *.py

better to use git clone, everything will be executable.

(if "clock" issue)

change ``time.clock()`` to ``time.time()`` in ``src/translate/find_invariants.py``, and then again ``./build.py``.

Install CPLEX: [instructions](http://www.fast-downward.org/LPBuildInstructions)

Deployed and public available URL: https://zihangs.github.io/plan_generators/

## Dataset

Goal and plan recognition dataset can be accessed [here](https://github.com/pucrs-automated-planning/goal-plan-recognition-dataset/)

