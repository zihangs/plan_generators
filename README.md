# Documentation built with MkDocs

### A few issues:

need to activate python 3 virtural environment if you have both python 2 and python 3

(set absolute path)

export DIVERSE_SCORE_COMPUTATION_PATH=/home/zihang/plan_generators/diversescore

export DIVERSE_SCORE_COMPUTATION_PATH=/Users/zihangs/plan_generators/diversescore (Mac)

1. need to download diverse score, https://github.com/IBM/diversescore download in /plan_generators
2. /diversescore/translate/invariant_finder.py (time, python 3) time.clock() -> time.time()
3. then cd to /diversescore/ build ./build.py



(if permission denied)

sudo chmod +x *.sh

sudo chmod +x *.py

better to use git clone, everything will be executable.

(if "clock" issue)

change ``time.clock()`` to ``time.time()`` in ``src/translate/find_invariants.py``, and then again ``./build.py``.

Install CPLEX: [instructions](http://www.fast-downward.org/LPBuildInstructions)

Deployed and public available URL: https://zihangs.github.io/plan_generators/

need to activate python 3 virtural environment if you have both python 2 and python 3

## Dataset

Goal and plan recognition dataset can be accessed [here](https://github.com/pucrs-automated-planning/goal-plan-recognition-dataset/)

### Instruction of trace generating script

Required python 3 to run.py. Require to download planners ([FI](https://github.com/IBM/forbiditerative)), store the planners in `./forbiditerative/` directory, need to build and test if the planners can run (a few dependency need to install). The generated traces are stored in `./gene_data/` directory 

**To build a common interface of planner:**

- Where to put the planner (dir)?
- Where are the domain (original) dataset?
- Where does the generated trace stored? 

(TODO: explain the structure of traces).

Planner specific parameters (top_k, diverse_agl, diverse_sat, diverse_bD):

- top_k: planner_name, trace_number
- diverse_agl: planner_name, trace_number
- diverse_sat: planner_name, trace_number, metric, larger_number
- diverse_bD: planner_name, trace_number, metric, bound, larger_number

```sh
# python run.py <planner_name> <trace_number>
python run.py top_k 10

# python run.py <planner_name> <trace_number>
python run.py diverse_agl 10

# python run.py <planner_name> <trace_number> <metric> <larger_number>
python run.py diverse_sat 10 stability 20

# python run.py <planner_name> <trace_number> <metric> <bound> <larger_number>
python run.py diverse_bD 10 stability 0.1 20
```



## Approaches to compare

GR using planner:

Landmark approach (Felipe): https://github.com/pucrs-automated-planning/diverse-plan-rec

GR as planning (Shirin): https://github.com/shirin888/planrecogasplanning-ijcai16-benchmarks

GR approaches mentioned in AAMAS:

landmark approach: https://github.com/pucrs-automated-planning/Planning-GoalRecognition

Code to run AAAI-10 version but using latest BFWS planners as satisficing reasoners: https://github.com/nirlipo/pnet-pr/tree/master/pr_as_planning


