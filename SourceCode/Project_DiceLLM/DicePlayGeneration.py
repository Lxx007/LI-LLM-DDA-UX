import random
import re
import time
import os
import copy
import openai
import csv
from openai import OpenAI
from dotenv import load_dotenv
import statistics

# from transformers import Conversation
import openai

# set your api key
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-4o'
OPENAI_RATE_LIMIT = 0.6
openai.api_key = API_KEY
# TEMPERATURE = 0


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

# system prompt to give an overall setting
gm_setting = """You are the game master in a game scenario. 
In this scenario, you will manipulate the opponent's dice. 
A player will roll a die. 
By comparing the result of the player's dice with the result of your dice, the difference between the two will cause the same amount of damage to the side with the lower value. 
Each side starts with 10 health points. As soon as one side's health reaches 0, the side with 0 health loses the game.
The dice number only ranges from 1 to 6 with 6 int numbers.
"""

# Initialization
history=[]
Player_win_rate = []
Game_Result = []
Rounds = []
Player_Dice_Sum = []
AI_Dice_Sum = []
WinnerLife = []
std_player = []
std_AI = []
R_Time = []

All_Dice_Player = []
All_Dice_AI = []
GameDetail = []
mode = "LLM"
purpose_line = ""
player_dice = random.randint(1, 6)

# data generation
for i in range (100):
    print("*******************Round " + str(i+1) + "************************")
    player_life = 10
    enemy_life = 10
    play_time = 0
    player_win = 0
    Player_Dice_All = 0
    AI_Dice_All = 0
    history = []
    Total_Responing_Time = 0
    while player_life >0 and enemy_life> 0:     
        play_time = play_time + 1
        if mode == "LLM":
            print("History is:")
            print(history)
            player_dice = random.randint(1, 6)
            Player_Dice_All = Player_Dice_All + player_dice
            print("Player Dice is: " + str(player_dice))
           
            prompt = f"The player's combat history is as follows: {history}. Current player health point is: {player_life}. Current enemy health point is: {enemy_life}. Current player dice roll is: {player_dice}. Please avoid showing the same dice as the player rolled: {player_dice}. {purpose_line} Give the value of the dice you want to show, with format /opponent_dice:"
           
            while (True): 
                while (True):
                    start_time = time.time()
                    # result = run_function_with_timeout(get_chat_response(gm_setting,prompt), 10)
                    while time.time() - start_time < 10:
                        result = get_chat_response(gm_setting,prompt)[0]
                        if result is not None:
                            break

                    # result = get_chat_response(gm_setting,prompt)[0]
                    try:
                        result_num = re.search(r'opponent_dice.*?(\d+)', result).group(1)
                    except Exception:
                        continue
                    # result_num = re.findall(r'\d+', result)
                    if len(result_num) == 1:
                        if 0 <= int(result_num[0]) <= 6:
                            break
                        else:
                            continue
                    else:
                        continue

                result_value = result_num[0]
                result_value = int(result_value)
                if int(result_value) != int(player_dice):
                    break
            print(str(result))
            print("LLM Dice is: " + str(result_num))
            
        elif mode == "Random":
            while (True):
                start_time = time.time()
                player_dice = random.randint(1, 6)
                Player_Dice_All = Player_Dice_All + player_dice
                result_value = random.randint(1, 6)
                if int(result_value) != int(player_dice):
                    break

        All_Dice_Player.append(copy.deepcopy(player_dice))
        All_Dice_AI.append(copy.deepcopy(result_value))   

        AI_Dice_All = AI_Dice_All + result_value

        damage = abs(player_dice - result_value)

        if(player_dice < result_value):
            player_life = player_life - damage
            history.append("lose")
        elif(player_dice > result_value):
            enemy_life = enemy_life - damage
            player_win = player_win + 1
            history.append("win")

        winrate = player_win/play_time
        print ("Player Win Rate = " + str(winrate))


        # Update history
        current_turn=[player_dice,result_value]
        print("player life:",player_life)
        print('enemy life:',enemy_life)
        end_time = time.time()
        total_time = end_time - start_time
        print('Responing Time:',total_time)
        Total_Responing_Time = Total_Responing_Time + total_time
        print('--------------------------------------------------------------------------')
        rate_limit_sleeper()

    def adjust_values(player_life, enemy_life):
        if player_life < 0:
            player_life = 0
        if enemy_life < 0:
            enemy_life = 0
        return player_life, enemy_life

    R_Time.append(copy.deepcopy(Total_Responing_Time))
    Player_win_rate.append(copy.deepcopy(winrate))
    Rounds.append(copy.deepcopy(play_time))
    Player_Dice_Sum.append(copy.deepcopy(Player_Dice_All))
    AI_Dice_Sum.append(copy.deepcopy(AI_Dice_All))
    player_life, enemy_life = adjust_values(player_life, enemy_life)
    WinnerLife.append(copy.deepcopy(abs(player_life-enemy_life)))
    if player_life>0:
        print("Player Win")
        Game_Result.append(copy.deepcopy("True"))
    else:
        print("LLM Win")
        Game_Result.append(copy.deepcopy("False"))


    std_player.append(copy.deepcopy(statistics.stdev(All_Dice_Player)))
    std_AI.append(copy.deepcopy(statistics.stdev(All_Dice_AI)))
    GameDetail.append(copy.deepcopy(All_Dice_Player))
    GameDetail.append(copy.deepcopy(All_Dice_AI))
    GameDetail.append(copy.deepcopy(history))
    All_Dice_Player = []
    All_Dice_AI = []
    history = []

Result = [Player_win_rate, Game_Result, WinnerLife, Rounds, R_Time, Player_Dice_Sum, std_player, AI_Dice_Sum, std_AI]