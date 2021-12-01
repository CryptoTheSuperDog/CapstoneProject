import os
import re
import sys

import numpy as np
from typing import TextIO
import subprocess
sys.path.insert(1, "C:/Users/Administrator/timegan")
sys.path.insert(2, "C:/Users/Administrator/atmos")
sys.path.insert(3, "C:/Users/Administrator/timegan/metrics")
from timegan import timegan
from metrics import discriminative_metrics
from predictive_metrics import predictive_score_metrics
from visualization_metrics import visualization
from data_loading import MinMaxScaler


def takeData(title_number, file, table_names, out_filename="Data.txt"):  # file out.out has most of the info wanted
    # go through output file and read out the data we need to a specific file
    # method: find file_line of title, find file_line of next title. Write data between two points to new file
    os.chdir("C:/Users/Administrator/atmos/photochem/output")

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
                print("Start is: ", table_names[title_number])
            elif title_number+1 > len(table_names):
                end_line = len(file_content)
                end_taken = True
            elif caps[0] == table_names[title_number + 1] and not end_taken:
                end_line = count
                end_taken = True
                print("End is: ", table_names[title_number+1])
            else:
                continue
        except KeyError:
            print("The Key you entered was not found...")
            break

    for j in range(title_line - 1, end_line - 1):
        data.append(file_content[j])
    file_open.close()

    output_file: TextIO = open(f"C:/Users/Administrator/PycharmProjects/Trappist_Climate_Code/{out_filename}", "w")
    for i in data:
        output_file.write(str(i.strip()+"\n"))
    output_file.close()

    os.chdir("C:/Users/Administrator/PycharmProjects/Trappist_Climate_Code")


def atmos(planet_template):
    # This will run the atmos climate model shell bash script "Runmodels.sh"
    # method: use subprocess to run bash in a specific child directory
    subprocess.run(["C:/Users/Administrator/atmos/RunModels.sh", planet_template, "y", "y", "n", "n"],
                   shell=True, cwd="C:/Users/Administrator/atmos")


def generateData(data):
    # Use timegan to do deeplearning task of generating new data instances
    os.chdir("C:/Users/Administrator/timegan")
    no, dim, seq_len = 10000, 5, 24

    # flip data to make chronological data
    ori_data = data[::-1]
    # normalize data
    ori_data = MinMaxScaler(ori_data)

    temporary = []
    # cut data by sequence length
    for i in range(0, len(ori_data) - seq_len):
        _x = ori_data[i:i + seq_len]
        temporary.append(_x)

    # mix datasets (to make it similar to i.i.d)
    idx = np.random.permutation(len(temporary))
    pre_processed = []
    for i in range(len(temporary)):
        pre_processed.append(temporary[idx[i]])

    parameters = dict()

    parameters['module'] = 'gru'
    parameters['hidden_dim'] = 24
    parameters['num_layer'] = 3
    parameters['iterations'] = 10000
    parameters['batch_size'] = 128

    # generate data
    generated_data = timegan(pre_processed, parameters)
    return generated_data
