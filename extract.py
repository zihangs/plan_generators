import os
import fileinput

trace_number = 100
observation_percent = [10,30,50,70,100]

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

def store_goal(hyps, real_hyp, store):
	f1 = open(hyps, "r")
	f2 = open(real_hyp, "r")
	a_hyp = f1.readline()[0:-1]
	real = f2.readline()
	count = 0
	while (a_hyp):
		if (a_hyp == real):
			print("Store goal No. " + str(count))
			txt = open(store, "w")
			txt.writelines(str(count))

			f1.close()
			f2.close()
			txt.close()
			return count
		a_hyp = f1.readline()[0:-1]
		count += 1

	return False

def copy_xes(last_folder, current_folder):
	arr = os.listdir(last_folder)
	for file in arr:
		if file[0] == 'c':
			os.system("cp " + last_folder + file + " " + current_folder)

		# else we can remove the folder
		# rm -r last_folder file


# create problem and test folder
new_folder_lv1 = "./problems/"
test_lv1 = "./test/"
os.mkdir(new_folder_lv1)
os.mkdir(test_lv1)



for percent in observation_percent:

	new_folder_lv1 = "./problems/" + str(percent) + "/"
	test_lv1 = "./test/" + str(percent) + "/"

	os.mkdir(new_folder_lv1)
	os.mkdir(test_lv1)

	ori_folder = "./" + str(percent) + "/"
	arr = os.listdir(ori_folder)

	current_template = ""
	current_hyp = ""

	count = 0
	for file in arr:
		new_folder_lv2 = new_folder_lv1 + str(count) + "/"
		test_lv2 = test_lv1 + "p_" + str(count) + "/"
		train_traces = new_folder_lv2 + "train/"
		os.mkdir(test_lv2)
		os.mkdir(new_folder_lv2)
		os.mkdir(train_traces)

		os.system("cp " + ori_folder + file + " " + new_folder_lv2)
		os.system("tar -xvjf " + new_folder_lv2 + file + " -C " + new_folder_lv2)  # tar -xvjf filename.tar.bz2
		os.system("cp " + new_folder_lv2 + "obs.dat " + test_lv2)  # copy obs file to test
		os.system("cp " + new_folder_lv2 + "template.pddl " + new_folder_lv2 + "template_stable.pddl")

		store_goal(new_folder_lv2+"hyps.dat", new_folder_lv2+"real_hyp.dat", test_lv2+"goal.txt")

		# rewrite the plan
		with open(test_lv2+"obs.dat", 'a') as file:
			file.writelines(';cost')
			file.close()

		if ((len(current_template)>0) and 
			(files_equal(current_template, new_folder_lv2+"template.pddl") and 
				files_equal(current_hyp, new_folder_lv2+"hyps.dat"))):
			# copy the xes files to this folder
			last_folder = new_folder_lv1 + str(int(new_folder_lv2[-2]) - 1) + "/train/"
			
			# copy_xes(last_folder, train_traces)

			print("skip " + str(count))

		else:
		# rewrite the templete
			f = open(new_folder_lv2+"hyps.dat")
			num = 0
			line = f.readline()
			while (line):

				# indicate the progress
				print("Percent: " + str(percent) + ", Number: " + str(count) + ", Goal: " + str(num))

				hyp = line.replace(",", "\n")
				os.system("cp " + new_folder_lv2 + "template_stable.pddl " + new_folder_lv2 + "template.pddl")
				with fileinput.input(new_folder_lv2+"template.pddl", inplace=True) as ft:
					for line in ft:
						new_line = line.replace('<HYPOTHESIS>', hyp)
						print(new_line, end='')

				# copy to the place for using k-planner
				os.system("cp " + new_folder_lv2 + "template.pddl " + "./pnet-pr/benchmarks/domains/grid/instances/")
				os.system("cp " + new_folder_lv2 + "domain.pddl " + "./pnet-pr/benchmarks/domains/grid/")
				os.chdir("./pnet-pr/benchmarks/")
				os.system("python run.py benchmark ../kstar/fast-downward.py domains result_domains " + str(trace_number))
				os.system("mv ./grid_template_plans/ " + "../../" + train_traces)

				# change back
				os.chdir("../../")
				os.rename(train_traces + "grid_template_plans/", train_traces + "goal_" + str(num) + "/")
				
				num+=1
				
				line = f.readline()
			f.close()

		# created XES
		os.system("java -cp xes.jar generate_XES "+train_traces)
		current_template = new_folder_lv2+"template_stable.pddl"
		current_hyp = new_folder_lv2+"hyps.dat"
		# created pnml using split miner  (only in windows)

		count+=1
		if count == 2:
			break

	print(count)

'''
	ori_folder = "./" + str(per) + "/"
	arr = os.listdir(ori_folder)

	current_problem = ""
	for file in arr:
		name = file.split("_")
		if name[0]+name[1] != current_problem:
			current_problem = name[0]+name[1]
			new_folder_lv2 = new_folder_lv1 + current_problem + "/"
			os.mkdir(new_folder_lv2)

		os.system("cp " + ori_folder + file + " " + new_folder_lv2)

		goal = name[2].split("-")[1]
		print(goal)
'''


		
