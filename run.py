import os
import sys
import time
import fileinput

from config_param import *

# CONSTANt VARIABLES
OBSERVATION_PERCENT = [10, 30, 50, 70, 100]
DATASET_NAME = "goal-plan-recognition-dataset"
PROBLEM_DIR = "problems"
TEST_DIR = "test"
TIMEOUT_REPORT_PATH = './gene_data/report.csv'
OUTPUT = "gene_data"

################################# HELPER FUNCTIONS ##############################
# To check whether two problems are identical
def files_equal(file1, file2):
	f1 = open(file1, "r")
	f2 = open(file2, "r")
	line1 = f1.readline()
	line2 = f2.readline()
	while (line1 and line2):
		if not (line1 == line2):
			print("different")
			return False
		line1 = f1.readline()
		line2 = f2.readline()

	return True

# Store the tag number of real goal in a txt file, the number tag starts from 0
def store_goal(hyps, real_hyp, store):
	f1 = open(hyps, "r")
	f2 = open(real_hyp, "r")
	# Remove "\n"
	a_hyp = get_valid_str(f1.readline())
	real = get_valid_str(f2.readline())

	count = 0
	while (a_hyp):
		if (a_hyp == real):
			print("Store goal No. " + str(count))
			txt = open(store, "w")
			txt.writelines(str(count))

			f1.close()
			f2.close()
			txt.close()
			return count # Real goal found

		a_hyp = get_valid_str(f1.readline())
		count += 1

	print("Error: Not found the real goal")
	return os._exit(0)

# Remove the invalid char at the end of strings
def get_valid_str(string):
	if string:
		invalid_char = ["\n","\r"]
		while(string[-1] in invalid_char):
			string = string[0:-1]
		if len(string) == 0:
			print("Error: Empty string")
			os._exit(0)
		return string

	return string

# Check and generate file or dir
def create_dir_or_file(name):
	if not os.path.exists(name):
		os.makedirs(name)
	else:
		print("Error: " + name + " ---- already exists")
		os._exit(0)
	return 0   # Sucessfully created the dir

# Can return either a directory or a file
def path_compose(nameList):
	name = ""
	for elem in nameList:
		if type(elem) is str:
			pass
		else: 
			elem = str(elem)
		name += (elem + "/")
	return name[0:-1]

# Run the planner, with a timeout setting
# @timeout_decorator.timeout(TIMEOUT_CLOCK)
def run_planner_with_timeout(planner_dir, trace_number):
	# for differet planners

	if planner_name == "top_k":
		print(os.getcwd())
		os.chdir("%s" % planner_dir)
		print("here")
		print(os.getcwd())
		exit_code = os.system("timeout %s ./plan_topk.sh domain.pddl template.pddl %s" % 
				(str(TIMEOUT_CLOCK), str(trace_number)))
		os.chdir("..")

	elif planner_name == "diverse_agl":
		os.chdir("%s" % planner_dir)
		exit_code = os.system("timeout %s ./plan_diverse_agl.sh domain.pddl template.pddl %s" % 
				(str(TIMEOUT_CLOCK), str(trace_number)))
		os.chdir("..")

	# need change directory
	elif planner_name == "diverse_sat":
		os.chdir("%s" % planner_dir)
		exit_code = os.system("timeout %s ./plan_diverse_sat.sh domain.pddl template.pddl %s %s %s" % 
				(str(TIMEOUT_CLOCK), str(trace_number), metric, str(larger_number)))
		os.chdir("..")

	elif planner_name == "diverse_bD":
		os.chdir("%s" % planner_dir)
		exit_code = os.system("timeout %s ./plan_diverse_bounded.sh domain.pddl template.pddl %s %s %s %s" % 
				(str(TIMEOUT_CLOCK), str(trace_number), metric, bound, str(larger_number)))
		os.chdir("..")

	else:
		print("No planner founded!")
		os._exit(0)

	if exit_code != 0:
		return True  # timeout = true
	else:
		return False # no timeout
		


########################### Wrap the miner #########################
## Parameters are from another file: config_param.py

def miner(directory):
	for filename in os.listdir(directory):
		if filename.endswith(".xes"):
			filename = directory + "/" +filename
			output = filename + ".pnml"

			if miner_name == "-TSM":
				os.system("java -cp miner.jar autoMiner -TSM %s %s %s %s %s" % (filename, output, param_dict["TSM_No_limit"], param_dict["TSM_Event_Percentage"], param_dict["TSM_Label_Percentage"]))
			
			if miner_name == "-DFM":
				os.system("java -cp miner.jar autoMiner -DFM %s %s %s" % (filename, output, param_dict["DFM_Threshold"]))

			if miner_name == "-IM":
				os.system("java -cp miner.jar autoMiner -IM %s %s %s" % (filename, output, param_dict["IM_Threshold"]))


###################################### HELPER CLASSES ##################################
class problem:
	def __init__(self, template, hyp):
		self.template = template
		self.hyp = hyp

	def exist(self):
		return self.template and self.hyp  # "" is Flase, otherwise True

	def identical(self, other):  # Input: a instance of problem
		return files_equal(self.template, other.template) and files_equal(self.hyp, other.hyp)


class extracted_dir:
	def __init__(self, data_output, domain, percentage, number, file):

		# Info
		self.data_output = data_output
		self.domain = domain
		self.percentage = percentage
		self.number = number
		self.tar = file

		# Prepare
		self.create_problem_path()
		self.create_test_path()
		self.create_train_trace_path()

	def create_problem_path(self):
		path = path_compose([self.data_output, self.domain, PROBLEM_DIR, self.percentage, self.number])
		create_dir_or_file(path)
		self.current_problem_num_path = path

	def create_test_path(self):
		## self.number :: "p_" + str(self.number)
		path = path_compose([self.data_output, self.domain, TEST_DIR, self.percentage, self.number])
		create_dir_or_file(path)
		self.current_test_num_path = path

	def create_train_trace_path(self):
		path = path_compose([self.data_output, self.domain, PROBLEM_DIR, self.percentage, self.number, "train"])
		create_dir_or_file(path)
		self.current_train_traces_path = path

	def extract_tar(self):
		tar_file = path_compose([DATASET_NAME, self.domain, self.percentage, self.tar])
		os.system("tar -xvjf %s -C %s" % (tar_file, self.current_problem_num_path))

	def copy_obs_to_test(self):
		tmp = path_compose([self.current_problem_num_path, "obs.dat"])
		os.system("cp %s %s" % (tmp, self.current_test_num_path))

	def store_template_stable(self):
		# Store a copy of template.pddl as template.stable.pddl
		tmp_1 = path_compose([self.current_problem_num_path, "template.pddl"])
		tmp_2 = path_compose([self.current_problem_num_path, "template_stable.pddl"])
		os.system("cp %s %s" % (tmp_1, tmp_2))

	def add_goal_tag(self):
		tmp_1 = path_compose([self.current_problem_num_path, "hyps.dat"])
		tmp_2 = path_compose([self.current_problem_num_path, "real_hyp.dat"])
		tmp_3 = path_compose([self.current_test_num_path, "goal.txt"])
		store_goal(tmp_1, tmp_2, tmp_3)

	def add_cost_suffix(self):
		file = path_compose([self.current_test_num_path, "obs.dat"])
		with open(file, 'a') as obs_f:
			obs_f.writelines(';cost')
			obs_f.close()

class planner_manager:
	def __init__(self, extracted_dir):
		self.extracted_dir = extracted_dir

	def open_hyps_file(self):
		self.hyps_list = open(path_compose([self.extracted_dir.current_problem_num_path, "hyps.dat"]))

	def close_hyps_file(self):
		self.hyps_list.close()

	# Iterate all goals (hyps), and generate plans for each goal and templete domain.
	# Return an indicator of timeout (True = timeout and failed / False = succeed)
	def iter_each_goals(self):
		self.open_hyps_file()
		current_goal = get_valid_str(self.hyps_list.readline())
		planner_dir = "./forbiditerative"


		is_timeout = False
		# Goal tag starts from 0
		num = 0
		while (current_goal):
			current_goal = current_goal.replace(",", "\n")
			# Duplicate a template.pddl and rename as template_stable.pddl
			tmp_1 = path_compose([self.extracted_dir.current_problem_num_path, "template_stable.pddl"])
			tmp_2 = path_compose([self.extracted_dir.current_problem_num_path, "template.pddl"])
			os.system("cp %s %s" % (tmp_1, tmp_2))

			# Replace the <HYPOTHESIS> with a goal (hyp)
			with fileinput.input(tmp_2, inplace=True) as ft:
				for line in ft:
					new_line = line.replace('<HYPOTHESIS>', current_goal)
					print(new_line, end='')

			# Generate plans (maybe timeout)
			is_timeout = self.create_plans(planner_dir)
			if is_timeout:
				break

			# TODO: check if we get enough traces
			# add code later

			# Where is the output directory

			# Move traces and delete
			if planner_name == "diverse_agl":
				os.system("mv %s/found_plans/ %s/" % (planner_dir, self.extracted_dir.current_train_traces_path))
				os.system("rm -rf %s/found_plans/" % planner_dir)

				# Rename
				tmp_1 = path_compose([self.extracted_dir.current_train_traces_path, "found_plans"])
				tmp_2 = path_compose([self.extracted_dir.current_train_traces_path, ("goal_" + str(num))])
				os.rename(tmp_1, tmp_2)

			# elif planner_name in ["diverse_sat", "diverse_bD"]:
			else:
				os.system("mv %s/found_plans/done/ %s/" % (planner_dir, self.extracted_dir.current_train_traces_path))
				os.system("rm -rf %s/found_plans/" % planner_dir)

				# Rename
				tmp_1 = path_compose([self.extracted_dir.current_train_traces_path, "done"])
				tmp_2 = path_compose([self.extracted_dir.current_train_traces_path, ("goal_" + str(num))])
				os.rename(tmp_1, tmp_2)


			num+=1
			# Update current goal
			current_goal = get_valid_str(self.hyps_list.readline())
		self.close_hyps_file()

		return is_timeout


	def create_plans(self, planner_dir):
		# copy pddls to right place
		
		tmp_1 = path_compose([self.extracted_dir.current_problem_num_path, "template.pddl"])
		tmp_2 = path_compose([self.extracted_dir.current_problem_num_path, "domain.pddl"])
		os.system("cp %s %s" % (tmp_1, planner_dir))
		os.system("cp %s %s" % (tmp_2, planner_dir))

		timeout = run_planner_with_timeout(planner_dir, trace_number)

		if timeout:
			os.system("rm -rf %s/found_plans/" % planner_dir)
			# remove the whole problem and test
			os.system("rm -rf %s/" % self.extracted_dir.current_problem_num_path)
			os.system("rm -rf %s/" % self.extracted_dir.current_test_num_path)

			mode = 'a' if os.path.exists(TIMEOUT_REPORT_PATH) else 'w'
			with open(TIMEOUT_REPORT_PATH, mode) as f:
				f.write("%s, %s, %s, %s\n" % (self.extracted_dir.domain,
					self.extracted_dir.percentage, self.extracted_dir.number,
					self.extracted_dir.tar))

		return timeout


################################## MAIN SCRIPT ############################
# CONFIGURABLE VARIABLES (config_param.py)
if planner_name == "diverse_sat":
	# trace_number = int(sys.argv[2])
	trace_number = int(param_dict["Diverse_sat_traces"])
	metric = param_dict["Diverse_sat_metric"]  # stability, uniqueness, state
	larger_number = int(param_dict["Diverse_sat_larger_traces"])

elif planner_name == "top_k":
	trace_number = int(param_dict["Topk_traces"])

elif planner_name == "diverse_agl":
	trace_number = int(param_dict["Diverse_agl_traces"])

elif planner_name == "diverse_bD":
	trace_number = int(param_dict["Diverse_bD_traces"])
	metric = param_dict["Diverse_bD_metric"]  # stability, uniqueness, state
	bound = float(param_dict["Diverse_bD_bound"])
	larger_number = int(param_dict["Diverse_bD_larger_traces"])

for domain in DOMAIN_LIST:
	for per in OBSERVATION_PERCENT:
		archived_list = os.listdir(path_compose([DATASET_NAME, domain, per]))

		# track the template and hyp: check whether the <domain + goals> are identical
		current_problem = problem("", "") # initialize the first problem

		# extract tar.bz2
		count = 0
		for file in archived_list:
			working_dir = extracted_dir(OUTPUT, domain, per, count, file)
			working_dir.extract_tar()
			working_dir.copy_obs_to_test()
			working_dir.store_template_stable()
			working_dir.add_goal_tag()
			working_dir.add_cost_suffix()
			# generate tmp_problem for tracking
			tmp_problem = problem(path_compose([working_dir.current_problem_num_path, "template.pddl"]),
				path_compose([working_dir.current_problem_num_path, "hyps.dat"]))

			has_timeout = False

			if (current_problem.exist() and current_problem.identical(tmp_problem)):
				# current problem is identical as previous, doesn't need run planners
				print("skip " + str(count))
			
			else:
				############################# need to call planner ################################

				manager = planner_manager(working_dir)
				has_timeout = manager.iter_each_goals()

			if not has_timeout:
				# create XES
				os.system("java -cp xes.jar generate_XES " + working_dir.current_train_traces_path)

				# mine models
				miner(working_dir.current_train_traces_path)

				# update domain and problem file
				current_problem = tmp_problem

			count += 1

			# break control
			if count == 2:
				break







