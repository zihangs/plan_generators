# Generate plans using forbid iterative planners (top-k, diverse, etc)

This is a tool for creating synthetic plans, the generated plans will be converted to event logs (`.xes` files). Basically, this is a script which wrapped up current exisiting planners and the output data are in a suitable structure and format for our goal recognition experiments.

### Things need to be prepared

1. For running diverse planner, CPLEX and an recommended fast-downward planner is required.

2. Required python 3 runtime environment, I recommend to build a python 3 virtual environment if you both have python 2 and python 3 installed.

3. Need to complie C++ source codes, by following instuctions (CPLEX need to be pre-installed).

4. To configure the command line environment variables in absolute path

   export DIVERSE_SCORE_COMPUTATION_PATH=/home/ubuntu/plan_generators/diversescore (VM)

   export DIVERSE_FAST_DOWNWARD_PLANNER_PATH=/home/ubuntu/plan_generators/fd-red-black-postipc2018 (VM)

   export DIVERSE_SCORE_COMPUTATION_PATH=/Users/zihangs/plan_generators/diversescore (Mac)

5. Download the dataset and put the downloaded dataset in this directory.



### Commands for running the script

Before run the commands, you have to check the parameter configrations, the parameters at the top of `run.py`. Then just run the following commands to starts.

```sh
# activate the python 3 venv (if you don't using venv, ignore this step)
source <venv>/bin/activate

# run script
python run.py
```

It will take a long time to run.



### Outputs

Once the process is completed, check this directory, there will be a sub-directory `gene_data/`. All the domains, problems, tests and generated plans will be there. Then this directory will be used for our next steps for mining process models.

