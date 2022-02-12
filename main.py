OPS = {
    'MOV': 0x0,
    'ADD': 0x1,
    'SUB': 0x2,
    'ADC': 0x3,
    'SBC': 0x4,
    'AND': 0x5,
    'XOR': 0x6,
    'LSL': 0x7,
    'LDR': 0x8,
    'STR': 0xA,
}
OPCJUMP = {
    'JMP': 0xC0,
    'NOT': 0xC1,
    'JNE': 0xC2,
    'JEQ': 0xC3,
    'JCS': 0xC4,
    'JCC': 0xC5,
    'JMI': 0xC6,
    'JPL': 0xC7,
    'JGE': 0xC8,
    'JLT': 0xC9,
    'JGT': 0xCA,
    'JLE': 0xCB,
    'JHI': 0xCC,
    'JLS': 0xCD,
    'JSR': 0xCE,
    'RET': 0xCF,
}



#So python uses signed and magnitude binary not two's complement
#I fix this using this two_comp function below that basically puts the number is twoscomplement for, the integer value won't be signed anymore
def two_comp(n,nBits):
  if n<0:
    mask = (1 << nBits)-1
    return (~n ^ mask);
  else:
    return n
#Changes the Register format from RN to just N
def convReg(r):
    return int(r.replace("R", ""))



#Changes Immediate format by removing the # and converting to decimal
def convImm(Imm,nBits):
    if "#" == Imm[0]:
        Imm = Imm[1:]
    if "0x" == Imm[0:2]:
        return int(Imm, 16)
    elif "0b" == Imm[0:2]:
        return int(Imm, 2)
    else:
        return two_comp(int(Imm),nBits)


#translates a single line
def translate(a):
    #Check wether the opcode is valid
    if (a[0] not in OPS.keys()) and (a[0] not in OPCJUMP.keys()):
        print("Invalid OPC :", a[0])
        return -1
    #Creates the Operand format
    if len(a) == 4:
        i8 = 0 << 8
        i5_7 = convReg(
            a[2]) << 5  #takes the register number then shifts accordingly
        i0_4 = convImm(a[3],5)  # converts 5bits operand to an integer
        operand = i5_7 + i0_4  #adds together
    else:
        i8 = 1 << 8
        i0_7 = convImm(a[2],8)
        operand = i0_7
    #Creates the Opcode format
    if "J" in a[0]:
        opcode = int(OPCJUMP[a[0]]) << 8
    else:
        i12_15 = int(OPS[a[0]]) << 12
        i9_11 = convReg(a[1]) << 9
        opcode = i8 + i9_11 + i12_15
    #creates assemly
    return hex(operand + opcode)


infile = open("assembly.txt", "r")
outfile = open("machine.ram", "w")
address = 0

for line in infile:
    if line == []:
      pass
    line = line.replace(",", "")
    split = line.split()
    machine = translate(split)
    toWrite = str(str(hex(address)) + " " + str(machine) + "\n")
    print(toWrite)
    outfile.write(toWrite)
    address += 1
infile.close()
outfile.close()
#print(translate(ar))

print("Finished")