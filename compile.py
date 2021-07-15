import os
import subprocess

from utils import stylize_str, C, S, TAB, LINE_LEN

class Compiler:
	CC        = ["gcc"]
	GCC_FLAGS = ["-g", "-Wall", "-Werror", "-lm"]
	MAKE      = ["make", "all"]

	def __gen_compile_cmd(self):
		prog_bin = self.prog_path.rstrip(".c")
		cmd = self.CC + [self.prog_path, "-o", prog_bin] + self.C_FLAGS

		return cmd

	def __init__(self, prog_path="./main.c", type=".c"):
		self.prog_path = prog_path
		self.prog_dir  = os.path.dirname(self.prog_path)

		self.type      = type
		self.cmd       = self.__gen_compile_cmd() if type == ".c" else self.MAKE
		self.has_error = False

	def __clean_objets_files(self, dir_path):
		os.system(f"rm -f {dir_path}/*.o {dir_path}/*.gch")

	def __erro(self):
		self.has_error = True

		print(f"{TAB}> Erro na compilação com {self.type}:")
		os.system(" ".join(self.cmd))

	def compile_and_get_bin_program(self):
		print(stylize_str(" COMPILAÇÃO ".center(LINE_LEN, "="), style=S.STRONG))

		run = subprocess.Popen(self.cmd, stderr=subprocess.PIPE)
		error_out = run.stderr.readlines()

		if error_out: self.__erro()

		program_dir = os.path.dirname(self.prog_path)
		self.__clean_objets_files(program_dir)
		bin_program = get_program_name(program_dir)

		print(f"{TAB}> Programa compilado com sucesso!\n\n")
		return bin_program