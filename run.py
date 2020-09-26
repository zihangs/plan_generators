import os
import time
import timeout_decorator
import fileinput

# parameter configration
trace_number = 10
observation_percent = [50]
domain_name = "blocks-world"
dataset_name = "goal-plan-recognition-dataset"
timeout_clock = 1   # in seconds


timeout_report_path = './gene_data/report.csv'
data_dir = "gene_data"
domain_dir = "blocks-world"
problems_dir = "problems"
test_dir = "test"

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
		name += (elem + "/")
	return name[0:-1]

@timeout_decorator.timeout(timeout_clock)
def run_planner_with_timeout(planner_dir, trace_number):
	os.system("%s/plan_topk.sh %s/domain.pddl %s/template.pddl %s" % 
			(planner_dir, planner_dir, planner_dir, str(trace_number)))

############## create the dir ###############



for per in observation_percent:
	per_dir = str(per)
	archived_list = os.listdir(path_compose([dataset_name, domain_name, per_dir]))

	# track the template and hyp: check whether the <domain + goals> are identical
	current_template = ""
	current_hyp = ""

	# extract tar.bz2
	count = 0
	for file in archived_list:
		pro_num_dir = str(count)
		test_number_dir = "p_" + str(count)

		current_problem_num_path = path_compose([data_dir, domain_dir, problems_dir, per_dir, pro_num_dir])
		current_test_num_path = path_compose([data_dir, domain_dir, test_dir, per_dir, test_number_dir])
		# only generate once
		train_dir = "train"
		current_train_traces_path = path_compose([data_dir, domain_dir, problems_dir, per_dir, pro_num_dir, train_dir])
		
		create_dir_or_file(current_problem_num_path)
		create_dir_or_file(current_test_num_path)
		create_dir_or_file(current_train_traces_path)

		# copy the original tar.bz2 to current problem dir
		ori_file = path_compose([dataset_name, domain_name, per_dir, file])
		os.system("cp %s %s" % (ori_file, current_problem_num_path))

		# extract copied tar.bz2 file (tar -xvjf filename.tar.bz2)
		copied_tar = path_compose([current_problem_num_path, file])
		os.system("tar -xvjf %s -C %s" % (copied_tar, current_problem_num_path))

		# copy obs file to test dir
		tmp_1 = path_compose([current_problem_num_path, "obs.dat"])
		os.system("cp %s %s" % (tmp_1, current_test_num_path))
		
		# store a copy of template.pddl as template.stable.pddl
		tmp_1 = path_compose([current_problem_num_path, "template.pddl"])
		tmp_2 = path_compose([current_problem_num_path, "template_stable.pddl"])
		os.system("cp %s %s" % (tmp_1, tmp_2))

		# create goal tag in test (goal.txt)
		tmp_1 = path_compose([current_problem_num_path, "hyps.dat"])
		tmp_2 = path_compose([current_problem_num_path, "real_hyp.dat"])
		tmp_3 = path_compose([current_test_num_path, "goal.txt"])
		store_goal(tmp_1, tmp_2, tmp_3)

		# add the cost tag in obs in test set
		tmp_1 = path_compose([current_test_num_path, "obs.dat"])
		with open(tmp_1, 'a') as obs_f:
			obs_f.writelines(';cost')
			obs_f.close()


		# generate traces using planners
		tmp_1 = path_compose([current_problem_num_path, "template.pddl"])
		tmp_2 = path_compose([current_problem_num_path, "hyps.dat"])

		if (len(current_template)>0 and 
			files_equal(current_template, tmp_1) and 
			files_equal(current_hyp, tmp_2)):
			############### current problem is identical as previous, doesn't need run planners #######
			print("skip " + str(count))

			# copy the xes to this folder
			#last_num = str(count - 1)
			#last_folder = path_compose([data_dir, domain_dir, problems_dir, per_dir, last_num, train_dir])
			#copy_xes(last_folder, current_train_traces_path)
		
		else:
			############################# need to call planner ################################

			# select each goal in hyps and replace the line in template

			hyps_f = open(path_compose([current_problem_num_path, "hyps.dat"]))
			num = 0  # goal tag
			line = get_valid_str(hyps_f.readline())

			is_timeout = False

			# for each goal in hyps_f
			while (line):

				# print a progress indicator
				print("Percent: " + str(per) + ", Number: " + str(count) + ", Goal: " + str(num))
				
				hyp = line.replace(",", "\n")
				# template_stable.pddl is always the original file
				tmp_1 = path_compose([current_problem_num_path, "template_stable.pddl"])
				tmp_2 = path_compose([current_problem_num_path, "template.pddl"])
				os.system("cp %s %s" % (tmp_1, tmp_2))

				# replace the <HYPOTHESIS> with a goal
				with fileinput.input(tmp_2, inplace=True) as ft:
					for line in ft:
						new_line = line.replace('<HYPOTHESIS>', hyp)
						print(new_line, end='')

				#################### call plan for each goal ########################
				# copy to the place for calling the planner
				planner_dir = "./forbiditerative"
				tmp_1 = path_compose([current_problem_num_path, "template.pddl"])
				tmp_2 = path_compose([current_problem_num_path, "domain.pddl"])
				os.system("cp %s %s" % (tmp_1, planner_dir))
				os.system("cp %s %s" % (tmp_2, planner_dir))
				
				
				try:
					# need to config parameters
					run_planner_with_timeout(planner_dir, trace_number)
				except:
					os.system("rm -rf ./found_plans/")
					# remove the whole problem and test
					os.system("rm -rf %s/" % current_problem_num_path)
					os.system("rm -rf %s/" % current_test_num_path)

					mode = 'a' if os.path.exists(timeout_report_path) else 'w'
					with open(timeout_report_path, mode) as f:
						f.write("%s, %s, %s, %s\n" % (domain_name, per_dir, pro_num_dir, file))

					is_timeout = True
					break

				# move traces and delete
				os.system("mv ./found_plans/done/ %s/" % current_train_traces_path)
				os.system("rm -rf ./found_plans/")

				# todo check if we get enough traces
				tmp_1 = path_compose([current_train_traces_path, "done"])
				tmp_2 = path_compose([current_train_traces_path, ("goal_" + str(num))])
				os.rename(tmp_1, tmp_2)

				num+=1
				line = get_valid_str(hyps_f.readline())
			
			hyps_f.close()


		if not is_timeout:
			# create XES
			os.system("java -cp xes.jar generate_XES " + current_train_traces_path)

			# update domain and problem file
			current_template = path_compose([current_problem_num_path, "template_stable.pddl"])
			current_hyp = path_compose([current_problem_num_path, "hyps.dat"])

		count += 1

		
		# break control
		if count == 2:
			break
		

	print(count)




