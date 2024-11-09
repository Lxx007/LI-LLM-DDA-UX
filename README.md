# LI-LLM-DDA-UX
This is the supplementary file for the paper “Personalized Game Difficulty with Large Language Models: A Preliminary Study.”

Our experiment flow:
<img src="https://github.com/Lxx007/LI-LLM-DDA-UX/blob/main/Flow.png" width="1000" />

# SourceCode
This folder contains all of our source code, prompts, and raw data for the questionnaire. 
Please note:
1. The source code uses the API of GPT-4o. Please prepare your own API key if you need to use our code to access the OpenAI API.
2. The default relative position (commented) has been set in the code; please adjust it yourself if needed.
3. Python version >= 3.10
# SourceCode/Project_DiceLLM
This folder contains two subfolders and three Python scripts. 
Additionally, all prompts (Play Prompt, Classifying Prompt, and Rating Prompt) are included here.
# Fold "GameSimulationDetail"
This folder contains all the data we generated using GPT-4o.
# Fold "HumanEvaluator_Dice"
1. This folder contains a subfolder called “PlayerData,” which includes all players’ responses to our questionnaire (Game Log).
2. TThis folder contains four Python scripts:
A. DataCleaning.py – Extracting questionnaire data from game logs
B. Dice_Project.py – Main script for our rating and classification algorithm
C. Plays.py – 11 representative data sets
D. ScoringSystem.py – Scoring algorithm and our detailed game group settings
# DicePlayGeneration.py
This script pertains to stage 1 of our paper.
# RepresentativeSelection.py
This script is used for representative play selection in stage 2 of our work.
# DiceClassification.py
This script pertains to stage 3 of our paper.
