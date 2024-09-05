import random
import re
import time
import os
import copy
import openai
import csv
from openai import OpenAI
from dotenv import load_dotenv
from HumanEvaluator_Dice.Dice_Project import ranking_sys
from HumanEvaluator_Dice import Plays

# set your api key
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-4o'
openai.api_key = API_KEY

def get_chat_response(gm_setting: str, prompt: str, model=MODEL) :

    #print("Initiated chat with OpenAI API.")
    client = OpenAI()
    start_time = time.perf_counter()
    completion = client.chat.completions.create(model=model,
                                                messages=[
                                                    {"role": "system", "content": gm_setting},
                                                    {"role": "user", "content": prompt}],
                                                temperature = 0)
    #print("Completed chat with OpenAI API.")
    return completion.choices[0].message.content, model

def csv_reader (dir, data_container):
    with open(dir, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data_container.append([str(i) for i in row])

# initialization containers
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

# read generated data
# directory_path = "./Project_DiceLLM/GameSimulationDetail"
# Your dir
directory_path = ""

files = os.listdir(directory_path)
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

# data scoring
All_game_log = Detail_Pure_Random + Detail_Easy + Detail_Hard + Detail_Interesting + Detail_No_Goal + Detail_No_Goal_CoT + Detail_Win_0 + Detail_Win_25 + Detail_Win_50 + Detail_Win_75 + Detail_Win_100
Fun_above_Avg, Challenge_above_Avg, Relaxation_above_Avg, Order_Fun, Order_Challenge, Order_Relaxation, Fun_Score_A, Challenge_Score_A, Relaxation_Score_A = ranking_sys()
Game_Plays = Plays.plays()

# create few shots for prompt 1 and prompt 2A and 2B
few_shot = ""
few_shot_class = ""
for i in range (len(Game_Plays)):
    player_dice_seq = Game_Plays[i][0]
    enemy_dice_seq = Game_Plays[i][1]
    Interesting_Score = Fun_Score_A[i]
    Challenge_Score = Challenge_Score_A[i]
    Relaxation_Score = Relaxation_Score_A[i]
    Samples= f"The details of the Num.{i+1} game are as follows: The player's dice sequence is: {player_dice_seq}. The enemy dice sequence is: {enemy_dice_seq}. The interesting score of this game is: {Interesting_Score}; The challenge score is: {Challenge_Score}; The relaxation score is: {Relaxation_Score}.\n"    
    Sample_Class = f"The details of the Num.{i+1} game are as follows: The player's dice sequence is: {player_dice_seq}. The enemy's dice sequence is: {enemy_dice_seq}."
    if i in Fun_above_Avg:
        Sample_Class = Sample_Class + " The game is interesting;"
    else:
        Sample_Class = Sample_Class + " The game is not interesting;"
    if i in Challenge_above_Avg:
        Sample_Class = Sample_Class + " The game is challenging;"
    else:
        Sample_Class = Sample_Class + " The game is not challenging;"
    if i in Relaxation_above_Avg:
        Sample_Class = Sample_Class + " The game is relaxation.\n"
    else:
        Sample_Class = Sample_Class + " The game is not relaxation.\n"  
    few_shot = few_shot + Samples
    few_shot_class = few_shot_class + Sample_Class

# prompt 1
Few_shot_class = []
gm_setting = "You are a gamer and are watching a game competition. You are asked to classify three aspects of the game, namely, interesting, challenge, and relaxation, based on the examples provided."
for j in range (1100):
    prompt_head = "Please classify current_play as interesting, challenge, and relaxation based on the examples provided, with format /interesting_class:{0: not interesting; 1: interesting}; /challenge_class:{0: not challenging; 1: challenge}; /relaxation_class:{0: not relaxation; 1: relaxation}. Think it step by step.\n"
    cur_player_dice_seq = All_game_log[3*j]
    cur_enemy_dice_seq = All_game_log[3*j + 1]
    prompt_play = f"The details of current_play are as follows: The current player's dice sequence is: {cur_player_dice_seq}. The current enemy's dice sequence is: {cur_enemy_dice_seq}.\n"
    sample_head = "Examples: \n"
    Full_prompt = prompt_head + prompt_play + sample_head + few_shot_class
    print(Full_prompt)
    while (True):
        try:
            result = get_chat_response(gm_setting,Full_prompt)[0]
            print(result)
            interesting_c = re.search(r'interesting_class.*?(\d+)', result).group(1)
            challenge_c = re.search(r'challenge_class.*?(\d+)', result).group(1)
            relaxation_c = re.search(r'relaxation_class.*?(\d+)', result).group(1)
            assess_score = [interesting_c, challenge_c, relaxation_c]
            break
        except Exception:
            continue
    Few_shot_class.append(copy.deepcopy(assess_score))
    print("-------------------------------------------------------------------------------------------------------------------------")

# prompt 2A/2B
Few_shot_Scoring = []
gm_setting = "You are a gamer and are watching a game competition. You are asked to score three aspects of the game, namely, interesting, challenge, and relaxation, based on the examples provided."
for j in range (1100):
    prompt_head = "Please rate current_play as interesting, challenge, and relaxation based on the examples provided, with format /interesting_Score:{interesting}; /challenge_Score:{challenge}; /relaxation_Score:{relaxation}. Think it step by step.\n"
    cur_player_dice_seq = All_game_log[3*j]
    cur_enemy_dice_seq = All_game_log[3*j + 1]
    prompt_play = f"The details of current_play are as follows: The player's dice sequence is: {cur_player_dice_seq}. The enemy dice sequence is: {cur_enemy_dice_seq}.\n"
    sample_head = "Examples: \n"
    Full_prompt = prompt_head + prompt_play + sample_head + few_shot
    print(Full_prompt)
    while (True):
        try:
            result = get_chat_response(gm_setting,Full_prompt)[0]
            print(result)
            interesting_s = re.search(r'interesting_Score.*?(\d+)', result).group(1)
            challenge_s = re.search(r'challenge_Score.*?(\d+)', result).group(1)
            relaxation_s = re.search(r'relaxation_Score.*?(\d+)', result).group(1)
            assess_score = [interesting_s, challenge_s, relaxation_s]
            break
        except Exception:
            continue
    Few_shot_Scoring.append(copy.deepcopy(assess_score))
    print("-------------------------------------------------------------------------------------------------------------------------")

with open('../DiceResult/Fewshot_Class_1st.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(Few_shot_class)