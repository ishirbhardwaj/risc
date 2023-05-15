isa_desc = {
    "add": {"type": "A", "bin": "00000"},
    "sub": {"type": "A", "bin": "00001"},
    "mov": {"type": "bogus", "bin": "bogus"},
    # "mov": {"type": "B", "bin": "00010"},
    # "mov": {"type": "C", "bin": "00011"},
    "ld": {"type": "D", "bin": "00100"},
    "st": {"type": "D", "bin": "00101"},
    "mul": {"type": "A", "bin": "00110"},
    "div": {"type": "C", "bin": "00111"},
    "rs": {"type": "B", "bin": "01000"},
    "ls": {"type": "B", "bin": "01001"},
    "xor": {"type": "A", "bin": "01010"},
    "or": {"type": "A", "bin": "01011"},
    "and": {"type": "A", "bin": "01101"},
    "not": {"type": "C", "bin": "01101"},
    "cmp": {"type": "C", "bin": "01110"},
    "jmp": {"type": "E", "bin": "01111"},
    "jlt": {"type": "E", "bin": "11100"},
    "jgt": {"type": "E", "bin": "11101"},
    "je": {"type": "E", "bin": "11111"},
    "hlt": {"type": "F", "bin": "11010"},
}

reg_desc = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    # "FLAGS": "111",
}

new_line_count = 0
instructions = []
final_binary = []
errors = []
variables = {}
labels = {}
var = False
var_count = 0
line_count = 0
label_count = 0

with open("input.txt", "r") as f:
    d = f.read()
    temp = ""
    for i in range(len(d)):
        temp += d[i]
        if d[i] == ":":
            temp += "\n"
            new_line_count += 1

with open("temporary.txt", "w") as f:
    f.write(temp)


def binary(x):
    val = bin(x)[2:]
    return f"{((7 - len(val)) * '0')}{val}"


try:
    with open("temporary.txt", "r") as f:
        data = f.readlines()
        for i in data:
            i = i.strip().split()
            if len(i) > 0:
                instructions.append(i)
    for i in range(len(instructions)):
        instruction = instructions[i][0]
        if instruction[-1] == ":" and instruction[-2] != " ":
            labels[instruction[:-1]] = binary(label_count)
        elif instruction != "var":
            label_count += 1
    if len(instructions) > 0 and len(instructions) <= 127:
        if (
            instructions[-1][0] == "hlt"
            and len(instructions[-1]) == 1
            and instructions.count(["hlt"]) == 1
        ):
            for i in instructions:
                instruction = i[0]
                if instruction in isa_desc:
                    line_count += 1
                    var = True
                    var_count = len(instructions) - len(variables) - new_line_count
                    if line_count > 0:
                        for j in variables:
                            variables[j] = binary(var_count)
                            var_count += 1
                    type_instruction = isa_desc[instruction]["type"]
                    bin_instruction = isa_desc[instruction]["bin"]
                    instruction_binary = ""
                    if instruction == "mov":
                        if len(i) == 3:
                            if i[2][0] != "$":
                                type_instruction = "C"
                                bin_instruction = "00011"
                                if i[2] == "FLAGS":
                                    reg_desc["FLAGS"] = "111"
                            else:
                                type_instruction = "B"
                                bin_instruction = "00010"
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    if "A" in type_instruction:
                        if len(i) == 4:
                            reg_1 = i[1]
                            reg_2 = i[2]
                            reg_3 = i[3]
                            if (
                                reg_1 in reg_desc
                                and reg_2 in reg_desc
                                and reg_3 in reg_desc
                            ):
                                instruction_binary = f"{bin_instruction}00{reg_desc[reg_1]}{reg_desc[reg_2]}{reg_desc[reg_3]}"
                            else:
                                errors.append(
                                    f"ERROR Line {line_count}: Invalid register."
                                )
                                break
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    elif "B" in type_instruction:
                        if len(i) == 3:
                            reg_1 = i[1]
                            immediate_val = i[2]
                            if immediate_val[1:].isdigit():
                                immediate_val = int(immediate_val[1:])
                                if immediate_val >= 0 and immediate_val <= 127:
                                    immediate_val = binary(immediate_val)
                                    if reg_1 in reg_desc:
                                        instruction_binary = f"{bin_instruction}0{reg_desc[reg_1]}{immediate_val}"
                                    else:
                                        errors.append(
                                            f"ERROR Line {line_count}: Invalid register."
                                        )
                                        break
                                else:
                                    errors.append(
                                        f"ERROR Line {line_count}: Immediate value out of range."
                                    )
                                    break
                            else:
                                errors.append(
                                    f"ERROR Line {line_count}: Invalid immediate value."
                                )
                                break
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    elif "C" in type_instruction:
                        if len(i) == 3:
                            reg_1 = i[1]
                            reg_2 = i[2]
                            if reg_1 in reg_desc and reg_2 in reg_desc:
                                if reg_1 != "FLAGS":
                                    instruction_binary = f"{bin_instruction}00000{reg_desc[reg_1]}{reg_desc[reg_2]}"
                                else:
                                    errors.append(
                                        f"ERROR Line {line_count}: Illegal use of FLAGS."
                                    )
                                    break
                            else:
                                errors.append(
                                    f"ERROR Line {line_count}: Invalid register."
                                )
                                break
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    elif "D" in type_instruction:
                        if len(i) == 3:
                            reg_1 = i[1]
                            mem_address = i[2]
                            if mem_address in variables:
                                if reg_1 in reg_desc:
                                    instruction_binary = f"{bin_instruction}0{reg_desc[reg_1]}{variables[mem_address]}"
                                else:
                                    errors.append(
                                        f"ERROR Line {line_count}: Invalid register."
                                    )
                                    break
                            elif mem_address in labels:
                                errors.append(
                                    f"ERROR Line {line_count}: Illegal use of label as variable"
                                )
                                break
                            else:
                                errors.append(
                                    f"ERROR Line {line_count}: Undefined variable."
                                )
                                break
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    elif "E" in type_instruction:
                        if len(i) == 2:
                            mem_address = i[1]
                            if mem_address in labels:
                                instruction_binary = (
                                    f"{bin_instruction}0000{labels[mem_address]}"
                                )
                            elif mem_address in variables:
                                errors.append(
                                    f"ERROR Line {line_count}: Illegal use of variable as label."
                                )
                                break
                            else:
                                errors.append(
                                    f"ERROR Line {line_count}: Undefined label."
                                )
                                break
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    elif "F" in type_instruction:
                        if len(i) == 1:
                            instruction_binary = f"{bin_instruction}00000000000"
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    final_binary.append(instruction_binary)
                elif instruction == "var":
                    if not var:
                        if len(i) == 2:
                            variables[i[1]] = 0
                        else:
                            errors.append(
                                f"ERROR Line {line_count}: Invalid length of argument."
                            )
                            break
                    else:
                        errors.append(
                            f"ERROR Line {line_count}: Variable not declared in the beginning."
                        )
                        break
                elif instruction[-1] == ":" and instruction[-2] != " ":
                    pass
                else:
                    errors.append(f"ERROR Line {line_count}: Invalid statement.")
                    break
                if "FLAGS" in reg_desc:
                    reg_desc.pop("FLAGS")
        else:
            errors.append(
                f"ERROR Line {line_count}: hlt not being used once as the last instruction."
            )
    else:
        errors.append(f"ERROR Line {line_count}: Invalid length of instructions.")
except:
    errors.append(f"ERROR Line {line_count}: General Syntax Error.")

with open("errors.txt", "w") as f:
    for i in errors:
        if len(i) != 0:
            print(i)
            f.write(i + "\n")

if len(errors) == 0:
    with open("output.txt", "w") as f:
        for i in final_binary:
            if len(i) != 0:
                print(i)
                f.write(i + "\n")
