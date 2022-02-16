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
            elif title_number+1 > len(table_names):
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
        output_file.write(str(i.strip()+"\n"))
    output_file.close()

    os.chdir(cwd)


def atmos(planet_template):
    # This will run the atmos climate model shell bash script "Runmodels.sh"
    # method: use subprocess to run bash in a specific child directory
    subprocess.run([f"{cwd}/atmos/RunModels.sh", planet_template, "y", "y", "n", "n"],
                   shell=True, cwd=f"{cwd}/atmos")
    # Might work differently on different shell environments


def generateData(data):
    # Use timegan to do deeplearning task of generating new data instances

    parameters = dict()

    parameters['module'] = 'gru'
    parameters['hidden_dim'] = 50
    parameters['num_layer'] = 5
    parameters['iterations'] = 1000
    parameters['batch_size'] = 30
    print("Parameters: ", parameters)
    # generate data
    generated_data = timegan(data, parameters)

    return generated_data
