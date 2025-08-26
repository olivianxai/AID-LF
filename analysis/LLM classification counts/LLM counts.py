import json
import os

#do organize data if organizing data into readable 1 file, do get data if getting data for 1 indiv LLM count
mode = "organize data"

if mode=="get data":
    with open(r"C:\Users\xiaol\OneDrive\Documents\VS_code\Fallacies API calls\google doc file.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip().lower() for line in lines]

    with open(r"C:\Users\xiaol\OneDrive\Documents\VS_code\Fallacies API calls\ground_truths.txt", 'r', encoding='utf-8') as file:
        ground_truths = file.readlines()
    ground_truths = [ground_truth.strip().lower() for ground_truth in ground_truths]

    #set up dictionaries to keep count of fallacy classifications/
    fallacy_classification_count = {}
    secondary_fallacy_classification_count = {}
    for ground_truth in ground_truths:
        fallacy_classification_count[ground_truth] = 0
        secondary_fallacy_classification_count[ground_truth] = 0

    for idx, line in enumerate(lines):
        #what phrases to detect? Input here
        detect_phrases = ["Gemini with KB + Prolog:"]
        for phrase in detect_phrases:
            #only add counts for phrases in detect_phrases and if the LLM has not hallucinated a no classification or no fallacy/
            if (phrase.lower() in line) and ("Nonexistent fallacy".lower() not in line) and ("No Classification".lower() not in line):
                #check 4 spell error
                exists = False
                for ground_truth in ground_truths:
                    if ground_truth in line:
                        exists = True         
                assert exists == True, f"fix spelling on line {idx + 1}"

                #count fallacy classifications for LLM biases
                for ground_truth in ground_truths:
                    if ground_truth in line:
                        fallacy_classification_count[ground_truth] += 1
                if "inconsistency ->" in line and not "inconsistency (" in line:
                    fallacy_classification_count["inconsistency"] -= 1

    #sort the dictionary for more visibility, but gonna use code to count anyways, this just for sanity check
    sorted_fallacy_classification_count = dict(sorted(fallacy_classification_count.items(), key=lambda item: item[1], reverse=True))

    with open("LLM bias counts/Instruction-Guided Classification with Relational Graphs Gemini.json", 'w') as file:
        json.dump(sorted_fallacy_classification_count, file, indent=1)

elif mode=="organize data":
    dicts = {"Claude" : [], "GPT" : [], "Gemini" : []}
    folders = os.listdir("LLM bias counts")
    for folder in folders:
        files = os.listdir(f"LLM bias counts/{folder}")
        for file in files:
            with open(f"LLM bias counts/{folder}/{file}", 'r') as file:
                dicts[folder].append(json.load(file))

    #remember that dicts is a dictionary with keys of LLM names, and values of dictionaries
    total_dict = {"Claude" : {}, "GPT" : {}, "Gemini" : {}}
    p_kv_pairs = dicts.items()
    for pkey, pvalue in p_kv_pairs:
        for dicti in pvalue:
            kv_pairs = dicti.items()
            for key, value in kv_pairs:
                total_dict[pkey][key] = 0
    for pkey, pvalue in p_kv_pairs:
        for dicti in pvalue:
            kv_pairs = dicti.items()
            for key, value in kv_pairs:
                total_dict[pkey][key] += value 

    for key, value in total_dict.items():
        total_dict[key] = dict(sorted(value.items(), key=lambda item: item[1], reverse=True))         

    with open("LLM bias counts/total bias counts.json", 'w') as file:
        json.dump(total_dict, file, indent=1)
