#!/usr/bin/python3
# Python Script by Guilherme Rios(Bio) - 2020

import subprocess
import os
import shutil
from sys import argv

class S: # Style flags
    NONE      = ";0"
    STRONG    = ";1"
    BLUR      = ";2"
    ITALIC    = ";3"
    UNDERLINE = ";4"
    FLASH     = ";6"
    NEGATIVE  = ";7"
    STRIKE    = ";9"

class C: # Color flags
    NONE   = ";50"
    BLACK  = ";30"
    RED    = ";31"
    GREEN  = ";32"
    YELLOW = ";33"
    BLUE   = ";34"
    PURPLE = ";35"
    CYAN   = ";36"
    WHITE  = ";37"

def stylize_str(string, color=C.NONE, style=S.NONE):
    start = "\033[0{}{}m".format(style, color)
    end   = "\033[m"

    stylized_str = f"{start}{string}{end}"

    return stylized_str

SHELL_CLEAR = lambda: os.system('clear')

def wait_next_step(wait_msg):
    input(wait_msg)
    SHELL_CLEAR()
    print(stylize_str(" RC SIM ".center(LINE_LEN, "-"), style=S.STRONG), end="\n\n")

LOG_FILENAME  = "rcSim.log"

TESTS_DIRNAME = "rcSimTestes"
FILES_DIRNAME = "rcSimArquivos"
OUTS_DIRNAME  = "rcSimSaidas"

TAB          = " " * 4
LINE_LEN     = 80
ARROW        = stylize_str("╰-> ", style=S.STRONG)
DIV_BAR      = stylize_str("-" * LINE_LEN, style=S.STRONG)
CASES_P_LINE = 12

GCC_FLAGS      = ["-g", "-Wall", "-Werror", "-lm"]
VALGRIND_FLAGS = "--leak-check=full --show-leak-kinds=all --track-origins=yes"
VALGRIND_SUCCESS_MSGS = {
    "leaks" : "All heap blocks were freed -- no leaks are possible",
    "errors": "ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)"
}

def read_lines(filename, mode="r"):
    if not os.path.exists(filename): return list()

    with open(filename, mode) as f:
        lines = f.readlines()
        f.close()

    return lines

def read_file(filename, mode="r"):
    if not os.path.exists(filename): return str()

    with open(filename, mode) as f:
        data = f.read()
        f.close()

    return data

def write_file(filename, data, mode="w+"):
    with open(filename, mode) as f:
        f.write(data)
        f.close()

class Out_Error:
    def __init__(self, missing_ls=None, surplus_ls=None, diff_ls=None) -> None:
        self.missings  = missing_ls if missing_ls else dict()
        self.surpluses = surplus_ls if surplus_ls else dict()
        self.diffs     = diff_ls    if diff_ls    else dict()

    def __bool__(self):
        return True if self.missings or self.surpluses or self.diffs else False

    def __repr__(self) -> str:
        return str(self.diffs) + str(self.missings) + str(self.surpluses)

def check_and_get_cmd_arguments():
    if len(argv) < 3:
        print("Rode com argumentos válidos!")
        print("$ rcsim <caminhoDoPrograma> <caminhoDosTestes> <caminhoDosArquivos(opcional)>")
        exit()

    program_path = f"./{argv[1]}"
    tests_path   = f"./{argv[2]}"

    program_path_is_valid =  (program_path.endswith(".c") or program_path.endswith("Makefile"))
    program_path_is_valid &= os.path.exists(program_path)
    if not program_path_is_valid:
        print("Rode com um caminho válido para o programa!")
        print("$ rcsim <caminhoDoPrograma> <caminhoDosTestes> <caminhoDosArquivos(opcional)>")
        print("<caminhoDosTestes> = arquivo .c ou Makefile, existente")
        exit()

    tests_path_is_valid =  (os.path.isdir(tests_path) or tests_path.endswith(".zip"))
    tests_path_is_valid &= os.path.exists(tests_path)
    if not tests_path_is_valid:
        print("Rode com um caminho válido para os casos testes.")
        print("$ rcsim <caminhoDoPrograma> <caminhoDosTestes> <caminhoDosArquivos(opcional)>")
        print("<caminhoDosTestes> = arquivo .zip ou pasta, existente, com as entradas/saídas a serem testadas")
        exit()

    if len(argv) < 4: return program_path.rstrip("/"), tests_path.rstrip("/"), ""

    files_path = f"./{argv[3]}"

    files_path_is_valid =  (os.path.isdir(files_path) or files_path.endswith(".zip"))
    files_path_is_valid &= os.path.exists(files_path)
    if not files_path_is_valid:
        print("Rode com um caminho válido para os arquivos.")
        print("$ rcsim <caminhoDoPrograma> <caminhoParaTestes> <caminhoParaArquivos(opcional)>")
        print("<caminhoParaArquivos> = arquivo .zip ou pasta, existente, com os arquivos necessários para execução do programa")
        exit()

    return program_path.rstrip("/"), tests_path.rstrip("/"), files_path.rstrip("/")

def gen_compile_cmd(program_path):
    return ["gcc", program_path, "-o", program_path.rstrip(".c")] + GCC_FLAGS

def clean_objets_files(path):
    os.system(f"rm -f {path}*.o {path}*.gch")

def get_program_name(program_dir):
    files = list(map(lambda f: f"{program_dir}/{f}", os.listdir(program_dir)))
    files.sort(key=os.path.getmtime, reverse=True)

    return files[0]

def clean_files_from_path(tests_dir, filter_func):
    files = list(filter(filter_func, os.listdir(tests_dir)))
    [os.remove(f) for f in map(lambda f: f"{tests_dir}/{f}", files)]

def get_inputs_and_outputs(tests_dir):
    ins = list(filter(lambda f: f.endswith(".in"), os.listdir(tests_dir)))

    cmp = lambda s1: int(s1.rstrip(".in"))
    ins.sort(key=cmp)
    ins = list(map(lambda f: f"{tests_dir}/{f}", ins))

    outs = [f.replace(".in", ".out") for f in ins]

    return ins, outs

def update_files_to_run(dest_path, files):
    os.system(f"cp -f {' '.join(files)} {dest_path}")

def compare_files(out_file, my_file):
    exp_out = list(map(str.rstrip, read_lines(out_file)))
    my_out  = list(map(str.rstrip, read_lines(my_file)))

    if exp_out == my_out: return None

    exp_out_len = len(exp_out)
    my_out_len  = len(my_out)

    min_out_len = min(exp_out_len, my_out_len)
    over_lines  = {
        "missing": {
            i: stylize_str(f" > | {l} |", C.GREEN) for i, l in enumerate(exp_out[min_out_len:], start=min_out_len+1)
        },
        "surplus": {
            i: stylize_str(f" < | {l} |", C.RED) for i, l in enumerate(my_out[min_out_len:], start=min_out_len+1)
        }
    }

    errors   = Out_Error(over_lines["missing"], over_lines["surplus"])
    iterable = enumerate(zip(exp_out[:min_out_len], my_out[:min_out_len]), start=1)
    for idx, (exp_line, my_line) in iterable:
        if exp_line == my_line: continue

        exp_line_len = len(exp_line)
        my_line_len  = len(my_line)

        min_line_len = min(exp_line_len, my_line_len)

        error_lines = {
            "exp": stylize_str(" > |", C.GREEN),
            "my" : stylize_str(" < |", C.RED)
        }
        for exp_char, my_char in zip(exp_line[:min_line_len], my_line[:min_line_len]):
            if exp_char == my_char:
                error_lines["exp"] += exp_char
                error_lines["my"]  += my_char
            else:
                error_lines["exp"] += stylize_str(exp_char, C.GREEN)
                error_lines["my"]  += stylize_str(my_char, C.RED)

        error_lines["exp"] += stylize_str(exp_line[min_line_len:]+"|", C.GREEN)
        error_lines["my"]  += stylize_str(my_line[min_line_len:]+"|", C.RED)

        errors.diffs[idx] = error_lines

    return errors

def define_emoji(amt_corrects, amt_cases):
    if amt_corrects == amt_cases:
        emoji = "(o°◡°)o☆"
    elif amt_corrects > (3/4) * amt_cases:
        emoji = "o(*￣◡￣*)o"
    elif amt_corrects > (2/4) * amt_cases:
        emoji = "^____^"
    elif amt_corrects > (1/4) * amt_cases:
        emoji = "(┬┬﹏┬┬)"
    else:
        emoji = "(╯°□°）╯︵ ┻━┻"

    return stylize_str(emoji, style=S.STRONG)

def compile_and_get_bin_program(program_path, exists_makefile):
    print(stylize_str(" COMPILAÇÃO ".center(LINE_LEN, "="), style=S.STRONG))

    [os.remove(f) for f in filter(os.path.exists, map(str.rstrip, read_lines(LOG_FILENAME, "r")))]

    if exists_makefile:
        compile_type = "Makefile"
        cmd = ["make", "all"]
    else:
        compile_type = ".c"
        cmd = gen_compile_cmd(program_path)

    run = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    error_out = run.stderr.readlines()

    if error_out:
        print(f"{TAB}> Erro na compilação com {compile_type}:")
        os.system(" ".join(cmd))
        print(f"\n\n{TAB}Ajeita ae e roda de novo, encerrando rcSim ... :(")
        exit()

    program_dir = os.path.dirname(program_path)
    clean_objets_files(program_dir)
    bin_program = get_program_name(program_dir)

    print(f"{TAB}> Programa compilado com sucesso!\n\n")
    return bin_program

def setup_tests(tests_path, files_path):
    print(stylize_str(" ORGANIZAÇÃO DOS TESTES ".center(LINE_LEN, "="), style=S.STRONG))

    tests_dir = f"{os.path.dirname(tests_path)}/{TESTS_DIRNAME}"
    if tests_path.endswith(".zip"):
        tests_type = ".zip"
        cmd = ["unzip", "-qqo", tests_path, "-d", tests_dir]

        run = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        error_out = run.stderr.readlines()

        if error_out:
            print(f"{TAB}> Erro ao organizar testes com {tests_type}:")
            os.system(" ".join(cmd))
            print(f"\n\n{TAB}Ajeita ae e roda de novo, encerrando rcSim ... :(")
            exit()
    elif os.path.isdir(tests_path):
        tests_type = "pasta"

        if os.path.exists(tests_dir): shutil.rmtree(tests_dir)
        shutil.copytree(tests_path, tests_dir)

    clean_files_from_path(tests_dir, lambda f: not (f.endswith(".in") or f.endswith(".out")))
    inputs, outputs = get_inputs_and_outputs(tests_dir)

    print(f"{TAB}> Casos de testes organizados com sucesso!\n")

    if not files_path: return inputs, outputs, list()

    files_dir = f"{os.path.dirname(files_path)}/{FILES_DIRNAME}"
    if files_path.endswith(".zip"):
        tests_type = ".zip"
        cmd = ["unzip", "-qqo", files_path, "-d", files_dir]

        run = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        error_out = run.stderr.readlines()

        if error_out:
            print(f"{TAB}> Erro ao organizar arquivos com {tests_type}:")
            os.system(" ".join(cmd))
            print(f"\n\n{TAB}Ajeita ae e roda de novo, encerrando rcSim ... :(")
            exit()
    elif os.path.isdir(files_path):
        tests_type = "pasta"

        if os.path.exists(files_dir): shutil.rmtree(files_dir)
        shutil.copytree(files_path, files_dir)

    clean_files_from_path(files_dir, lambda f: f.endswith(".in") or f.endswith(".out"))
    files = list(map(lambda f: f"{files_dir}/{f}", os.listdir(files_dir)))

    print(f"{TAB}> Arquivos para execução organizados com sucesso!\n")

    return inputs, outputs, files

def run_and_generation_outputs(bin_program, exists_makefile, inputs, files):
    print(stylize_str(" EXECUÇÃO DOS TESTES ".center(LINE_LEN, "="), style=S.STRONG))

    cmd = "make run <" if exists_makefile else f"./{bin_program} <"

    my_outs    = list()
    run_errors = list()

    my_outs_dir = f"{os.path.dirname(bin_program)}/{OUTS_DIRNAME}"
    if os.path.exists(my_outs_dir): shutil.rmtree(my_outs_dir)
    os.mkdir(my_outs_dir)

    for inp in inputs:
        if files: update_files_to_run(os.path.dirname(bin_program), files)

        run = subprocess.Popen(cmd + inp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error_out = run.communicate()

        if error_out:
            print(f"{TAB}> Erro de execução para o teste {os.path.basename(inp).rjust(5, '0')}:")
            os.system(" ".join(cmd))
            print(error_out.decode())
            run_errors.append(inp.rstrip(".in"))
        else:
            print(f"{TAB}> Caso {os.path.basename(inp).rjust(5, '0')} executado com sucesso!")

            my_out_filename = f"{my_outs_dir}/{os.path.basename(inp).replace('.in', '.myout')}"
            write_file(my_out_filename, out, "wb+")
            my_outs.append(my_out_filename)
    print()

    return my_outs, run_errors

def check_outputs(exp_outs, my_outs):
    print(stylize_str(" CHECAGEM DAS SAÍDAS ".center(LINE_LEN, "="), style=S.STRONG))

    all_errors = dict()
    amt_corrects = 0
    for exp_out, my_out in zip(exp_outs, my_outs):
        cur_errors = compare_files(exp_out, my_out)

        if cur_errors:
            result = "incorreta [x]"
            all_errors[os.path.basename(exp_out).rstrip('.out')] = cur_errors
        else:
            result = "correta   [✔]"
            amt_corrects += 1

        print(f"{TAB}> Saída para caso {os.path.basename(exp_out).rstrip('.out').rjust(2, '0')} está {result}")

    amt_cases = len(exp_outs)
    emoji = define_emoji(amt_corrects, amt_cases)
    print(f"\n{TAB}[ {amt_corrects:02d}/{amt_cases:02d} ] saídas corretas {emoji}", end="\n\n")

    return all_errors

def gen_line_error_str(line_data):
    title    = f"{TAB}{ARROW}linha {line_data[0]}:"
    exp_line = f"{TAB}{line_data[1]['exp']}"
    my_line  = f"{TAB}{line_data[1]['my']}"

    return "\n".join([title, exp_line, my_line])

def print_errors(all_errors):
    print(stylize_str(" DETALHES DAS DIFERENÇAS ".center(LINE_LEN, "="), style=S.STRONG))

    wrong_cases = list(all_errors.keys())
    wrong_print = [wrong_cases[i:i+CASES_P_LINE] for i in range(0, len(wrong_cases), CASES_P_LINE)]
    wrong_print = ["  ".join(map(lambda s: f"[{s.rjust(2, '0')}]", l)) for l in wrong_print]

    input_msg   = [
        "Escolha um dos casos abaixo para ver a diferença ou pressione \"s\" para sair:",
        "\n".join(wrong_print),
        "> "
    ]

    user_choice = input("\n".join(input_msg)).lower().lstrip("0")
    while user_choice not in set(wrong_cases + ["s"]):
        user_choice = input("Opção inválida, tente novamente ... ").lower().lstrip("0")

    while user_choice != "s":
        SHELL_CLEAR()
        print(stylize_str(" RC SIM ".center(LINE_LEN, "-"), style=S.STRONG), end="\n\n")
        print(stylize_str(" DETALHES DAS DIFERENÇAS ".center(LINE_LEN, "="), style=S.STRONG))

        case_errors = all_errors[user_choice]
        print(f"{TAB}{stylize_str(f'Caso {user_choice}:', style=S.STRONG)}")

        print("\n".join(map(gen_line_error_str, case_errors.diffs.items())))

        uncommon_lines = dict()
        if case_errors.missings:
            type_uncommon  = "faltante"
            uncommon_lines = case_errors.missings
        elif case_errors.surpluses:
            type_uncommon  = "excedente"
            uncommon_lines = case_errors.surpluses

        keys = list(uncommon_lines.keys())
        if len(keys) == 1:
            print(f"{TAB}{ARROW}linha {type_uncommon} [{keys[0]}]:")
            print("\n".join(map(lambda s: f"{TAB}{s}", uncommon_lines.values())))
        elif len(keys) > 1:
            print(f"{TAB}{ARROW}linhas {type_uncommon}s [{keys[0]} - {keys[-1]}]:")
            print("\n".join(map(lambda s: f"{TAB}{s}", uncommon_lines.values())))

        print(DIV_BAR, end="\n\n")

        wait_next_step("\nPressione enter para voltar à escolha de caso ... ")
        print(stylize_str(" DETALHES DAS DIFERENÇAS ".center(LINE_LEN, "="), style=S.STRONG))
        user_choice = input("\n".join(input_msg)).lower().lstrip("0")
        while user_choice not in set(wrong_cases + ["s"]):
            user_choice = input("Opção inválida, tente novamente ... ").lower().lstrip("0")

def run_valgrind(inputs, bin_program, files):
    user_choice = input("\nGostaria de checar uso de memória com valgrind? (s/n) ").lower()
    while not (user_choice.startswith("s") or user_choice.startswith("n")):
        if not user_choice: break
        user_choice = input("Opção inválida, tente novamente ... (s/n) ").lower()
    if user_choice.startswith("n"): return

    SHELL_CLEAR()
    print(stylize_str(" RC SIM ".center(LINE_LEN, "-"), style=S.STRONG), end="\n\n")
    print(stylize_str(" CHECAGEM COM VALGRIND ".center(LINE_LEN, "="), style=S.STRONG))

    cmd = f"valgrind ./{bin_program} {VALGRIND_FLAGS} <"

    error_valgrind_outs = dict()
    amt_without_errors  = 0
    for inp in inputs:
        if files: update_files_to_run(os.path.dirname(bin_program), files)

        run = subprocess.Popen(cmd + inp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        valgrind_out = run.communicate()[1].decode()

        possible_mem_errors = {
            "erros": (VALGRIND_SUCCESS_MSGS["errors"] not in valgrind_out),
            "leaks": (VALGRIND_SUCCESS_MSGS["leaks"]  not in valgrind_out)
        }

        case = os.path.basename(inp).rstrip('.in').rjust(2, "0")
        if True in possible_mem_errors.values():
            result = ["com erros no uso de memória [✖] (ocorreram "]

            possible_mem_errors = dict(filter(lambda e: e[1] == True, possible_mem_errors.items()))
            result.append(" e ".join(map(str.strip, possible_mem_errors.keys())))
            result.append(")")

            error_valgrind_outs[case.lstrip("0")] = valgrind_out
        else:
            amt_without_errors += 1
            result = ["sem erros no uso de memória [✔]"]

        print(f"{TAB}> Caso {case} {''.join(result)}")

    amt_cases = len(inputs)
    emoji = define_emoji(amt_without_errors, amt_cases)
    print(f"\n{TAB}[ {amt_without_errors:02d}/{amt_cases:02d} ] saídas corretas {emoji}", end="\n\n")

    if not error_valgrind_outs: return

    wait_next_step("\nPressione enter para ir para detalhes sobre os erros ... ")
    print(stylize_str(" CHECAGEM COM VALGRIND ".center(LINE_LEN, "="), style=S.STRONG))

    wrong_cases = list(error_valgrind_outs.keys())
    wrong_print = [wrong_cases[i:i+CASES_P_LINE] for i in range(0, len(wrong_cases), CASES_P_LINE)]
    wrong_print = ["  ".join(map(lambda s: f"[{s.rjust(2, '0')}]", l)) for l in wrong_print]

    input_msg   = [
        "Escolha um dos casos abaixo para ver o erro ou pressione \"s\" para sair:",
        "\n".join(wrong_print),
        "> "
    ]

    user_choice = input("\n".join(input_msg)).lower().lstrip("0")
    while user_choice not in set(wrong_cases + ["s"]):
        user_choice = input("Opção inválida, tente novamente ... ").lower().lstrip("0")

    while user_choice != "s":
        SHELL_CLEAR()
        print(stylize_str(" RC SIM ".center(LINE_LEN, "-"), style=S.STRONG), end="\n\n")
        print(stylize_str(" CHECAGEM COM VALGRIND ".center(LINE_LEN, "="), style=S.STRONG))
        print(stylize_str(f" Caso {user_choice} ".center(LINE_LEN, "-"), style=S.STRONG))
        print(f"{TAB}{stylize_str(f'Caso {user_choice}:', style=S.STRONG)}")

        print(error_valgrind_outs[user_choice])

        print(DIV_BAR, end="\n\n")

        wait_next_step("\nPressione enter para voltar à escolha de caso ... ")
        print(stylize_str(" DETALHES DAS DIFERENÇAS ".center(LINE_LEN, "="), style=S.STRONG))
        user_choice = input("\n".join(input_msg)).lower().lstrip("0")
        while user_choice not in set(wrong_cases + ["s"]):
            user_choice = input("Opção inválida, tente novamente ... ").lower().lstrip("0")

def main():
    print(stylize_str(" RC SIM ".center(LINE_LEN, "-"), style=S.STRONG), end="\n\n")

    program_path, tests_path, files_path = check_and_get_cmd_arguments()
    exists_makefile = (program_path.endswith("Makefile"))

    wait_next_step("Pressione enter para iniciar a compilação ... ")
    bin_program = compile_and_get_bin_program(program_path, exists_makefile)

    wait_next_step("Pressione enter para iniciar a organização dos testes ... ")
    inputs, outputs, files = setup_tests(tests_path, files_path)

    wait_next_step("Pressione enter para iniciar a execução dos casos ... ")
    my_outputs, run_errors = run_and_generation_outputs(bin_program, exists_makefile, inputs, files)

    if run_errors:
        error_cases = ", ".join(run_errors)
        print(f"\nCorrija os erros dos casos {error_cases} e depois rode novamente")
        return

    wait_next_step("Pressione enter para iniciar a checagem das saídas ... ")
    out_errors = check_outputs(outputs, my_outputs)
    if out_errors: 
        wait_next_step("Pressione enter para ir para detalhes das diferenças ... ")
        print_errors(out_errors)

    run_valgrind(inputs, bin_program, files)
    os.remove(bin_program)

if __name__ == "__main__":
    SHELL_CLEAR()
    main()
    print(stylize_str("\n\nEncerrando rcSim ... flwww \(°◡°)\n", style=S.STRONG))
