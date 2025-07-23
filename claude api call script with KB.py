import json

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="",
)

def load_fallacy_kb():
    lst = []
    with open('final_instructions.json', 'r') as file:
        lines = file.readlines()
        for line in lines:
            lst.append(json.loads(line.strip()))
    return lst 
    
def get_claude_response(prompt):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.content[0].text


# Define the Fallacy Manager agent (controller)
def construct_prompt(statement, fallacy):
    for name, steps, ground_truth, operations in fallacy:
        name = fallacy["name"]
        steps = fallacy["steps"]
        ground_truth = fallacy["ground_truth"]
        operations = fallacy["operations"]
        prompt = f"""Statement: "{statement}"
Your task is to determine whether this is an example of the fallacy: {name}.
Follow these steps:
{steps}

and compare each step's result with the ground truth:
{ground_truth}

After the comparison, perform the following operations:
{operations} and return the final result.

Does the statement match this fallacy?
ONLY response in this format - 
*yes or no*
**reasoning for each step:**
DO NOT output anything else 
"""
        
        return prompt

# Example usage
def call_fallacy_checker(statement):
    fallacies = load_fallacy_kb()
    for fallacy in fallacies:
        print(fallacy["name"])
        prompt = construct_prompt(statement, fallacy)
        response = get_claude_response(prompt)
        print(response)
        classification = response.split("*")[1]
        if classification.lower() == "yes":
            return response
    return "no classification"

user_statement = "I believe one should never deliberately hurt another person, that’s why I can never be a surgeon"
result = call_fallacy_checker(user_statement)
print("\nFinal Result:", result)      
            
                                  

