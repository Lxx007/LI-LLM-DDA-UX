from HumanEvaluator_Dice import DataCleaning as DC
from HumanEvaluator_Dice import ScoringSystem as Score

def ranking_sys():
    Log_File_Name = "Dice_Fighting.txt"
    directory_to_search = "./Project_DiceLLM/HumanEvaluator_Dice/PlayerData"
    full_data = DC.find_files(directory_to_search, Log_File_Name)
    Results = DC.data_intergration(full_data)
    Fun_Score, Challenge_Score, Relaxation_Score = Score.Score(Results)

    Fun_above_Avg = [i for i, value in enumerate(Fun_Score) if value > sum(Fun_Score)/len(Fun_Score)]
    Challenge_above_Avg = [i for i, value in enumerate(Challenge_Score) if value > sum(Challenge_Score)/len(Challenge_Score)]
    Relaxation_above_Avg = [i for i, value in enumerate(Relaxation_Score) if value > sum(Relaxation_Score)/len(Relaxation_Score)]

    Order_Fun = sorted(range(len(Fun_Score)), key=lambda x: Fun_Score[x], reverse=True)
    Order_Challenge = sorted(range(len(Challenge_Score)), key=lambda x: Challenge_Score[x], reverse=True)
    Order_Relaxation = sorted(range(len(Relaxation_Score)), key=lambda x: Relaxation_Score[x], reverse=True)
    return Fun_above_Avg, Challenge_above_Avg, Relaxation_above_Avg, Order_Fun, Order_Challenge, Order_Relaxation, Fun_Score, Challenge_Score, Relaxation_Score