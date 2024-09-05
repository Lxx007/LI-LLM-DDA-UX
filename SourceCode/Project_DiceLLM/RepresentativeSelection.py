import os
import csv
import copy
import numpy as np
from scipy.spatial.distance import pdist, squareform

# detail infor dir
# directory_path = "./Project_DiceLLM/GameSimulationDetail"
# Your Dir
directory_path = ""

files = os.listdir(directory_path)

# initialization
Detail_Pure_Random = []
Detail_Easy = []
Detail_Hard = []
Detail_Interesting = []
Detail_No_Goal = []
Detail_No_Goal_CoT = []
Detail_Win_0 = []
Detail_Win_25 = []
Detail_Win_50 = []
Detail_Win_75 = []
Detail_Win_100 = []

game_detail = []

# read dir
def csv_reader (dir, data_container):
    with open(dir, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data_container.append([str(i) for i in row])

# get all pattens data
for file in files:
    game_detail_information_dir = directory_path + "/" + str(file) + "/detail.csv"
    if str(file) == 'Feel Easy':
        csv_reader (game_detail_information_dir, Detail_Easy)
    elif str(file) == 'Feel Hard':
        csv_reader (game_detail_information_dir, Detail_Hard)
    elif str(file) == 'Feel Interesting':
        csv_reader (game_detail_information_dir, Detail_Interesting)
    elif str(file) == 'NoGoal':
        csv_reader (game_detail_information_dir, Detail_No_Goal)
    elif str(file) == 'NoGoalCoT':
        csv_reader (game_detail_information_dir, Detail_No_Goal_CoT)
    elif str(file) == 'PureRandom':
        csv_reader (game_detail_information_dir, Detail_Pure_Random)
    elif str(file) == 'Win0':
        csv_reader (game_detail_information_dir, Detail_Win_0)
    elif str(file) == 'Win25':
        csv_reader (game_detail_information_dir, Detail_Win_25)
    elif str(file) == 'Win50':
        csv_reader (game_detail_information_dir, Detail_Win_50)
    elif str(file) == 'Win75':
        csv_reader (game_detail_information_dir, Detail_Win_75)
    elif str(file) == 'Win100':
        csv_reader (game_detail_information_dir, Detail_Win_100)
    else:
        print("Unexpected Folder")

# All data
All_game_log = Detail_Pure_Random + Detail_Easy + Detail_Hard + Detail_Interesting + Detail_No_Goal + Detail_No_Goal_CoT + Detail_Win_0 + Detail_Win_25 + Detail_Win_50 + Detail_Win_75 + Detail_Win_100

# algorithm for padding
def flatten_then_padding(data):
    game_detail = []
    longest_list = max(data, key = len)
    # shortest_list = min(data, key = len)
    max_length = len(longest_list)
    for i in range(0, len(data), 3):
        if i + 1 < len(data):
            data[i].extend([0] * abs(max_length - len(data[i])))
            data[i + 1].extend([0] * abs(max_length - len(data[i + 1])))
            flatten_data = data[i] + data[i + 1]
            flatten_data = [int(i) for i in flatten_data]
            game_detail.append(copy.deepcopy(flatten_data))
    return game_detail

# data_processing
def data_processing(data , min_length = 2):
    game_detail = []
    for i in range(0, len(data), 3):
        if i + 1 < len(data):
            # flatten_data = data[i] + data[i + 1]
            flatten_data = [item for sublist in zip(data[i], data[i + 1]) for item in sublist]
            flatten_data = [int(i) for i in flatten_data]
            game_detail.append(copy.deepcopy(flatten_data))
    longest_list = max(game_detail, key = len)
    max_length = len(longest_list)
    for i_j in game_detail:
        i_j.extend([0] * abs(max_length - len(i_j)))
    game_detail = np.array(game_detail)
    return game_detail #result,


shortest_list = min(All_game_log, key = len)
min_length = len(shortest_list)
game_detail = data_processing(All_game_log, min_length)

game_detail_11 = game_detail.reshape(11, 100, 38)

# algorithm to get the top k points for the mini-sum-distance
def k_top_distance_matrix(data, top_k):
    distances = pdist(data, 'euclidean')
    dist_matrix = squareform(distances)
    average_distances = np.mean(dist_matrix, axis=1)
    indices = np.argpartition(average_distances, top_k)[:top_k]
    indices = indices[np.argsort(average_distances[indices])]
    return indices

Data_Top_K = []

color_R = 0
for data_i in game_detail_11:
    index_of_top = k_top_distance_matrix(data_i, 3)
    index_of_top = list(index_of_top)
    index_of_top = [i + (color_R * 100) for i in index_of_top]
    Data_Top_K.append(copy.deepcopy(index_of_top))

Representative_List = []
Top_1_Orginal = np.array(Data_Top_K)[:,0].tolist()
for represtation_i in Top_1_Orginal:
    R_new = [i for i in game_detail.tolist()[represtation_i] if i != 0]
    n = len(R_new)
    R_new_star = [R_new[i] for i in range(0, n, 2)] + [R_new[i] for i in range(1, n, 2)]
    Representative_List.append(copy.deepcopy(R_new_star))

# 写入CSV文件
#with open('../DiceResult/RepresentativeDice.csv', 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerows(Representative_List)