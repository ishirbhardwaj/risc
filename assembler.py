isa_desc = {
    "add": {"type": "A", "bin": "00000"},
    "sub": {"type": "A", "bin": "00001"},
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

instructions = []
variables = []
labels = []
var = False


def binary(x):
    x = x[::-1]
    val = 0
    for i in range(len(x)):
        val = int(x[i]) * (2**i)
    return f"{(8 - len(str(val)) * 0)}{val}"


try:
    with open("assembly.txt", "r") as f:
        data = f.readlines()
        for i in data:
            instructions.append(i.strip().split())

    if len(instructions) > 0:
        if instructions[-1][0] == "hlt" and len(instructions[-1]) == 1:
            for i in instructions:
                if len(i) > 0:
                    instruction = i[0]
                    if instruction in isa_desc:
                        var = True
                        type_instruction = isa_desc[instruction]["type"]
                        bin_instruction = isa_desc[instruction]["bin"]
                        instruction_binary = ""
                        if instruction == "mov":
                            if len(i) == 3:
                                if i[2][0] != "$":
                                    type_instruction = "B"
                                    bin_instruction = "00010"
                                else:
                                    type_instruction = "C"
                                    bin_instruction = "00011"
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
                                    print("Invalid register.")
                        elif "B" in type_instruction:
                            if len(i) == 3:
                                reg_1 = i[1]
                                immediate_val = i[2]
                                if immediate_val[1:].isdigit():
                                    immediate_val = int(immediate_val[1:])
                                    if immediate_val >= 0 and immediate_val <= 127:
                                        immediate_val = binary(immediate_val[1:])
                                        if reg_1 in reg_desc:
                                            instruction_binary = f"{bin_instruction}0{reg_desc[reg_1]}{immediate_val}"
                                        else:
                                            print("Invalid register.")
                                    else:
                                        print("Immediate value out of range.")
                                else:
                                    print("Invalid immediate value.")
                        elif "C" in type_instruction:
                            if len(i) == 3:
                                reg_1 = i[1]
                                reg_2 = i[2]
                                if reg_1 in reg_desc and reg_2 in reg_desc:
                                    instruction_binary = f"{bin_instruction}00000{reg_desc[reg_1]}{reg_desc[reg_2]}"
                                else:
                                    print("Invalid register.")
                        elif "D" in type_instruction:
                            if len(i) == 3:
                                reg_1 = i[1]
                                mem_address = i[2]
                                if mem_address in variables:
                                    if reg_1 in reg_desc:
                                        instruction_binary = f"{bin_instruction}0{reg_desc[reg_1]}{mem_address}"
                                    else:
                                        print("Invalid register.")
                                elif mem_address in labels:
                                    print("Illegal use of label as variable")
                                else:
                                    print("Undefined variable.")
                        elif "E" in type_instruction:
                            if len(i) == 2:
                                if mem_address in labels:
                                    instruction_binary = (
                                        f"{bin_instruction}0000{mem_address}"
                                    )
                                elif mem_address in variables:
                                    print("Illegal use of variable as label.")
                                else:
                                    print("Undefined label.")
                        elif "F" in type_instruction:
                            if len(i) == 1:
                                instruction_binary = f"{bin_instruction}00000000000"
                    elif instruction == "var":
                        if not var:
                            if len(i) == 2:
                                variables.append(i[1])
                        else:
                            print("Variable not declared in the beginning.")
                    elif instruction[-1] == ":" and instruction[-2] != " ":
                        if len(i) == 1:
                            labels.append(instruction)
                    else:
                        print("Invalid statement.")
        else:
            print("hlt not being used as the last instruction.")
except:
    print("Error encountered.")
