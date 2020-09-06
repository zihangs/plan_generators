import os
import fileinput

# parameter configration
trace_number = 100
observation_percent = [10,30,50,70,100]
domain_name = "blocks-world"
dataset_name = "goal-plan-recognition-dataset"

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
	invalid_char = ["\n","\r"]
	while(string[-1] in invalid_char):
		string = string[0:-1]
	if len(string) == 0:
		print("Error: Empty string")
		os._exit(0)
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

############## create the dir ###############

data_dir = "gene_data"
domain_dir = "blocks-world"
problems_dir = "problems"
test_dir = "test"

for per in observation_percent:
	per_dir = str(per)

	# create_dir_or_file(path_compose([data_dir, domain_dir, problems_dir, per_dir]))
	# create_dir_or_file(path_compose([data_dir, domain_dir, test_dir, per_dir]))
	# 

	archived_list = os.listdir(path_compose([dataset_name, domain_name, per_dir]))
	print(len(archived_list))

	# extract tar.bz2

	# prepare test set

	# prepare problem set
	    # sas to xes



