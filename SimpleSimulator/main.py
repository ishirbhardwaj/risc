pc = 0
rf = [0, 0, 0, 0, 0, 0, 0, 0]
binary_instructions = []
flag = True

# while True:
#     line = input().strip()
#     if len(line) > 0:
#         binary_instructions.append(line)
#     else:
#         break

while True:
    try:
        line = input().strip()
    except EOFError:
        break
    if len(line) > 0:
        binary_instructions.append(line)


for i in range(128 - len(binary_instructions)):
    binary_instructions.append(16 * "0")


def var_length_binary(x, n):
    x = bin(int(x))[2:]
    return f"{(n - len(x)) * '0'}{x}"


def decimal(x):
    x = int(x)
    output = 0
    power = 1
    while x > 0:
        output = output + (x % 10) * power
        power *= 2
        x //= 10
    return output


while flag:
    instruction = binary_instructions[pc]
    op_code = instruction[:5]
    mem_control = False
    if op_code == "00000":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] + rf[decimal(instruction[13:])]
        )
        if rf[decimal(instruction[7:10])] > ((2**16) - 1):
            rf[decimal(instruction[7:10])] = 0
            rf[7] = 8
    elif op_code == "00001":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] - rf[decimal(instruction[13:])]
        )
        if rf[decimal(instruction[7:10])] < 0:
            rf[decimal(instruction[7:10])] = 0
            rf[7] = 8
    elif op_code == "00010":
        rf[7] = 0
        rf[decimal(instruction[6:9])] = decimal(instruction[9:])
    elif op_code == "00011":
        rf[decimal(instruction[10:13])] = rf[decimal(instruction[13:])]
        rf[7] = 0
    elif op_code == "00100":
        rf[7] = 0
        rf[decimal(instruction[6:9])] = decimal(
            binary_instructions[decimal(instruction[9:])]
        )
    elif op_code == "00101":
        rf[7] = 0
        binary_instructions[decimal(instruction[9:])] = var_length_binary(
            rf[decimal(instruction[6:9])], 16
        )
    elif op_code == "00110":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] * rf[decimal(instruction[13:])]
        )
        if rf[decimal(instruction[7:10])] > ((2**16) - 1):
            rf[decimal(instruction[7:10])] = 0
            rf[7] = 8
    elif op_code == "00111":
        rf[7] = 0
        rf[0] = rf[decimal(instruction[10:13])] // rf[decimal(instruction[13:])]
        rf[1] = rf[decimal(instruction[10:13])] % rf[decimal(instruction[13:])]
        if rf[4] == 0:
            rf[0] = 0
            rf[1] = 0
            rf[7] = 8
    elif op_code == "01000":
        rf[7] = 0
        rf[decimal(instruction[6:9])] = decimal(
            f"{'0' * decimal(instruction[9:])}{bin(rf[decimal(instruction[6:9])])[2:]}"[
                :16
            ]
        )
    elif op_code == "01001":
        rf[7] = 0
        rf[decimal(instruction[6:9])] = decimal(
            f"{bin(rf[decimal(instruction[6:9])])[2:]}{'0' * decimal(instruction[9:])}"[
                -16:
            ]
        )
    elif op_code == "01010":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] ^ rf[decimal(instruction[13:])]
        )
    elif op_code == "01011":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] | rf[decimal(instruction[13:])]
        )
    elif op_code == "01100":
        rf[7] = 0
        rf[decimal(instruction[7:10])] = (
            rf[decimal(instruction[10:13])] & rf[decimal(instruction[13:])]
        )
    elif op_code == "01101":
        rf[7] = 0
        rf[decimal(instruction[10:13])] = (
            decimal("1" * 16) - rf[decimal(instruction[13:])]
        )
    elif op_code == "01110":
        if rf[decimal(instruction[10:13])] == rf[decimal(instruction[13:])]:
            rf[7] = 1
        elif rf[decimal(instruction[10:13])] > rf[decimal(instruction[13:])]:
            rf[7] = 2
        elif rf[decimal(instruction[10:13])] < rf[decimal(instruction[13:])]:
            rf[7] = 4
    elif op_code == "01111":
        mem_addr = instruction[9:]
        mem_control = True
        rf[7] = 0
    elif op_code == "11100":
        mem_addr = instruction[9:]
        if rf[7] == 4:
            mem_control = True
        rf[7] = 0
    elif op_code == "11101":
        mem_addr = instruction[9:]
        if rf[7] == 2:
            mem_control = True
        rf[7] = 0
    elif op_code == "11111":
        mem_addr = instruction[9:]
        if rf[7] == 1:
            mem_control = True
        rf[7] = 0
    elif op_code == "11010":
        flag = False
        rf[7] = 0

    print(var_length_binary(pc, 7), end=f"{' ' * 7}")
    for i in rf:
        print(f" {var_length_binary(i, 16)}", end="")
    print()

    pc += 1

    if mem_control is not False:
        pc = decimal(mem_addr)

for i in binary_instructions:
    print(i)
