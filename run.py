import os
import time
import timeout_decorator
import fileinput

# parameter configration
trace_number = 10
observation_percent = [50]
domain_name = "blocks-world"
dataset_name = "goal-plan-recognition-dataset"
timeout_clock = 100  # in seconds

timeout_report_path = './gene_data/report.csv'

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

# store the tag number of real goal in a txt file
# the number tag starts from 0
def store_goal(hyps, real_hyp, store):
	f1 = open(hyps, "r")
	f2 = open(real_hyp, "r")
	# remove "\n"
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
			return count # real goal found

		a_hyp = get_valid_str(f1.readline())
		count += 1

	print("Error: Not found the real goal")
	return os._exit(0)

# remove the invalid char at the end of strings
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

# check and generate file or dir
def create_dir_or_file(name):
	if not os.path.exists(name):
		os.makedirs(name)
	else:
		print("Error: " + name + " ---- already exists")
		os._exit(0)
	return 0   # sucessfully created the dir

# can return either dir or file
def path_compose(nameList):
	name = ""
	for elem in nameList:
		if type(elem) is str:
			pass
		else: 
			elem = str(elem)
		name += (elem + "/")
	return name[0:-1]

@timeout_decorator.timeout(timeout_clock)
def run_planner_with_timeout(planner_dir, trace_number):
	os.system("%s/plan_topk.sh %s/domain.pddl %s/template.pddl %s" % 
			(planner_dir, planner_dir, planner_dir, str(trace_number)))


class problem:
	def __init__(self, template, hyp):
		self.template = template
		self.hyp = hyp

	def exist(self):
		return self.template and self.hyp  # "" is Flase, otherwise True

	def identical(self, other):  # a instance of problem
		return files_equal(self.template, other.template) and files_equal(self.hyp, other.hyp)


class extracted_dir:
	def __init__(self, data_output, domain, percentage, number, file):

		# info
		self.data_output = data_output
		self.domain = domain
		self.percentage = percentage
		self.number = number
		self.tar = file

		# prepare
		self.create_problem_path()
		self.create_test_path()
		self.create_train_trace_path()

	def create_problem_path(self):
		path = path_compose([self.data_output, self.domain, PROBLEM_DIR, self.percentage, self.number])
		create_dir_or_file(path)
		self.current_problem_num_path = path

	def create_test_path(self):
		# test_number_dir = "p_" + str(count)
		path = path_compose([self.data_output, self.domain, TEST_DIR, self.percentage, self.number])
		create_dir_or_file(path)
		self.current_test_num_path = path

	def create_train_trace_path(self):
		path = path_compose([self.data_output, self.domain, PROBLEM_DIR, self.percentage, self.number, "train"])
		create_dir_or_file(path)
		self.current_train_traces_path = path

	def extract_tar(self):
		tar_file = path_compose([dataset_name, self.domain, self.percentage, self.tar])
		os.system("tar -xvjf %s -C %s" % (tar_file, self.current_problem_num_path))

	def copy_obs_to_test(self):
		tmp = path_compose([self.current_problem_num_path, "obs.dat"])
		os.system("cp %s %s" % (tmp, self.current_test_num_path))

	def store_template_stable(self):
		# store a copy of template.pddl as template.stable.pddl
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

	def iter_each_goals(self):
		self.open_hyps_file()
		current_goal = get_valid_str(self.hyps_list.readline())
		is_timeout = False
		# goal tag start from 0
		num = 0
		while (current_goal):
			current_goal = current_goal.replace(",", "\n")
			# duplicate a template.pddl and rename as template_stable.pddl
			tmp_1 = path_compose([self.extracted_dir.current_problem_num_path, "template_stable.pddl"])
			tmp_2 = path_compose([self.extracted_dir.current_problem_num_path, "template.pddl"])
			os.system("cp %s %s" % (tmp_1, tmp_2))

			# replace the <HYPOTHESIS> with a goal
			with fileinput.input(tmp_2, inplace=True) as ft:
				for line in ft:
					new_line = line.replace('<HYPOTHESIS>', current_goal)
					print(new_line, end='')

			# generate plans
			is_timeout = self.create_plans()
			if is_timeout:
				break

			# move traces and delete
			os.system("mv ./found_plans/done/ %s/" % self.extracted_dir.current_train_traces_path)
			os.system("rm -rf ./found_plans/")

			# todo check if we get enough traces
			tmp_1 = path_compose([self.extracted_dir.current_train_traces_path, "done"])
			tmp_2 = path_compose([self.extracted_dir.current_train_traces_path, ("goal_" + str(num))])
			os.rename(tmp_1, tmp_2)

			num+=1
			current_goal = get_valid_str(self.hyps_list.readline())
		self.close_hyps_file()

		return is_timeout

	def create_plans(self):
		# copy pddls to right place
		planner_dir = "./forbiditerative"
		tmp_1 = path_compose([self.extracted_dir.current_problem_num_path, "template.pddl"])
		tmp_2 = path_compose([self.extracted_dir.current_problem_num_path, "domain.pddl"])
		os.system("cp %s %s" % (tmp_1, planner_dir))
		os.system("cp %s %s" % (tmp_2, planner_dir))
		try:
			# need to config parameters
			run_planner_with_timeout(planner_dir, trace_number)
			# return timeout = False
			return False
		except:
			os.system("rm -rf ./found_plans/")
			# remove the whole problem and test
			os.system("rm -rf %s/" % self.extracted_dir.current_problem_num_path)
			os.system("rm -rf %s/" % self.extracted_dir.current_test_num_path)

			mode = 'a' if os.path.exists(timeout_report_path) else 'w'
			with open(timeout_report_path, mode) as f:
				f.write("%s, %s, %s, %s\n" % (self.extracted_dir.domain,
					self.extracted_dir.percentage, self.extracted_dir.number,
					self.extracted_dir.tar))
			# return timeout = True
			return True


############## create the dir ###############
PROBLEM_DIR = "problems"
#problems_dir
TEST_DIR = "test"
#test_dir
data_dir = "gene_data"
domain_dir = "blocks-world"

for per in observation_percent:
	archived_list = os.listdir(path_compose([dataset_name, domain_name, per]))

	# track the template and hyp: check whether the <domain + goals> are identical
	current_problem = problem("", "") # initialize the first problem

	# extract tar.bz2
	count = 0
	for file in archived_list:
		working_dir = extracted_dir(data_dir, domain_dir, per, count, file)
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

			# update domain and problem file
			current_problem = tmp_problem

		count += 1

		# break control
		if count == 2:
			break




