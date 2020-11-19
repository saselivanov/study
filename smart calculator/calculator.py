from collections import deque

calc_dict = {"test_a": 10, "test_b": -20}
operators = ["+", "-", "*", "/", "^"]
brackets = ["(", ")"]
precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "(": None, ")": None}


def peek_stack(stack):
    if stack:
        return stack[-1]
    else:
        return None


def slash_checker(string):
    if str(string).startswith("/"):
        return 1
    else:
        return 0


def known_commands(string):
    if string == "/exit":
        return 0
    elif string == "/help":
        print("The program calculates everything")
    else:
        print("Unknown command")


def addition(b, a):
    return a + b


def subtraction(b, a):
    return a - b


def multiplication(b, a):
    return a * b


def division(b, a):
    if a % b == 0:
        return int(a / b)
    else:
        return a / b


def power(b, a):
    return a ^ b


def parse_into_list(string):
    string = string.replace("=", " = ")
    string = string.replace("^", " ^ ")
    string = string.replace("*", " * ")
    string = string.replace("/", " / ")
    string = string.replace("(", " ( ")
    string = string.replace(")", " ) ")
    string = string.replace("+", " + ")
    string = string.replace("-", " - ")
    str_to_list = string.split()
    return str_to_list


def turn_into_digits(lst):
    int_list = []
    for one in lst:
        if one.isdigit():
            one = int(one)
            int_list.append(one)
        elif one.startswith("-") and one[1:].isdigit():
            counter = 0
            counter -= int(one[1:])
            int_list.append(counter)
        elif one.startswith("+") and one[1:].isdigit():
            counter = 0
            counter += int(one[1:])
            int_list.append(counter)
        else:
            int_list.append(one)
    return int_list


def eliminate_dbl_minus(lst):
    for i, sign in enumerate(lst):
        if sign == "+":
            for j, next_sign in enumerate(lst[i + 1:]):
                if next_sign == "+":
                    continue
                else:
                    del lst[i + 1:i + 1 + j]
                    break
        elif sign == "-":
            counter = 1
            for j, next_neg_sign in enumerate(lst[i + 1:]):
                if next_neg_sign == "-":
                    counter += 1
                    continue
                else:
                    del lst[i:i + j]
                    if counter % 2 == 0:
                        lst[i] = "+"
                    else:
                        lst[i] = "-"
                    break
        else:
            continue
    return lst


def str_to_no_dict_list(some_input_string):
    return eliminate_dbl_minus(
        turn_into_digits(
            parse_into_list(some_input_string)
        )
    )


def full_compute_list(some_input_string):
    global calc_dict
    lst = str_to_no_dict_list(some_input_string)
    for i, one in enumerate(lst):
        if i == 0 and one == "-":
            lst[i + 1] = lst[i + 1] * (-1)
            del lst[i]
        if str(one).isalpha() and one in calc_dict:
            lst[i] = calc_dict[one]
    return lst


def print_var_if_exist(string):
    global calc_dict
    if string in calc_dict:
        print(calc_dict[string])
    else:
        print("Unknown variable_from var print")


def assignment(lst):
    global calc_dict
    if len(lst) > 3:
        print("Invalid assignment_from_>3")
        return 0
    elif len(lst) == 1:
        print("Invalid assignment_no_operands")
        return 0
    elif lst[1] != "=":
        print("Invalid assignment_from_no_in_the_middle_equal_sign")
        return 0
    elif not str(lst[0]).isalpha():
        print("Invalid identifier_no_alpha_at_first")
        return 0
    elif not str(lst[2]).isalpha() and not str(lst[2]).isdigit():
        print("Invalid assignment_from_whoat")
        return 0
    elif str(lst[2]).isalpha() and lst[2] not in calc_dict:
        print("Unknown variable_from_not_in_dict")
        return 0
    else:
        if str(lst[2]).isdigit():
            calc_dict[lst[0]] = lst[2]
        elif str(lst[2]).isalpha():
            calc_dict[lst[0]] = calc_dict[lst[2]]


def infix_to_postfix(lst):
    global operators, precedence
    postfix = []
    temp_stack = deque()
    for i, item in enumerate(lst):
        if i == 0:
            if item not in operators and item not in brackets:
                postfix.append(item)
            else:
                temp_stack.append(item)
        else:
            if item not in operators and item not in brackets:
                postfix.append(item)
            elif item == "(":
                temp_stack.append(item)
            elif item == ")":
                while peek_stack(temp_stack) != "(":
                    postfix.append(temp_stack.pop())
                temp_stack.pop()
            elif len(temp_stack) == 0:
                temp_stack.append(item)
            else:
                if peek_stack(temp_stack) == "(" or peek_stack(temp_stack) == ")":
                    temp_stack.append(item)
                elif len(temp_stack) == 0:
                    temp_stack.append(item)
                elif precedence[item] > precedence[peek_stack(temp_stack)]:
                    temp_stack.append(item)
                else:
                    postfix.append(temp_stack.pop())
                    if not temp_stack:
                        while peek_stack(temp_stack) != "(":
                            if not temp_stack:
                                break
                            while precedence[item] <= precedence[peek_stack(temp_stack)]:
                                postfix.append(temp_stack.pop())
                                if not temp_stack:
                                    break
                            break
                    temp_stack.append(item)
    while temp_stack:
        postfix.append(temp_stack.pop())
    return postfix


def calculation(lst):
    calc_stack = deque()

    for el in lst:
        if el in operators:
            if el == "+":
                calc_stack.append(addition(calc_stack.pop(), calc_stack.pop()))
                continue
            elif el == "-":
                calc_stack.append(subtraction(calc_stack.pop(), calc_stack.pop()))
                continue
            elif el == "*":
                calc_stack.append(multiplication(calc_stack.pop(), calc_stack.pop()))
                continue
            elif el == "/":
                calc_stack.append(division(calc_stack.pop(), calc_stack.pop()))
                continue
            elif el == "^":
                calc_stack.append(power(calc_stack.pop(), calc_stack.pop()))
                continue
        calc_stack.append(el)
    if len(calc_stack) > 1:
        return "Invalid expression"
    else:
        return calc_stack[0]


def type_of_operation(string):
    if len(str_to_no_dict_list(string)) == 1 and (list(string)[i].isalpha() for i in enumerate(list(string))):
        return "call var print from dict"
    elif full_compute_list(string).count("=") > 1:
        return "too many equal signs"
    elif full_compute_list(string).count("=") == 1:
        return "assignment"
    else:
        return "calculation!"


def main_menu():
    some_input = input()
    if some_input == "":
        pass
    elif slash_checker(some_input) == 1:
        if known_commands(some_input) == 0:
            return 0
    elif type_of_operation(some_input) == "call var print from dict":
        print_var_if_exist(some_input)
    elif type_of_operation(some_input) == "too many equal signs":
        print("Invalid assignment_from_too_many_equals")
    elif type_of_operation(some_input) == "assignment":
        assignment(str_to_no_dict_list(some_input))
    elif type_of_operation(some_input) == "calculation!":
        try:
            print(calculation(infix_to_postfix(full_compute_list(some_input))))
        except TypeError:
            print("Invalid expression_ TypeError")
        except IndexError:
            print("Invalid expression_ IndexError")


while True:
    if main_menu() == 0:
        print("Bye!")
        break
