import json

#stepwise + relational graphs requires different code to check for second-best classifications, set this to true
#if double checking stepwise + relational graphs
stepwise_relational = True

#file name which our double chec=ked values are saved into
OUTPUT_FILE_NAME = "relational_graphs_gemini.json"

#lines with these phrases will be 
detect_phrases = ["Gemini with KB + Prolog:"]

with open(r"google doc file.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
lines = [line.strip().lower() for line in lines]

with open(r"ground_truths.txt", 'r', encoding='utf-8') as file:
    ground_truths = file.readlines()
ground_truths = [ground_truth.strip().lower() for ground_truth in ground_truths]

#i think these are the ones missing the fallacy example statemtns, so skip these
ground_truths.remove("methodology")
ground_truths.remove("reasoning")

ground_truth_idx = 0
accuracy_dict = {}
if stepwise_relational:
    second_best_dict = {}
for ground_truth in ground_truths:
    accuracy_dict[ground_truth] = 0
    if stepwise_relational:
        second_best_dict[ground_truth] = 0

tot_correct = 0

for line in lines:
    for phrase in detect_phrases:
        if phrase.lower() in line:
            print(ground_truths[ground_truth_idx])
            truth = input(line)
            if truth == '1':
                tot_correct += 1
                accuracy_dict[ground_truths[ground_truth_idx]] = 1
            if truth == '3' and stepwise_relational:
                second_best_dict[ground_truths[ground_truth_idx]] = 1
            ground_truth_idx += 1
        
#do sanity check to make sure no big errors
print(tot_correct)

if stepwise_relational:
    accuracy_dict = [accuracy_dict, second_best_dict]
with open(OUTPUT_FILE_NAME, 'w') as file:
    json.dump(accuracy_dict, file, indent=1)
