import re


def extract_function_name(string):
    # Define a regular expression pattern to match the function name
    pattern = r"def\s+(\w+)\s*\(.*\)"

    # Use re.match() to search for the pattern in the string
    match = re.match(pattern, string)

    # If a match is found, return the function name
    if match:
        return match.group(1)
    else:
        return None


def replace_function_name(string, replacement_string):
    # Define the regular expression pattern to match the function name
    pattern = r"def\s+(\w+)\s*"

    # Use re.sub() to replace the pattern with the replacement string
    modified_string = re.sub(pattern, "def " + replacement_string, string)

    return modified_string


# made according to mixtral response
def get_code_from_response(response):
    lines = response.split("\n")
    code = ""
    in_code = False
    for i, line in enumerate(lines):
        if line.startswith("```python"):
            in_code = True
        elif line.startswith("```"):
            in_code = False
            return code
        elif in_code == True:
            if i == len(lines) - 1:
                return code
            code += line + "\n"
    # incomplete output, most likely incomplete assertion.
    # ignore this last assertion and move with the rest

    return code


# replaces the unittest call with another one to fix exec problem with running on colab
def replaceUnitTestCall(code):
    pattern = r"unittest.main()"

    # Use re.sub() to replace the pattern with the replacement string
    modified_code = re.sub(
        pattern, "unittest.main(argv=['first-arg-is-ignored'])", code
    )

    return modified_code


def get_feedback_from_run(response):
    lines = response.split("\n")
    feedback = ""
    in_failmessage = False
    for i, line in enumerate(lines):
        if line.startswith("FAIL"):
            in_failmessage = True
            feedback += line + "\n"
        elif line.startswith("--"):
            if lines[i + 1].startswith("Ran"):
                return feedback

        elif in_failmessage == True:
            if line.startswith("=="):
                continue
            if i == len(lines) - 1:
                return feedback
            feedback += line + "\n"