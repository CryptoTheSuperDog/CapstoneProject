import os
import re
from typing import TextIO
import subprocess
from timegan import timegan

cwd = os.getcwd()


def takeData(title_number, file, table_names, out_filename="Data.txt"):  # file out.out has most of the info wanted
    # go through output file and read out the data we need to a specific file
    # method: find file_line of title, find file_line of next title. Write data between two points to new file
    os.chdir(f"{cwd}/atmos/photochem/output/")

    file_open: TextIO = open(file, "r")
    file_content: list = file_open.readlines()
    title_pattern: re.Pattern = re.compile("[A-Z ]+")
    data: list = []
    title_line: int = 0
    end_line: int = 0
    count: int = 0
    title_taken: bool = False
    end_taken: bool = False

    for i in file_content:
        count += 1
        caps: list = title_pattern.findall(i)
        try:
            if not caps:  # Handle blank lines
                continue
            elif caps[0] == table_names[title_number] and not title_taken:
                title_line = count
                title_taken = True
                # print("Start is: ", table_names[title_number])
            elif title_number + 1 > len(table_names):
                end_line = len(file_content)
                end_taken = True
            elif caps[0] == table_names[title_number + 1] and not end_taken:
                end_line = count
                end_taken = True
                # print("End is: ", table_names[title_number+1])
            else:
                continue
        except KeyError:
            print("The Key you entered was not found...")
            break

    for j in range(title_line - 1, end_line - 1):
        data.append(file_content[j])
    file_open.close()

    output_file: TextIO = open(f"{cwd}/{out_filename}", "w")
    for i in data:
        if "E+00-" in i:
            i = i.replace("E+00-", "E+00 -")
        output_file.write(str(i.strip() + "\n"))
    output_file.close()
    os.chdir(cwd)


def atmos(planet_template, arg1="y", arg2="y", arg3="n", arg4="n"):
    # This will run the atmos climate model shell bash script "Runmodels.sh"
    # method: use subprocess to run bash in a specific child directory
    file = open(f"{cwd}/atmos/RunModels.sh", "r+")
    lines = file.readlines()
    # 14, 46, 54, 61, 69
    lines[14] = f"folder={planet_template}\n"
    lines[46] = f" recompile={arg1}\n"
    lines[54] = f"  run_photo={arg2}\n"
    lines[61] = f"recompile={arg3}\n"
    lines[69] = f"run_clima={arg4}\n"
    file.close()
    file = open(f"{cwd}/atmos/RunModels.sh", "r+")
    file.writelines(lines)
    file.close()

    subprocess.run([f"{cwd}/atmos/RunModels.sh"], shell=True, cwd=f"{cwd}/atmos")

    # Might work differently on different shell environments


def generateData(data, module='gru', hidden_dim=50, num_layer=5, iterations=1000, batch_size=30):
    # Use timegan to do deeplearning task of generating new data instances

    parameters = dict()

    parameters['module'] = module
    parameters['hidden_dim'] = hidden_dim
    parameters['num_layer'] = num_layer
    parameters['iterations'] = iterations
    parameters['batch_size'] = batch_size
    print("Parameters: ", parameters)
    # generate data
    generated_data = timegan(data, parameters)

    return generated_data
