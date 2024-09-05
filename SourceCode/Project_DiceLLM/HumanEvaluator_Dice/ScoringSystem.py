def Score (Results):
    # 内置游戏组别
    Game_Group_D0 = [0, 
                     [7,10],
                     [5,10],
                     [4,9],
                     [3,8],
                     [2,6],
                     [1,11],
                     [9,10],
                     [7,8],
                     [5,6],
                     [3,4],
                     [1,2]]
    Game_Group_D1 = [1, 
                     [7,11],
                     [5,11],
                     [4,6],
                     [3,10],
                     [2,8],
                     [1,9],
                     [6,10],
                     [6,8],
                     [5,7],
                     [2,4],
                     [1,3]]
    Game_Group_D2 = [2, 
                     [5,9],
                     [8,11],
                     [4,10],
                     [3,9],
                     [1,7],
                     [2,9],
                     [10,11],
                     [6,7],
                     [5,8],
                     [2,3],
                     [1,4],]
    Game_Group_D3 = [3, 
                     [4,11],
                     [7,9],
                     [6,9],
                     [3,11],
                     [2,11],
                     [1,10],
                     [8,9],
                     [4,7],
                     [3,6],
                     [2,5],
                     [1,5]]
    Game_Group_D4 = [4, 
                     [8,10],
                     [9,11],
                     [6,11],
                     [4,5],
                     [3,7],
                     [2,10],
                     [1,8],
                     [4,8],
                     [3,5],
                     [2,7],
                     [1,6]]
    Game_Setting = [Game_Group_D0, Game_Group_D1, Game_Group_D2, Game_Group_D3, Game_Group_D4]
    # 按照组别得出每个数据的得分（三个得分）
    Scoring = [[1,0],[0,1],[0.5,0.5],[0,0]]
    Fun_Score = [0] * 11
    Challenge_Score = [0] * 11
    Relaxation_Score = [0] * 11

    # Iterate through the sets in G
    for group in (Game_Setting):
        for sets in range (1, len(group)):
            paired_sets = group[sets]
            Sets_Result = Results[group[0]][sets]
            for result_detail in range (len(Sets_Result)):
                if result_detail == 0:
                    for compare_result in range (len(Sets_Result[result_detail])):
                        Fun_Score[paired_sets[0] - 1] = Fun_Score[paired_sets[0] - 1] + Scoring[compare_result][0] * Sets_Result[result_detail][compare_result]
                        Fun_Score[paired_sets[1] - 1] = Fun_Score[paired_sets[1] - 1] + Scoring[compare_result][1] * Sets_Result[result_detail][compare_result]
                elif result_detail == 1:
                    for compare_result in range (len(Sets_Result[result_detail])):
                        Challenge_Score[paired_sets[0] - 1] = Challenge_Score[paired_sets[0] - 1] + Scoring[compare_result][0] * Sets_Result[result_detail][compare_result]
                        Challenge_Score[paired_sets[1] - 1] = Challenge_Score[paired_sets[1] - 1] + Scoring[compare_result][1] * Sets_Result[result_detail][compare_result]
                elif result_detail == 2:
                    for compare_result in range (len(Sets_Result[result_detail])):
                        Relaxation_Score[paired_sets[0] - 1] = Relaxation_Score[paired_sets[0] - 1] + Scoring[compare_result][0] * Sets_Result[result_detail][compare_result]
                        Relaxation_Score[paired_sets[1] - 1] = Relaxation_Score[paired_sets[1] - 1] + Scoring[compare_result][1] * Sets_Result[result_detail][compare_result]
    return Fun_Score, Challenge_Score, Relaxation_Score