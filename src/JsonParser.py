# parser json files even if they are incomplete and therefore have invalid syntax
# note that this will not always return the maximum amount of data possible but might cut off some data at the end
import re
import json


def parse_json(json_str, throw_error=True):
    json_str = json_str.replace("```json\n", "")
    json_str = json_str.replace("```", "").strip()
    if json_str == "":
        return {}
    try:
        obj = json.loads(json_str)
    except json.JSONDecodeError:
        if throw_error:
            raise RuntimeError(
                "Coudn't parse json returned by chat gpt\n\nJson:\n" + json_str
            )
        else:
            return None
    return obj


def parse_incomplete_json(json_data):
    stack = []
    json_data = json_data.strip()

    parsed_json = parse_json(json_data, throw_error=False)
    if parsed_json is not None:
        return parsed_json

    for i, c in enumerate(json_data):
        if c in ["{", "["]:
            stack.append(c)
        elif c == "}":
            if len(stack) == 0:
                raise Exception("Too many closing brackets at char {}".format(i))
            if stack[-1] == "{":
                stack.pop()
            else:
                raise Exception("Mismatched brackets at char {}".format(i))
        elif c == "]":
            if len(stack) == 0:
                raise Exception("Too many closing brackets at char {}".format(i))
            if stack[-1] == "[":
                stack.pop()
            else:
                raise Exception("Mismatched brackets at char {}".format(i))

    if len(stack) != 0:
        suffix = ""

        for elem in reversed(stack):
            complete_dict = {"{": "}", "[": "]"}
            suffix += complete_dict[elem]

        # cut to last , { or [
        regex = r".*[,{\[]"  # dot matches newline

        while True:
            trimmed_json_data = re.match(regex, json_data, re.DOTALL).group()

            if trimmed_json_data[-1] == ",":
                trimmed_json_data = trimmed_json_data[:-1]

            result = parse_json(json_data + suffix, throw_error=False)
            if result is not None:
                return result

            if trimmed_json_data == json_data:
                raise Exception("Could not parse json")

            json_data = trimmed_json_data
