from common import *

###- CONSTANTS -###
# Operand separators
OPERAND_SEPARATORS = ', \t'
# Space characters for inbetween operands and instruction
INSTRUCTION_SPACING = ' \t'
# Opcode position in first word; how much to shift opcode relative to the first word (in bits, left)
OPCODE_POSITION = 4
# Word length in bits
WORD_LENGTH = 8
# Max length an instruction can have (in words)
INSTRUCTION_MAX_LENGTH = 3

###- ALL POSSIBLE OPERANDS -###
# Operands
# Format : '<1 char label>':[<position in word>, <word position>, <bit length>, <1: signed, 0: unsigned>, "<full name>"]
OPERANDS= {
           'a':[0, 2, 16, 0, "Address"],
           'I':[0, 2, 8,  0, "Immediate"],
           'A':[0, 1, 4,  0, "A"],
           'P':[0, 1, 4,  0, "Page (A)"],
           'B':[0, 2, 4,  0, "B"],
           'O':[0, 2, 4,  0, "Offset (B)"],
           'D':[4, 1, 4,  0, "Dest"],
           'S':[4, 1, 4,  0, "Selected register"],
           'L':[0, 0, 4,  0, "ALU instruction"],
           'F':[0, 0, 4,  0, "Flag type"],
           'T':[3, 0, 1,  0, "Type value"],
          }

###- NATIVE INSTRUCTIONS -###
# Format: '<mnemonic>':[<opcode>, '<operand flags in order of use in opcode>', <opcode specific mask>, <size in user-defined words>]
# [A=0] means operand A is optional and defaults to 0
OPCODES = {
           'nop' :[0x0, '',     0x000000, 3],
           'brk' :[0x1, '',     0x000000, 3],
           'alu' :[0x2, 'LDAB', 0x000000, 3],
           'alui':[0x3, 'LDAI', 0x000000, 3],
           'ldi' :[0x4, 'DI',   0x000000, 3],
           'lodl':[0x5, 'TDPI', 0x000000, 3],
           'strl':[0x6, 'TSPI', 0x000000, 3],
           'psh' :[0x7, 'S',    0x000000, 3],
           'pop' :[0x8, 'D',    0x000000, 3],
           'jmp' :[0x9, 'a',    0x000000, 3],
           'jf'  :[0xA, 'Fa',   0x000000, 3],
           'rjm' :[0xB, 'PO',   0x000000, 3],
           'call':[0xC, 'a',    0x000000, 3],
           'ret' :[0xD, '',     0x000000, 3],
           'wait':[0xE, '',     0x000000, 3],
           'sta' :[0xF, 'a',    0x000000, 3],
           'lda' :[0xF, 'a',    0x080000, 3],
          } # Opcodes

###- PSEUDO-INSTRUCTIONS -###
# Pseudo-instructions
# Format : 'label':['<resolution as formatted string>']
# - instructions must be separated by newlines ('\n')
PSEUDO_INSTRUCTIONS = {
           'mov'  :['alu 0, {0}, %R0, {1}'],    # MOV DEST, A -> ALU ADD, DEST, %R0, A ; DEST = A
           'movi'  :['alui 0, {0}, %R0, {1}'],  # MOVI DEST, A -> ALUI ADD, DEST, %R0, IMM ; DEST = IMM
           'inc'  :['alui 0, {0}, {0}, 1'],     # INC A -> ALUI ADD, A, A, 1 ; A + 1
           'dec'  :['alui 2, {0}, {0}, 1'],     # DEC A -> ALUI SUB, A, A, 1 ; A - 1
           'cmp'  :['alu 2, %R0, {0}, {1}'],    # CMP A, B -> ALU SUB, %R0, A, B ; A - B (set flags)
           'cmpi' :['alui 2, %R0, {0}, {1}'],   # CMPI A, B -> ALUI SUB, %R0, A, IMM ; A - IMM (set flags)
           'shl'  :['alui 4, {0}, {1}, {2}'],   # SHL DEST, A, B -> ALUI MULT, DEST, A, 2**B ; DEST = A << B
           'add'  :['alu 0, {0}, {1}, {2}'],    # ADD DEST, A, B -> ALU ADD, DEST, A, B ; DEST = A + B
           'addi' :['alui 0, {0}, {1}, {2}'],   # ADDI DEST, A, IMM -> ALUI ADD, DEST, A, IMM ; DEST = A + IMM
           'addc' :['alu 1, {0}, {1}, {2}'],    # ADDC DEST, A, B -> ALU ADDC, DEST, A, B ; DEST = A + B (w/carry)
           'addci':['alui 1, {0}, {1}, {2}'],   # ADDCI DEST, A, IMM -> ALUI ADDC, DEST, A, IMM ; DEST = A + IMM (w/carry)
           'sub'  :['alu 2, {0}, {1}, {2}'],    # SUB DEST, A, B -> ALU SUB, DEST, A, B ; DEST = A - B
           'subi' :['alui 2, {0}, {1}, {2}'],   # SUBI DEST, A, IMM -> ALUI SUB, DEST, A, IMM ; DEST = A - IMM
           'subb' :['alu 3, {0}, {1}, {2}'],    # SUBB DEST, A, B -> ALU SUBB, DEST, A, B ; DEST = A - B (w/borrow)
           'subbi':['alui 3, {0}, {1}, {2}'],   # SUBBI DEST, A, IMM -> ALUI SUBB, DEST, A, IMM ; DEST = A - IMM (w/borrow)
           'mult' :['alu 4, {0}, {1}, {2}'],    # MULT DEST, A, B -> ALU MULT, DEST, A, B ; DEST = A * B
           'multi':['alui 4, {0}, {1}, {2}'],   # MULTI DEST, A, IMM -> ALUI MULT, DEST, A, IMM ; DEST = A * IMM
           'and'  :['alu 5, {0}, {1}, {2}'],    # AND DEST, A, B -> ALU AND, DEST, A, B ; DEST = A & B
           'andi' :['alui 5, {0}, {1}, {2}'],   # ANDI DEST, A, IMM -> ALUI AND, DEST, A, IMM ; DEST = A & IMM
           'or'   :['alu 6, {0}, {1}, {2}'],    # OR DEST, A, B -> ALU OR, DEST, A, B ; DEST = A | B
           'ori'  :['alui 6, {0}, {1}, {2}'],   # ORI DEST, A, IMM -> ALUI OR, DEST, A, IMM ; DEST = A | IMM
           'xor'  :['alu 7, {0}, {1}, {2}'],    # XOR DEST, A, B -> ALU XOR, DEST, A, B ; DEST = A ^ B
           'xori' :['alui 7, {0}, {1}, {2}'],   # XORI DEST, A, IMM -> ALUI XOR, DEST, A, IMM ; DEST = A ^ IMM
           'nand' :['alu 8, {0}, {1}, {2}'],    # NAND DEST, A, B -> ALU NAND, DEST, A, B ; DEST = !(A & B)
           'nandi':['alui 8, {0}, {1}, {2}'],   # NANDI DEST, A, IMM -> ALUI NAND, DEST, A, IMM ; DEST = !(A & IMM)
           'nor'  :['alu 9, {0}, {1}, {2}'],    # NOR DEST, A, B -> ALU NOR, DEST, A, B ; DEST = !(A | B)
           'nori' :['alui 9, {0}, {1}, {2}'],   # NORI DEST, A, IMM -> ALUI NOR, DEST, A, IMM ; DEST = !(A | IMM)
           'xnor' :['alu 10, {0}, {1}, {2}'],   # XNOR DEST, A, B -> ALU XNOR, DEST, A, B ; DEST = !(A ^ B)
           'xnori':['alui 10, {0}, {1}, {2}'],  # XNORI DEST, A, IMM -> ALUI XNOR, DEST, A, IMM ; DEST = !(A ^ IMM)
           'shr'  :['alu 11, {0}, {1}, %R0'],   # SHR DEST, A -> ALU SHR, DEST, A, %R0 ; DEST = A >> 1
           'asr'  :['alu 12, {0}, {1}, %R0'],   # ASR DEST, A -> ALU ASR, DEST, A, %R0 ; DEST = A ~>> 1
           'rol'  :['alu 13, {0}, {1}, %R0'],   # ROL DEST, A -> ALU ROL, DEST, A, %R0 ; DEST = A ROL 1
           'ror'  :['alu 14, {0}, {1}, %R0'],   # ROR DEST, A -> ALU ROR, DEST, A, %R0 ; DEST = A ROR 1
           'shrc' :['alu 15, {0}, {1}, %R0'],   # SHRC DEST, A -> ALU SHRC, DEST, A, %R0 ; DEST = (A >> 1) | (Carry << 15)
           'neg'  :['multi {0}, {1}, -1'],      # NEG DEST, A -> MULTI DEST, A, -1 ; DEST = -A, (A * -1)
           'not'  :['alu 9, {0}, {1}, %R0'],    # NOT DEST, A -> ALU NOR, DEST, A, %R0 ; DEST = !A
           'str'  :['strl 0, {0}, {1}, {2}'],   # STR REG, A, B -> STRL 0, REG, A, B ; REG = MEMORY[A, B]
           'strx' :['strl 1, {0}, {1}, {2}'],   # STRX REG, A, IMM -> STRL 1, REG, A, IMM ; REG = MEMORY[A, IMM]
           'lod'  :['lodl 0, {0}, {1}, {2}'],   # LOD 0, DEST, A, B -> LODL 0, DEST, A, B ; MEMORY[A, B] = REG
           'lodx' :['lodl 1, {0}, {1}, {2}'],   # LODX 0, DEST, A, IMM -> LODL 1, DEST, A, IMM ; MEMORY[A, IMM] = REG
           'jz'   :['jf 0, {0}'],
           'jc'   :['jf 1, {0}'],
           'jo'   :['jf 2, {0}'],
           'js'   :['jf 3, {0}'],
           'jgt'  :['jf 4, {0}'],
           'jlt'  :['jf 5, {0}'],
           'jb'   :['jf 6, {0}'],
           'jirqe':['jf 7, {0}'],
           'jnz'  :['jf 8, {0}'],
           'jnc'  :['jf 9, {0}'],
           'jno'  :['jf 10, {0}'],
           'jns'  :['jf 11, {0}'],
           'jngt' :['jf 12, {0}'],
           'jnlt' :['jf 13, {0}'],
           'jnb'  :['jf 14, {0}'],
           'jnirqe':['jf 15, {0}'],
         }
###- STARTING SYMBOLS -###
# Dictionary that the assembler starts with
STARTING_SYMBOLS = {
                    '%R0' :0,  '%R1' :1,  '%R2' :2,  '%R3' :3, # Registers
                    '%R4' :4,  '%R5' :5,  '%R6' :6,  '%R7' :7,
                    '%R8' :8,  '%R9' :9,  '%RA' :10, '%SR' :11,
                    '%SPX':12, '%SPY':13, '%CSX':14, '%CSY':15,
                   }

###- UTILITY -###
# Define check
def is_define(word: str):
    if(len(word) == 0):
        return 0
    return word == 'define'
# Label check
def is_label(word: str):
    if(len(word) == 0):
        return 0
    return (word[0] == '.') | ((word[-1] == ':') << 1)
# Definition check
def is_definition(word: str, symbols: dict):
    if(len(word) == 0):
        return 0
    return word in symbols
# Pseudo-instruction check
def is_pseudo(word: str):
    if(len(word) == 0):
        return 0
    return word in PSEUDO_INSTRUCTIONS
# Turn label as it appears in code into how it'll be used in instructions ('Done:' -> '.Done')
def to_label(word: str, filename: str, line: int, caller: str):
    if(len(word) == 0):
        return 0
    result = is_label(word)
    if(result != 0):
        if(result == 1):
            return word
        elif(result == 2):
            return ('.' + word[:-1])
        elif(result == 3):
            return word[:-1]
    else:
        fatal_error('assembler', f"{caller}: {filename}:{line}: Could not interpret label \'{word}\'")
# Convert label from many syntaxes into 1 syntax
def convert_label(word: str):
    result = is_label(word)
    if(result != 0):
        if(result == 1):
            return (word[1:] + ':')
        elif(result == 2):
            return word
        elif(result == 3):
            return word[1:]
    else:
        fatal_error('assembler debug', f"convert_label: Could not interpret label \'{word}\'")
# Resolve symbols
# symbols = [symbols, labels, definitions]
def resolve(word: any, filename: str, line: int, symbols: dict, caller: str):
    # Return unmodified if is an int
    if(type(word) == int):
        return word
    # labels
    elif(is_label(word) == 1):
        try:
            return symbols[1][word]
        except KeyError as _ERR:
            print('Labels table dump:')
            print(dump_dict(symbols[1]))
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve label \'{word}\'\n{_ERR}")
    # definitions
    elif(is_definition(word, symbols[2])):
        try:
            return symbols[2][word]
        except KeyError as _ERR:
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve definitioon-.. whaat? I checked! It's inside the table I swear! Take a look!\nDump:\n{dump_dict(symbols[2])}\n{_ERR}")
    # everything else
    try:
        return symbols[0][word]
    except KeyError as _ERR:
        print('Symbol table dump:')
        print(dump_dict(symbols[0]))
        fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve symbol \'{word}\'\n{_ERR}")
# Resolve integers, ignores everything else
def resolve_integer(word: any, filename: str, line: int, caller: str):
    # Return unmodified if is an int, or empty
    if((type(word) == int) or (len(word) == 0)):
        return word
    # Auto-detect format
    if(word[0] in '-0123456789'):
        try:
            offset = 0
            if(word[0] == '-'):
                offset = 1
            if(word[offset:offset + 2] == '0x'):
                return int(word[:offset] + word[offset + 2:], 16)
            elif(word[offset:offset + 2] == '0o'):
                return int(word[:offset] + word[offset + 2:], 8)
            elif(word[offset:offset + 2] == '0b'):
                return int(word[:offset] + word[offset + 2:], 2)
            else:
                return int(word, 10)
        except ValueError as _ERR:
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve number \'{word}\'\n{_ERR}")
    # $ prefixed hexadecimal
    elif(word[0] == '$'):
        try:
            return int(word[1:], 16)
        except ValueError as _ERR:
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve hexadecimal \'{word}\'\n{_ERR}")
    # Return unmodified if not an integer
    return word
# Handle character constant
def char_constant(string: str, idx: int, filename: str, line: int, caller: str, resolve_strings: bool = True):
    idx_end=strfind_escape(string, '\'', idx + 1)
    if(idx_end==-1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing terminating \' character.\n{string}\n{' ' * idx}^{'~' * (len(string) - idx - 1)}")
    idx_end += 1
    if(not resolve_strings):
        return (idx, idx_end, [string[idx:idx_end]])
    try:
        evaluated = eval(string[idx:idx_end])
    except Exception as _ERR:
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Could not evaluate character constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}\n{_ERR}")
    if(len(evaluated) > 1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Too many characters in character constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}")
    elif(len(evaluated) == 0):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty character constant.\n{string}\n{' ' * idx}^~")
    return (idx, idx_end, [ord(evaluated) & ((1 << WORD_LENGTH) - 1)])
# Handle string constant
def string_constant(string: str, idx: int, filename: str, line: int, caller: str, resolve_strings: bool = True):
    idx_end=strfind_escape(string, '\"', idx + 1)
    if(idx_end==-1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing terminating \" character.\n{string}\n{' ' * idx}^{'~' * (len(string) - idx - 1)}")
    idx_end += 1
    if(not resolve_strings):
        return (idx, idx_end, [string[idx:idx_end]])
    try:
        evaluated = eval(string[idx:idx_end])
    except Exception as _ERR:
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Could not evaluate string constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}\n{_ERR}")
    if(len(evaluated) == 0):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty string constant.\n{string}\n{' ' * idx}^~")
    return (idx, idx_end, [(ord(char) & ((1 << WORD_LENGTH) - 1)) for char in evaluated])
# Decompose instruction + character constants
def decompose_instruction(string: str, filename: str, line: int, caller: str, resolve_strings: bool = True):
    idx=0
    output=[]
    while(idx<len(string)):
        idx=inverted_strfind(string, OPERAND_SEPARATORS, idx)
        if(idx==-1):
            break
        if(string[idx] == '\''):
            idx, idx_end, constant = char_constant(string, idx, filename, line, caller, resolve_strings)
            output = output + constant
        elif(string[idx] == '\"'):
            idx, idx_end, constants = string_constant(string, idx, filename, line, caller, resolve_strings)
            if(len(constants) != 1):
                fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1} There must be exactly 1 character in string constant. (for instruction operands)\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}")
            output = output + constants
        else:
            idx_end=strfind(string, OPERAND_SEPARATORS, idx)
            if(idx_end==-1):
                output.append(string[idx:])
                break
            output.append(string[idx:idx_end])
        idx=idx_end
    if(resolve_strings):
        return [resolve_integer(x, filename, line, caller) for x in output]
    return output
# Decompose instruction + character constants + strings
def decompose_instruction_multi(string: str, filename: str, line: int, caller: str, resolve_strings: bool = True):
    idx=0
    output=[]
    while(idx<len(string)):
        idx=inverted_strfind(string, OPERAND_SEPARATORS, idx)
        if(idx==-1):
            break
        if(string[idx] == '\''):
            idx, idx_end, constant = char_constant(string, idx, filename, line, caller, resolve_strings)
            output = output + constant
        elif(string[idx] == '\"'):
            idx, idx_end, constants = string_constant(string, idx, filename, line, caller, resolve_strings)
            output = output + constants
        else:
            idx_end=strfind(string, OPERAND_SEPARATORS, idx)
            if(idx_end==-1):
                output.append(string[idx:])
                break
            output.append(string[idx:idx_end])
        idx=idx_end
    if(resolve_strings):
        return [resolve_integer(x, filename, line, caller) for x in output]
    return output
# Parse line
def parse_line(line: list, filename: str, caller: str, resolve_strings: bool = True):
    decomposed_lines = []
    decomposed_definitions = []
    split_A = 0
    split_B = 0
    instruction = ''
    # Labels and finding instruction
    while(is_label(instruction) or (split_A == 0)):
        split_B = strfind(line[0], INSTRUCTION_SPACING, split_A)
        if(split_B == -1):
            instruction = line[0][split_A:]
        else:
            instruction = line[0][split_A:split_B]
        if(is_label(instruction)):
            decomposed_lines.append([[instruction], line[1]])
        if(split_B == -1):
            break
        split_A = inverted_strfind(line[0], INSTRUCTION_SPACING, split_B)
    if(split_B != -1):
        parameters  = line[0][split_A:]
    else:
        parameters = ""
    if(is_label(instruction)):
        return decomposed_lines, decomposed_definitions
    instruction = instruction.lower()
    # Definition
    if(is_define(instruction)):
        decomposed_definitions.append([[instruction] + decompose_instruction(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # ORG
    elif(instruction == 'org'):
        decomposed_lines.append([[instruction] + decompose_instruction(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # DB
    elif(instruction == 'db'):
        decomposed_lines.append([[instruction] + decompose_instruction_multi(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # Assume it's an instruction
    else:
        decomposed_lines.append([[instruction] + decompose_instruction(parameters, filename, line[1], caller, resolve_strings), line[1]])
    return decomposed_lines, decomposed_definitions
# Recompose line
def recompose_line(line: list):
    instruction = line[0][0]
    if(is_label(instruction)):
        return convert_label(instruction)
    return instruction.upper() + ' ' + ', '.join(str(x) for x in line[0][1:])
# Display multiple lines of Assembly
def print_assembly(lines: list, last_was: list, line_width: int):
    last_line = 0
    special_case = False
    for line in lines:
        if(last_line == line[1]):
            print("%s: "%(' ' * line_width), end='')
        else:
            print("%0*d: "%(line_width, line[1]), end='')
        if((line[0][0] not in ['org', 'db', 'define']) and (is_label(line[0][0]) == 0)):
            print("  ", end='')
        print(recompose_line(line), end='')
        # I don't even know
        if(((line[1] in last_was) and (last_line != line[1])) or special_case):
            if(is_label(line[0][0]) != 0):
                special_case = True
            else:
                print(" ; resolved from ; %s"%(recompose_line(last_was[line[1]])), end='')
                special_case = False
        last_line = line[1]
        print()
# Display multiple lines of Assembly with machine code positions
def print_assembly_wordpos(lines: list, last_was: list, line_width: int, hex_width: int):
    last_line = 0
    special_case = False
    for line in lines:
        if(last_line == line[1]):
            print("%s:%0*X: "%(' ' * line_width, hex_width, line[2]), end='')
        else:
            print("%0*d:%0*X: "%(line_width, line[1], hex_width, line[2]), end='')
        if((line[0][0] not in ['org', 'db', 'define']) and (is_label(line[0][0]) == 0)):
            print("  ", end='')
        print(recompose_line(line), end='')
        # I don't even know
        if(((line[1] in last_was) and (last_line != line[1])) or special_case):
            if(is_label(line[0][0]) != 0):
                special_case = True
            else:
                print(" ; resolved from ; %s"%(recompose_line(last_was[line[1]])), end='')
                special_case = False
        elif(line[0][0] == 'org'):
            print(" ; jump to 0x%0*X"%(hex_width, line[2]), end='')
        last_line = line[1]
        print()
# Strip line of comments
def remove_comment(comment_symbols: str, line: str):
    index=strfind(line, comment_symbols)
    if(index==-1):
        return line
    return line[:index]

###- MAIN THING -###
# Assemble function
def assemble(assembly_filename: str, ROM_size: int, verbose_level: int, debug_flags: int, matt_mode: bool):
    try:
        assembly_file = open(assembly_filename, 'r')
    except FileNotFoundError as _ERR:
        fatal_error('assembler', f"{assembly_filename}: File not found.\n{_ERR}")
    if(verbose_level >= 0):
        print(f"assembler: Reading from \'{assembly_filename}\'")
        if(matt_mode):
            # Matt mode engaged.
            print(f"assembler: Matt mode active. ORG, DB, & multi-line pseudo-instructions are disabled.")
    lines = [line.strip() for line in assembly_file]

    # DEBUG: ROM address size constant
    ROM_address_size = int(log2(ROM_size) + 3) >> 2
    line_address_size = int(log(len(lines), 10) + 1)
    if(verbose_level >= 2):
        print("Address hex width: %d (%s)"%(ROM_address_size, ''.join(hex(x%16).upper()[2] for x in range(ROM_address_size))))
        print("Line address width: %d (%s)"%(line_address_size, ''.join(chr(0x30 + (x%10)) for x in range(line_address_size))))

    # Remove comments and blanklines, and add line number
    lines = [[remove_comment("/;#", line).strip(), idx+1] for idx, line in enumerate(lines)]

    # Remove empty lines & add line numbers
    lines = [line for line in lines if(len(line[0]) != 0)]

    # Populatesymbol table
    symbols = STARTING_SYMBOLS
    # Definitions table
    definitions = {}
    # Labels table
    labels = {}

    # Calculate number of operands and add to macro element
    pop_keys = [pop for pop in PSEUDO_INSTRUCTIONS]
    for pop in pop_keys:
        popinfo=PSEUDO_INSTRUCTIONS[pop]
        # Remove pseudo instructions with more than 1 line of resolution if in Matt mode
        if((len(popinfo[0].split('\n')) > 1) and matt_mode):
            PSEUDO_INSTRUCTIONS.pop(pop)
            continue
        # sketch sketch
        words=[]
        for line in popinfo[0].split('\n'):
            for decomposed in parse_line([line, 0], assembly_filename, 'pseudo-instruction prepper')[0]:
                words += decomposed[0]
        nums=[int(word[1:len(word)-1]) for word in words if str(word)[0]=='{']
        if(len(nums)==0):
            PSEUDO_INSTRUCTIONS[pop].insert(0, 0)
        else:
            PSEUDO_INSTRUCTIONS[pop].insert(0, max(nums)+1)
    
    # Check operands
    for operand in OPERANDS:
        if(OPERANDS[operand][1] >= INSTRUCTION_MAX_LENGTH):
            fatal_error('assembler', f"loading stage: wtf: Operand \'{OPERANDS[operand][4]}\' defined in a word outside set maximum length, are you sure it\'s correct?")
        if(OPERANDS[operand][0] >= WORD_LENGTH):
            fatal_error('assembler', f"loading stage: wtf: Operand \'{OPERANDS[operand][4]}\' shift amount is bigger than a word, are you sure it\'s correct?")
        if((((OPERANDS[operand][1] + 1) * WORD_LENGTH) - OPERANDS[operand][0] - OPERANDS[operand][2]) < 0):
            fatal_error('assembler', f"loading stage: wtf: Operand \'{OPERANDS[operand][4]}\' is defined outside the instruction, are you sure it\'s correct?")

    # Make instructions more machine-friendly and check instruction lengths
    for opcode in OPCODES:
        # Error and prompt user if instruction's length exceeds max length
        if((OPCODES[opcode][3] * WORD_LENGTH) > (INSTRUCTION_MAX_LENGTH * WORD_LENGTH)):
            fatal_error('assembler', f"loading stage: wtf: Instruction \'{opcode}\' exceeds set maximum length, are you sure it\'s correct?")

        processed_opcode=[]
        operands=OPCODES[opcode][1]

        idx=0
        minimum_operands=0
        while(idx<len(operands)):
            # Process optional operand
            if(operands[idx]=='['):
                idx_end=operands.find(']', idx)
                if(idx_end==-1):
                    fatal_error('assembler', f"loading stage: syntax error: No closing brace for operand \'{operands[idx+1]}\' in instruction \'{opcode}\'.")
                substr=operands[idx+1:idx_end]
                if(substr[2:]==''):
                    fatal_error('assembler', f"loading stage: wtf: No default defined for operand \'{substr[0]}\' for instruction \'{opcode}\'.")
                processed_opcode.append([substr[0], int(substr[2:])])
                idx=idx_end+1
                minimum_operands-=1
            # Process sequence of mandatory operands
            else:
                idx_end=operands.find('[', idx)
                if(idx_end==-1):
                    idx_end += len(operands) + 1
                substr=operands[idx:idx_end]
                processed_opcode = processed_opcode + [[x] for x in substr]
                idx=idx_end

        # Check operands used in instruction; make sure operands don't go outside the instruction
        for index in range(len(processed_opcode)):
            operand = processed_opcode[index][0]
            if(OPERANDS[operand][1] >= OPCODES[opcode][3]):
                fatal_error('assembler', f"loading stage: wtf: Operand \'{OPERANDS[operand][4]}\' in instruction \'{opcode}\' is defined in a word outside the instruction\'s length, are you sure it\'s correct?")

        maximum_operands=len(processed_opcode)
        minimum_operands=minimum_operands+maximum_operands
        processed_opcode=[processed_opcode, minimum_operands, maximum_operands]
        OPCODES[opcode][1]=processed_opcode

    # Validity check
    for opcode in OPCODES:
        operands=OPCODES[opcode][1][0]
        maxim=1
        for idx, operand in enumerate(operands):
            if(maxim <= len(operand)):
                maxim=len(operand)
            else:
                fatal_error('assembler', f"loading stage: wtf: Optional operand \'{operands[idx-1][0]}\' declared inbetween mandatory ones in instruction \'{opcode}\'! (Will cause problems later)")

#    for symbol in OPCODES:
#        symbols[symbol] = OPCODES[symbol][0] # Add corresponding numeral opcode

    # Decompose instructions and separate labels
    decomposed = []
    decomposed_definitions = []
    original_lines = {}
    for line in lines:
        new_lines, new_definitions = parse_line(line, assembly_filename, 'parser')
        decomposed = decomposed + new_lines
        decomposed_definitions = decomposed_definitions + new_definitions
        new_lines, new_definitions = parse_line(line, assembly_filename, 'parser', False)
        original_lines[line[1]] = new_lines + new_definitions

    # DEBUG: display Assembly right now
    if(verbose_level >= 3):
        print("ASSEMBLY:")
        print_assembly(decomposed, {}, line_address_size)

    # DEBUG: display definitions
    if(verbose_level >= 3):
        print("\nDEFINITIONS:")
        print_assembly(decomposed_definitions, {}, line_address_size)

    # Resolve pseudo-instructions
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nRESOLVING PSEUDO-INSTRUCTIONS..")
    last_was = {}
    cont=True
    while(cont):
        cont=False
        index = 0

        while(index < len(decomposed)):
            line = decomposed[index]
            line_number=line[1]
            words=line[0]

            if(is_pseudo(words[0])):
                if(line_number not in last_was):
                    last_was[line_number] = line
                cont=True
                popinfo=PSEUDO_INSTRUCTIONS[words[0]]
                if(popinfo[0] != (len(words) - 1)):
                    fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Incorrect number of operands for pseudo-instruction \'{words[0]}\'")
                # !!! HACKY SUBSTITUTION FOR A REAL METHOD, REMOVE LATER !!!
                if(words[0] == 'shl'):
                    gen_lines = popinfo[1].format(*(words[1:2] + [2 ** words[3]])).split('\n')
                else:
                    gen_lines = popinfo[1].format(*words[1:]).split('\n')
                parsed = []
                for gline in gen_lines:
                    new_lines, new_definitions = parse_line([gline, line_number], assembly_filename, 'parser')
                    parsed = parsed + new_lines
                    decomposed_definitions = decomposed_definitions + new_definitions
                # DEBUG: display resolved line
                if(verbose_level >= 2):
                    print('%0*d: %s -> %s'%(line_address_size, line_number, recompose_line(line), '\\n'.join(recompose_line(gline) for gline in parsed)))
                decomposed = decomposed[:index] + parsed + decomposed[index + 1:]
            else:
                index += 1

    # DEBUG: display Assembly after resolving pseudo-instructions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly(decomposed, last_was, line_address_size)

    # DEBUG: display definitions after resolving pseudo-instructions
    if(verbose_level >= 3):
        print("\nDEFINITIONS NOW:")
        print_assembly(decomposed_definitions, last_was, line_address_size)

    # Memorize definitions
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nMEMORIZING DEFINITIONS:")
    for index in range(len(decomposed_definitions)):
        line = decomposed_definitions[index]
        line_number = line[1]
        words = line[0]
        if(len(words) == 1):
            fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: No parameters given for definition.")
        elif(len(words) == 2):
            fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Only name given for definition.")
        elif(len(words) > 3):
            fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Too many parameters given for definition.")
        elif((words[1][0] in "0123456789") or (not words[1].isalnum())):
            fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Invalid name for definition \'{words[1]}\'")
        elif(type(words[2]) != int):
            fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Definition resolution couldn\'t be resolved as an integer \'{words[2]}\'")
        # 2000 error handling, 1 functional
        definitions[words[1]] = words[2]
        # DEBUG: display definition
        if(verbose_level >= 2):
            print(f"\'{words[1]}\' = {words[2]}")

    # DEBUG: display definitions table
    if(verbose_level >= 3):
        print(f"\nDEFINITIONS TABLE:\n{dump_dict(definitions)}", end='')

    # Resolve definitions
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nRESOLVING DEFINITIONS (USER-DEFINED & ISA-DEFINED)..")
    for index in range(len(decomposed)):
        line = deep_copy(decomposed[index])
        line_number = line[1]
        params = line[0]
        changed = False
        for index2 in range(1, len(params)):
            if(params[index2] in definitions):
                changed = True
                decomposed[index][0][index2] = definitions[params[index2]]
            elif(params[index2] in symbols):
                changed = True
                decomposed[index][0][index2] = symbols[params[index2]]
        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*X: %s -> %s"%(line_address_size, line_number, recompose_line(line), recompose_line(decomposed[index])))

    # DEBUG: display Assembly after resolving definitions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly(decomposed, last_was, line_address_size)

    # Calculate positions of lines in the machine code file, using the user-defined instruction lengths
    # Resolves & removes ORG directives too
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nCALCULATING POSITIONS IN MACHINE CODE..")
    position = 0 # Default is position 0
    for index in range(len(decomposed)):
        line = decomposed[index]
        words = line[0]
        line_number = line[1]
        # DEBUG: display current line
        if(verbose_level >= 2):
            spacing = ' ' * line_address_size
            print("%0*d: %s"%(line_address_size, line_number, recompose_line(line)))

        # Handle ORG directive
        if(words[0] == 'org'):
            # Error on ORG directive if in Matt mode
            if(matt_mode):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Encountered ORG directive, but they are disabled in Matt mode.")
            if(len(words) == 1):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: No parameters given for ORG directive.")
            elif(len(words) > 2):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Too many parameters given for ORG directive.")
            position = words[1]
            # DEBUG: show position jump
            if(verbose_level >= 2):
                print("%s: Encountered ORG directive, changing position to 0x%0*X"%(spacing, ROM_address_size, position))

        # Check if position is in ROM bounds
        if(position >= ROM_size):
            fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Position {'0x%X'%position} is out of bounds of the ROM. (ROM size = {ROM_size})")
        elif(position < 0):
            fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Position went negative ({'0x%X'%position}). What the fuck are you doing?")

        # Add current position to line
        decomposed[index].append(position)
        # DEBUG: show what position current line is in the machine code
        if(verbose_level >= 2):
            print("%s: is at 0x%0*X"%(spacing, ROM_address_size, position))

        # Handle known instruction
        if(words[0] in OPCODES):
            position += OPCODES[words[0]][3]
            # DEBUG: show how many words 'position' is incremented by
            if(verbose_level >= 2):
                print("%s: \'%s\' is a known instruction, and is %d words.\n%s: Incrementing position by %d words."%(spacing, words[0], OPCODES[words[0]][3], spacing, OPCODES[words[0]][3]))
        # Handle DB directive
        elif(words[0] == 'db'):
            # Error on DB directive if in Matt mode
            if(matt_mode):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Encountered DB directive, but they are disabled in Matt mode.")
            if(len(words) == 1):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: No parameters given for DB directive.")
            position += len(words) - 1
            # DEBUG: show how many words 'position' is incremented by
            if(verbose_level >= 2):
                print("%s: Encountered DB directive, that defines %d words.\n%s: Incrementing position by %d words."%(spacing, len(words) - 1, spacing, len(words) - 1))

    # DEBUG: show assembly after calculating positions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly_wordpos(decomposed, last_was, line_address_size, ROM_address_size)

    # Memorize labels
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nMEMORIZING LABELS..")
    for index in range(len(decomposed)):
        line = decomposed[index]
        words = line[0]
        line_number = line[1]
        line_word_pos = line[2]

        result = is_label(words[0])
        if(result != 0):
            label = to_label(words[0], assembly_filename, line_number, 'label resolver')
            labels[label] = line_word_pos
            # DEBUG: show what position label is at
            if(verbose_level >= 2):
                print("\'%s\' (\'%s\') is at 0x%0*X"%(label, words[0], ROM_address_size, line_word_pos))

    # DEBUG: show label table
    if(verbose_level >= 3):
        print("\nLABEL TABLE:")
        print(dump_dict(labels))

    # Resolve labels
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nRESOLVING LABELS..")
    for index in range(len(decomposed)):
        line = deep_copy(decomposed[index])
        line_number = line[1]
        params = line[0]
        changed = False
        for index2 in range(1, len(params)):
            if(type(params[index2]) == int):
                continue
            if(is_label(params[index2]) == 1):
                changed = True
                try:
                    decomposed[index][0][index2] = labels[params[index2]]
                except KeyError as _ERR:
                    fatal_error('assembler', f"label resolver: {assembly_filename}:{line_number}: Couldn\'t resolve label.\nLabel table dump:\n{dump_dict(labels)}")
        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*d:%0*X: %s -> %s"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line), recompose_line(decomposed[index])))

    # DEBUG: display Assembly after resolving labels
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly_wordpos(decomposed, last_was, line_address_size, ROM_address_size)

    # Lines should be clean by now

    # Start assembling
    # DEBUG: show current action
    if(verbose_level >= 1):
        print("\nSTARTING ASSEMBLY..")
    output_machine_code = []
    last_line = -1
    for i in range(len(decomposed)):
        # Decompose instruction
        line=decomposed[i]
        words=line[0]
        line_number=line[1]

        machine_code = 0
        current_instruction = words[0]
        words = words[1:]
        
        # Begin machine code translation
        # handle DB directive
        if(current_instruction == 'db'):
            output_machine_code.append([sum(words[len(words) - index - 1] << (index * WORD_LENGTH) for index in range(len(words))), line_number, line[2], len(words), original_lines[line_number][0]])
        # skip ORG directives
        elif(current_instruction == 'org'):
            continue
        # skip labels
        elif(is_label(current_instruction) != 0):
            continue
        # handle known instructions
        elif(current_instruction in OPCODES):
            # Resolve mnemonic
            try:
                current_opinfo = OPCODES[current_instruction]
            except KeyError as _ERR:
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Unknown instruction mnemonic \'{current_instruction}\'\n{_ERR}")
            current_size = current_opinfo[3]

            # Assemble opcode
            machine_code |= current_opinfo[0] << (OPCODE_POSITION + ((current_opinfo[3] - 1) * WORD_LENGTH))

            # Number of operands check
            if(  current_opinfo[1][-2] > len(words)):
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Not enough operands for instruction \'{current_instruction}\'")
            elif(current_opinfo[1][-1] < len(words)):
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Too many operands for instruction \'{current_instruction}\'")

            # Check operands and assemble them
            for idx, opcode in enumerate(current_opinfo[1][0]):
                if(len(words)<=idx):
                    words.append(opcode[1])
                opinfo = OPERANDS[opcode[0]]
                mask   = (1<<opinfo[2]) - 1
                if opinfo[3] and (words[idx]<0):
                    words[idx]=(~words[idx])+1
                if words[idx] != (words[idx] & mask):
                    fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Invalid {opinfo[4]} for instruction \'{current_instruction}\'")
                machine_code |= (words[idx] & mask) << (opinfo[0] + ((current_opinfo[3] - opinfo[1] - 1) * WORD_LENGTH))
                # Just to be safe, it's ANDed with the mask

            # OR with opcode-specific mask
            machine_code |= current_opinfo[2]

            # Length check
            if((int(log2(machine_code)) + 1) > (current_opinfo[3] * WORD_LENGTH)):
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Uh-oh! the instruction at this line ended up bigger than expected, this should be investigated.. You should open an issue about this!\n" +
                "Relevant info:\n" +
                "  Version format: {1}\n  Version.......: {0}\n".format(*render_version(VERSION, VER_FMT)) +
                f"  {assembly_filename}:{line_number}: {lines[i][0]}\n")

            # Output
            # Format is: [<INSTRUCTION>, <LINE IN ASSEMBLY FILE>, <POSITION IN WORDS>, <SIZE IN WORDS>, [<ORIGINAL OPERANDS>]]
            if(last_line != line_number):
                output_machine_code.append([machine_code, line_number, line[2], current_size, original_lines[line_number][0]])
            else:
                output_machine_code.append([machine_code, line_number, line[2], current_size])
            last_line = line_number
        else:
            fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: \'{current_instruction.upper()}\' is not a valid instruction.")

    if(verbose_level >= 1):
        print("\nSORTING OUTPUT BY POSITION IN MACHINE CODE..")
    output_machine_code.sort(key = lambda x:x[2])

    # DEBUG: print machine code and their origins
    if(verbose_level >= 2):
        print("OUTPUT:\n%s\nDISAMBIGUATION:"%(dump_array(output_machine_code)))
        word_size = (WORD_LENGTH + 3) >> 2
        for machine_code in output_machine_code:
            print('%0*d:%0*X: %s'%(line_address_size, machine_code[1], ROM_address_size, machine_code[2], " ".join("%0*X"%(word_size, x) for x in word_dissect(machine_code[0], machine_code[3], WORD_LENGTH))), end='')
            if(len(machine_code) >= 5):
                print(' ; %s'%(recompose_line(machine_code[4])), end='')
            print()
    if(debug_flags & 1):
        print(f'Label table dump:\n{dump_dict(labels)}')
    if(debug_flags & 2):
        print(f'Definition table dump:\n{dump_dict(definitions)}')
    return output_machine_code

# Formats output of the assembler
def formatter(assembler_output, output_file, rom_size, padding_word, format_style, verbose_level):
    format_style = format_style.lower()
    ROM_address_size = int(log2(rom_size) + 3) >> 2
    word_size = (WORD_LENGTH + 3) >> 2
    if(format_style in ['raw', 'image']):
        output = open(output_file, 'wb')
    else:
        output = open(output_file, 'w')

    if(verbose_level >= 1):
        print(f"formatter: Outputting to \'{output_file}\'")
        print("formatter: Outputting as", end='')

    # Matt's assembler format
    ## Outputs binary as ASCII
    ## Output is as big as it needs to be
    ## Empty space is filled with provided padding_word
    if(format_style == 'matt'):
        if(verbose_level >= 1):
            print(" Matt\'s format.")
        head = 0
        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = instruction[0]
            if(head != position):
                for _ in range(position - head):
                    output.write(bin(padding_word)[2:].zfill(WORD_LENGTH) + '\n')
                head = position
            output.write(bin(word)[2:].zfill(WORD_LENGTH * size) + '\n')
            head += size
    # Raw format
    ## Just raw binary, not human friendly
    ## Output is as big as it needs to be if raw format
    ## Output is fattened to be (rom_size * bytes_per_word) bytes with provided padding_word if image format
    ## Empty space is filled with provided padding_word
    elif(format_style in ['raw', 'image']):
        if(verbose_level >= 1):
            if(format_style == 'raw'):
                print(" raw format.")
            else:
                print(" ROM image format.")
        head = 0
        bytes_per_word = (WORD_LENGTH + 7) >> 3
        padding = bytes(word_dissect(padding_word, bytes_per_word, 8))

        if(format_style == 'image'):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])

        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = bytes(word_dissect(instruction[0], size * bytes_per_word, 8))
            if(head != position):
                for _ in range(position - head):
                    output.write(padding)
                head = position
            output.write(word)
            head += size
    # Hexdump formats
    ## Better human readability
    ## Output is fattened to be rom_size words (* Dependent on variation)
    ## Empty space is filled with provided padding_word (* Dependent on variation)
    ## Output is squeezed when a repeating line is detected to save space. (* Dependent on variation)
    elif(format_style[:7] == 'hexdump'):
        head = 0
        first_word = True
        # Disables squeezing
        no_squeeze = 'ns' in format_style
        # Disables squeezing for instructions
        squeeze_only_pad = 'sp' in format_style
        # Disables padding
        no_pad = 'np' in format_style
        # Disables fattening
        no_fat = ('nf' in format_style) or no_pad
        last_word = 0
        repeating = False
        address_length = int(log2(rom_size) + 3) >> 2

        if(verbose_level >= 1):
            print(" hexdump format", end='')

            if(no_squeeze):
                print(", without squeezing", end='')
            if(squeeze_only_pad):
                print(", squeezing only padding/fat", end='')
            if(no_pad):
                print(", without padding", end='')
            if(no_fat):
                print(", without file fattening", end='')
            print('.')

        if(not no_fat):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])

        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = instruction[0]
            if(head != position):
                for _ in range(position - head):
                    if(no_pad):
                        head = position
                        break
                    # if word isn't repeating, write
                    if((last_word != padding_word) or first_word or no_squeeze):
                        repeating = False
                        output.write('%0*X: %0*X\n'%(ROM_address_size, head, word_size, padding_word))
                        last_word = padding_word
                    # squeeze if haven't squeezed already
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                        head = position
                        break
                    head += 1
            # if word isn't repeating, write
            if((last_word != word) or first_word or no_squeeze or squeeze_only_pad):
                repeating = False
                output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in word_dissect(word, size, WORD_LENGTH))))
                last_word = word
            # squeeze if haven't squeezed already
            elif(not repeating):
                output.write('*\n')
                repeating = True
            head += size
            first_word = False
        if(repeating):
            output.write('%0*X:\n'%(ROM_address_size, head))
    # Logisim3 format
    elif(format_style[:8] == 'logisim3'):
        current_line = [0] * 16
        last_line = [-1] * 16
        current_line_index = 0
        head = 0
        index = 0
        repeating = False
        do_squeeze = ('ys' in format_style[8:])
        no_fat = ('nf' in format_style[8:])
        if(verbose_level >= 1):
            print(" logisim v3.0 format", end='')
            if(do_squeeze):
                print(", with squeezing", end='')
            if(no_fat):
                print(", with no file fattening", end='')
            print('.')
        if(not no_fat):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])
        output.write("v3.0 hex words addressed\n")
        while(index != len(assembler_output)):
            current = assembler_output[index]
            size = current[3]
            words = word_dissect(current[0], size, WORD_LENGTH)
            position = current[2]
            while((head + current_line_index) != position):
                if(current_line_index == 16):
                    if((current_line != last_line) or (not do_squeeze)):
                        output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in current_line)))
                        last_line = current_line.copy()
                        repeating = False
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                    current_line_index = 0
                    head += 16
                current_line[current_line_index] = padding_word
                current_line_index += 1
            for word in words:
                if(current_line_index == 16):
                    if((current_line != last_line) or (not do_squeeze)):
                        output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in current_line)))
                        last_line = current_line.copy()
                        repeating = False
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                    current_line_index = 0
                    head += 16
                current_line[current_line_index] = word
                current_line_index += 1
            index += 1
        if(current_line_index != 0):
            output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, current_line[x]) for x in range(current_line_index))))
    # Logisim2 RLE format
    elif(format_style == 'logisim2'):
        index = 0
        head  = 0
        line_index   = 0
        current_word = -1
        repetition   = 0
        if(verbose_level >= 1):
            print(" logisim v2.0 RLE format.")
        output.write("v2.0 raw\n")
        while(index != len(assembler_output)):
            current = assembler_output[index]
            size = current[3]
            words = word_dissect(current[0], size, WORD_LENGTH)
            position = current[2]
            while(head != position):
                if(current_word == -1):
                    current_word = padding_word
                    head += 1
                    continue
                if(current_word == padding_word):
                    repetition += 1
                else:
                    if(repetition >= 3):
                        if(line_index == 8):
                            output.write('\n')
                            line_index = 0
                        if(line_index == 7):
                            output.write('%d*%X'%(repetition + 1, current_word))
                        else:
                            output.write('%d*%X '%(repetition + 1, current_word))
                        line_index += 1
                    else:
                        for _ in range(repetition + 1):
                            if(line_index == 8):
                                output.write('\n')
                                line_index = 0
                            if(line_index == 7):
                                output.write('%X'%(current_word))
                            else:
                                output.write('%X '%(current_word))
                            line_index += 1
                    repetition = 0
                    current_word = padding_word
                head += 1
            for word in words:
                if(current_word == -1):
                    current_word = word
                    head += 1
                    continue
                if(current_word == word):
                    repetition += 1
                else:
                    if(repetition >= 3):
                        if(line_index == 8):
                            output.write('\n')
                            line_index = 0
                        if(line_index == 7):
                            output.write('%d*%X'%(repetition + 1, current_word))
                        else:
                            output.write('%d*%X '%(repetition + 1, current_word))
                        line_index += 1
                    else:
                        for _ in range(repetition + 1):
                            if(line_index == 8):
                                output.write('\n')
                                line_index = 0
                            if(line_index == 7):
                                output.write('%X'%(current_word))
                            else:
                                output.write('%X '%(current_word))
                            line_index += 1
                    repetition = 0
                    current_word = word
                head += 1
            index += 1
        if(repetition >= 3):
            if(line_index == 8):
                output.write('\n')
                line_index = 0
            if(line_index == 7):
                output.write('%d*%X'%(repetition + 1, current_word))
            else:
                output.write('%d*%X '%(repetition + 1, current_word))
            line_index += 1
        else:
            for _ in range(repetition + 1):
                if(line_index == 8):
                    output.write('\n')
                    line_index = 0
                if(line_index == 7):
                    output.write('%X'%(current_word))
                else:
                    output.write('%X '%(current_word))
                line_index += 1
        output.write('\n')
    # DEBUG format
    ## Most human readability
    ## Not for normal use
    elif(format_style == 'debug'):
        if(verbose_level >= 1):
            print(" DEBUG format.")
        line_address_size = int(log(find_max(assembler_output, key = lambda x:x[1]), 10) + 1)
        for machine_code in assembler_output:
            output.write('%0*d:%0*X: %s'%(line_address_size, machine_code[1], ROM_address_size, machine_code[2], " ".join("%0*X"%(word_size, x) for x in word_dissect(machine_code[0], machine_code[3], WORD_LENGTH))))
            if(len(machine_code) >= 5):
                output.write(' ; %s'%(recompose_line(machine_code[4])))
            output.write('\n')
    else:
        fatal_error('formatter', f"Don\'t know format \'{format_style}\'")

    output.close()
