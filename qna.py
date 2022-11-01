import util

def question_evaluator(eval):
    """
    Only adds correct_selected flag to the evaluator output
    """

    all_options  = []

    all_options.append(util.fuzzy_dict_simplifier(eval.correct_answer_matches_summary, option = 0))
    all_options.extend([util.fuzzy_dict_simplifier(l, option = i + 1) for i, l in enumerate(eval.distractors_matches_summary)])
    

    winner_picked, match_type, option = evaluator(all_options)

    if winner_picked and option == 0:
        correct_selected = True
    else:
        correct_selected = False

    return [correct_selected, winner_picked, match_type, option] 


def evaluator(all_options):
    """
    winner_picked = False -> match_type = no_matches / all_equivalent / draw, option = -1
    winner_picked = True -> match_type = triple / double / single, option = 0/1/2/3

    returns winner_picked, match_type, option

    if the winner decided based on triples -> match_type = triple etc
    """

    # delete all empty matches
    for d in all_options:
        del(d["none"])

    # winner_picked = False, match_type = no_matches, option = -1
    temp_set = set(list(all_options[0].values())[:3] + list(all_options[1].values())[:3] 
                 + list(all_options[2].values())[:3] + list(all_options[3].values())[:3])

    if temp_set == set([0]):
        return [False, "no_matches", -1]

    # winner_picked = False, match_type = draw, option = -1
    if util.compare_matches(all_options[0], all_options[1]) and util.compare_matches(all_options[1], all_options[2]) and util.compare_matches(all_options[2], all_options[3]):
        return [False, "all_equivalent", -1]

    # sort with multiple keys
    # at the end, check if the first place unique
    
    all_options = sorted(all_options, key=lambda d: (d["triple"], d["double"], d["single"]), reverse=True)

    if util.compare_matches(all_options[0], all_options[1]): 
        return [False, "draw", -1]

    # first place unique, check what decided the result
    
    for match_type in ["triple", "double", "single"]:
        if all_options[0][match_type] != all_options[1][match_type]:
            return [True, match_type, all_options[0]["option"]]



