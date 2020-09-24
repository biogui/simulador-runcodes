#!/usr/bin/python3
# Python Scrypt by Guilherme Rios(Bio) - 2020
import subprocess
from sys import argv
from os import system, listdir, path

UNIC = 0
MULTIPLE = 1

VERBOSE = 0
QUIET = 1

TAB = "    "

# Valid paths's arguments ##########################################################################
if len(argv) < 3:
	print("Run with valid arguments!")
	exit()
if not path.isdir(argv[-1]) and argv[-1][-4:] != ".zip":
	print("Run with valid tests' path argument!")
	exit()
if argv[-2][-2:] != ".c" and argv[-2][-8:] != "Makefile":
	print("Run with valid arguments!")
	exit()

IGNORE_MODE = True if argv[1] == "-i" else False
PROGRAM_PATH = f"./{argv[-2]}"
TESTS_PATH = f"./{argv[-1]}"

class S: # Style flags
	none = ";0"
	strong = ";1"
	blur = ";2"
	italic = ";3"
	underline = ";4"
	flash = ";6"
	negative = ";7"
	strike = ";9"

class C: # Colors flags
	none = ";50"
	black = ";30"
	red = ";31"
	green = ";32"
	yellow = ";33"
	blue = ";34"
	purple = ";35"
	cyan = ";36"
	white = ";37"

def stylizes_str(string, color=C.none, style=S.none):
	start = "\033[0{}{}m".format(style, color)
	end = "\033[m"
	return "{}{}{}".format(start, string, end)

def get_program_dirr(path):
	for i, char in enumerate(path[::-1]):
		if char == '/':
			return path[:len(path)-i]

def get_program_name(prev_files, curr_files):
	for file in curr_files:
		if file not in prev_files:
			if file.split(".")[-1] not in ["o", "gch"]:
				return file

def get_inputs_and_outputs(tests_dirr):
	ins = list()
	outs = list()

	files = listdir(tests_dirr)
	for file in files:
		if file[-3:] == ".in":
			out_pair = f"{file[:-3]}.out"

			if out_pair in files:
				ins.append(f"{tests_dirr}/{file}")
				outs.append(f"{tests_dirr}/{out_pair}")

	return ins, outs

def len_to_ignore_mode(line):
	for i, char in enumerate(line):
		if char == '\n' or char == '\r':
			return i

	# EOF case
	return i + 1

def is_correct(out_file, my_file):
	expected_out = open(out_file, "rb")
	my_out = open(my_file, "rb")

	line_posix = 0
	errors = dict()
	over_lines = list()
	while True:
		try:
			expected_line = expected_out.readline().decode()
			my_line = my_out.readline().decode()
			line_posix += 1

			ex_len = len(expected_line)
			my_len = len(my_line)

			if ex_len == 0 and my_len == 0:
				break

			if ex_len == 0:
				while my_line:
					over_lines.append(my_line)
					my_line = my_out.readline().decode()
				over_lines.insert(0, "surplus")

				break

			if my_len == 0:
				over_lines = list()
				while expected_line:
					over_lines.append(expected_line)
					expected_line = expected_out.readline().decode()
				over_lines.insert(0, "missing")

				break

			if expected_line != my_line:
				pos_fails = list()

				# Recalculate lenths ignoring 
				if IGNORE_MODE:
					ex_len = len_to_ignore_mode(expected_line)
					my_len = len_to_ignore_mode(my_line)

				min_len = min(my_len, ex_len)
				max_len = max(my_len, ex_len)

				for i in range(min_len):
					if expected_line[i] != my_line[i]:
						pos_fails.append(i)

				for i in range(min_len, max_len):
					pos_fails.append(i)

				if pos_fails:
					errors[line_posix] = (expected_line, my_line, pos_fails)

		except UnicodeDecodeError:
			pass

	if over_lines: errors[-line_posix] = over_lines
	is_correct = True
	if len(errors) > 0:
		is_correct = False

	return is_correct, errors

def define_emoji(n_corrects, n_cases):
	if n_corrects == n_cases:
		return stylizes_str("(o゜▽゜)o☆", style=S.strong)
	elif n_corrects > 3*n_cases//4:
		return stylizes_str("o(*￣▽￣*)o", style=S.strong)
	elif n_corrects > n_cases//2:
		return stylizes_str("^____^", style=S.strong)
	elif n_corrects > n_cases//4:
		return stylizes_str("(┬┬﹏┬┬)", style=S.strong)
	else:
		return stylizes_str("(╯°□°）╯︵ ┻━┻", style=S.strong)

def print_errors(all_errors):
	ex_indicator = stylizes_str("> |", C.green)
	my_indicator = stylizes_str("< |", C.red)
	arrow = stylizes_str("╰-> ", style=S.strong)

	separator = stylizes_str('-' * 77, style=S.strong)
	title = " Differences "
	print(stylizes_str(f"{title:-^77}", style=S.strong))

	for case, case_errors in all_errors.items():
		print(stylizes_str(f"Case {case}:", style=S.strong))

		for line, error in case_errors.items():
			if line < 0:
				print(f"{arrow}{error[0]} lines from the line {-line}:")
				if error[0] == "surplus":
					indicator = stylizes_str("< ", C.red)
					color = C.red
				elif error[0] == "missing":
					indicator = stylizes_str("> ", C.green)
					color = C.green

				for over_line in error[1:]:
					over_line = stylizes_str(over_line, color)
					print(f"{TAB}{indicator}{over_line}", end="")

				break

			print(f"{arrow}line {line}:")
			print(f"{TAB}{ex_indicator}", end="")
			for pos, eChr in enumerate(error[0]):
				if eChr == '\r':
					char = "\\r"
				elif eChr == '\n':
					char = "\\n"
				else:
					char = eChr

				if pos in error[2]:
					char = stylizes_str(char, C.green)

				print(char, end="")
			print(stylizes_str("|", C.green))

			print(f"{TAB}{my_indicator}", end="")
			for pos, mChr in enumerate(error[1]):
				if mChr == '\r':
					char = "\\r"
				elif mChr == '\n':
					char = "\\n"
				else:
					char = mChr

				if pos in error[2]:
					char = stylizes_str(char, C.red)
				print(char, end="")
			print(stylizes_str("|", C.red))

		print(f"\n{separator}")

# Compile ##########################################################################################
if PROGRAM_PATH[-8:] == "Makefile":
	mode = MULTIPLE
	program_dirr = get_program_dirr(PROGRAM_PATH)
	prev_files = listdir(program_dirr)

	cmd = subprocess.Popen(["make", "all"], stderr=subprocess.PIPE)
	error_out = cmd.stderr.read()

	if error_out:
		system("make all")
		print("\nMakefile error! Exiting...")
		exit()

	curr_files = listdir(program_dirr)
	program = get_program_name(prev_files, curr_files)
	system(f"rm -f {PROGRAM_PATH[:-8]}*.o {PROGRAM_PATH[:-8]}*.gch")

else:
	mode = UNIC
	program = PROGRAM_PATH[:-2]

	cmd = subprocess.Popen(["gcc", f"{program}.c", "-o", program, "-g", "-Wall", "-Werror", "-lm"], stderr=subprocess.PIPE)
	error_out = cmd.stderr.read()

	if error_out:
		system(f"gcc {flags} {program}.c -o {program}")

		print("\nCompilation error! Exiting...")
		exit()

# Set dirr to inputs and outputs ###################################################################
if TESTS_PATH[-4:] == '.zip':
	tests_dirr = "tests/"
	cmd = subprocess.Popen(["unzip", "-qqo", TESTS_PATH, "-d", tests_dirr], stderr=subprocess.PIPE)
	error_out = cmd.stderr.read().decode("utf-8")

	if error_out:
		system(f"rm {program}")

		print(error_out)
		print("Unpacking error! Exiting...")
		exit()
else:
	tests_dirr = TESTS_PATH

inputs, outputs = get_inputs_and_outputs(tests_dirr)

# Define the trigger to running ####################################################################
if mode == MULTIPLE:
	trigger = ["make", "run"]
elif mode == UNIC:
	trigger = [f"./{program}", ""]

# Run and generates outputs ########################################################################
my_outs = list()
valgrind_outs = list()
for inp in inputs:
	my_out = f"{inp[:-3]}.myout"
	stdin = open(inp, "rb").read()

	cmd_run = subprocess.Popen([trigger[0], trigger[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, error_out = cmd_run.communicate(stdin)

	if error_out:
		system(f"rm -rf {program} tests/")

		print(error_out.decode())
		print("Execution error! Exiting...")
		exit()

	open(my_out, "wb").write(out)
	my_outs.append(f"{my_out}")

# Check outputs and get errors #####################################################################
all_errors = dict()
n_cases, n_corrects = 0, 0

title = " Coference "
print(stylizes_str(f"\n{title:-^77}", style=S.strong))
for out, my_out in zip(outputs, my_outs):
	correct, file_errors = is_correct(out, my_out)
	n_cases += 1

	if correct:
		result = f"Case {str(n_cases).zfill(2)} is correct!"
		print(f"{result:^77}")

		n_corrects += 1
	else:
		result = f"Case {str(n_cases).zfill(2)} is incorrect!"
		print(f"{result:^77}")

		all_errors[n_cases] = file_errors

init = '>' * 27
end = '<' * 27
emoji = define_emoji(n_corrects, n_cases)
print(f"\n{init} {str(n_corrects).zfill(2)}/{str(n_cases).zfill(2)} correct outputs {end}")
print(f"{emoji:^86}\n")

# Print errors if ther are #########################################################################
if len(all_errors): print_errors(all_errors)

# Valgrind memory coference ########################################################################
print_mem_check = input("\nWould you like to test your program with valgrind?(y/n) ").lower()

while print_mem_check != "y" and print_mem_check != "yes" and print_mem_check != "n" and print_mem_check != "no":
	print_mem_check = input("Invalid option, try again... ").lower()

print_mem_check = True if print_mem_check[0] == "y" else False

if print_mem_check:
	title = " Memory Check "
	print(stylizes_str(f"\n{title:-^77}", style=S.strong))
	for i, inp in enumerate(inputs):
		case_name = f"Case {i+1} "
		print(stylizes_str(f"{case_name:-<77}", style=S.strong))

		stdin = open(inp, "rb").read()
		cmd_valgrind = subprocess.Popen(["valgrind", "--leak-check=full", "--show-leak-kinds=all", "--track-origins=yes", f"./{program}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, valgrind_out = cmd_valgrind.communicate(stdin)
		print(valgrind_out.decode())

# Clean files ######################################################################################
system(f"rm -f {program}")

if TESTS_PATH[-4:] == ".zip":
	system(f"rm -rf tests/")

print(stylizes_str("Byee ヾ(￣▽￣)", style=S.strong))