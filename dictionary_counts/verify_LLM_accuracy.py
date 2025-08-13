import json

#may need to change file name which our double checked values are saved into
OUTPUT_FILE_NAME = "hierarchical_gemini.json"

#lines with these phrases will be the only lines displayed, also the lines will be displayed one by one, not all at a time, so it is easier to manually double check
detect_phrases = ["Gemini classification:"]

with open(r"google doc file.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
lines = [line.strip().lower() for line in lines]

with open(r"ground_truths.txt", 'r', encoding='utf-8') as file:
    ground_truths = file.readlines()
ground_truths = [ground_truth.strip().lower() for ground_truth in ground_truths]

#i think these are the ones missing the fallacy example statements, so skip these
ground_truths.remove("methodology")
ground_truths.remove("reasoning")

ground_truth_idx = 0
accuracy_dict = {}
for ground_truth in ground_truths:
    accuracy_dict[ground_truth] = 0

tot_correct = 0

for line in lines:
    for phrase in detect_phrases:
        if phrase.lower() in line:
            print(ground_truths[ground_truth_idx])
            truth = input(line)
            if truth == '1':
                tot_correct += 1
                accuracy_dict[ground_truths[ground_truth_idx]] = 1
            ground_truth_idx += 1
        
#do sanity check to make sure no big errors
print(tot_correct)

with open(OUTPUT_FILE_NAME, 'w') as file:
    json.dump(accuracy_dict, file, indent=1)
