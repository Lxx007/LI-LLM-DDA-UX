# LI-LLM-DDA-UX
This is the supplement files for the paper "LI: The concept of prompt design for a LLM to DDA with a better UX"
# SourceCode
This folder contains all of our source code, prompts, and raw data for the questionnaire.
Please note:
1. The source code uses the API of ChatGPT-4o. please prepare your own API-key when you need to use our code to use OpenAI API.
2. The default relative position (commented) has been set in the code, please adjust it yourself if needed.
3. Python version >= 3.10
# SourceCode/Project_DiceLLM
This folder contains two folds and three Python scripts.
# Fold "GameSimulationDetail"
This folder publicizes all the data we generated using ChatGPT-4
# Fold "HumanEvaluator_Dice"
1. This folder contains one folder called "PlayerData", which publicizes all players' responses to our questionnaire(Game Log).
2. This folder contains four Python scripts.
They are listed as follows:
A. DataCleaning.py -- Extracting questionnaire data from game logs
B. Dice_Project.py -- Main script about our rating and classification
C. Plays.py -- 11 representative data
D. ScoringSystem.py -- Scoring algorithm and our detailed game group settings
# DicePlayGeneration.py
Our paper's stage 1, which contains our prompt 1
# RepresentativeSelection.py
Representative data selection in stage 2 of our work
# DiceClassification.py
Our paper's stage 3, which contains our prompt 2A and 2B
