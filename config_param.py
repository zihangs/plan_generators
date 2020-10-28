# python venv: source <venv>/bin/activate

# need to configure (set absolute path)
# export DIVERSE_SCORE_COMPUTATION_PATH=/home/zihang/plan_generators/diversescore

# python run.py top_k 10
# python run.py diverse_agl 10
# python run.py diverse_sat 10 stability 20
# python run.py diverse_bD 10 stability 0.1 20

miner_name = "-DFM"     #["-TSM", "-IM", "-DFM"]
planner_name = "top_k"  #[top_k, diverse_agl, diverse_sat, diverse_bD]
DOMAIN_LIST = ["sokoban"]
TIMEOUT_CLOCK = 1800  # in seconds (for planner)


param_dict = {
	##### miners #####
	"TSM_No_limit": -1,
	"TSM_Event_Percentage": 100,
	"TSM_Label_Percentage": 100,

	"DFM_Threshold": 0.0,

	"IM_Threshold": 0.0,

	##### planners #####
	"Topk_traces": 100,

	"Diverse_agl_traces": 10,

	"Diverse_sat_traces": 10,
	"Diverse_sat_metric": "stability",
	"Diverse_sat_larger_traces": 20,

	"Diverse_bD_traces": 10,
	"Diverse_bD_metric": "stability",
	"Diverse_bD_bound": 0.1,
	"Diverse_bD_larger_traces": 20
}
