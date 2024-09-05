import os
import csv
import re
import copy

def data_extraction (lines):
    single_data = []
    for i in range (len(lines)):
        if i == 0:
            pattern = r"Group (\d+)"
            matches = re.findall(pattern, lines[i])
            single_data.append(copy.deepcopy(int(matches[0])))
        else:
            pattern = r"\((\d+,\d+,\d+,\d+)\)"
            matches = re.findall(pattern, lines[i])
            result = [list(map(int, match.split(','))) for match in matches]
            single_data.append(copy.deepcopy(result))
    return single_data

def data_finding(file_path):
    Log_key_word = "LogBlueprintUserMessages"
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    matching_lines = [line for line in lines if Log_key_word in line]
    return data_extraction(matching_lines)

def find_files(directory, file_name):
    data = []
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            userful_information = data_finding(file_path)
            data.append(copy.deepcopy(userful_information))
    return data

def data_intergration(full_data):
    All_Group_0 = [item for item in full_data if item[0] == 0]
    All_Group_1 = [item for item in full_data if item[0] == 1]
    All_Group_2 = [item for item in full_data if item[0] == 2]
    All_Group_3 = [item for item in full_data if item[0] == 3]
    All_Group_4 = [item for item in full_data if item[0] == 4]

    data_reorg = [All_Group_0, All_Group_1, All_Group_2, All_Group_3, All_Group_4]
    Final_Result = []
    for k in data_reorg:
        Group_number = k[0][0]
        result = [Group_number] + [[[] for _ in range(len(k[0][i]))] for i in range(1, len(k[0]))]

        for sublist in k:
            for i in range(1, len(sublist)):
                for j in range(len(sublist[i])):
                    # If the inner list is not empty, sum the corresponding elements
                    if result[i][j]:
                        result[i][j] = [x + y for x, y in zip(result[i][j], sublist[i][j])]
                    else:
                        result[i][j] = sublist[i][j]
        Final_Result.append(copy.deepcopy(result))
    return Final_Result