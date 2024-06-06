# All rights to this code go to the original owner, @MattBatWings
from common import *

###- CONSTANTS -###
# Number of registers
NUMBER_OF_REGISTERS = 0 # Does not apply to this kind of architecture
# Opcode position; how much to shift opcode (in bits, left)
OPCODE_POSITION = 16
# Max length an instruction can have (in bits)
INSTRUCTION_MAX_LENGTH = 24

###- ALL POSSIBLE OPERANDS -###
# Operands
# Format : '<1 char label>':[<position>, <bit length>, <1: signed, 0: unsigned>, "<full name>"]
OPERANDS= {
           'A':[0, 16, 0, 'ADDRESS'],
           'P':[8, 8,  0, 'PAGE'],
           'O':[0, 8,  0, 'OFFSET'],
           'D':[8, 8,  0, 'DATA'],
          }

###- NATIVE INSTRUCTIONS -###
# Format: '<label>':[<opcode>, '<operand flags in order of use in opcode>', <opcode specific mask>]
# [A=0] means operand A is optional and defaults to 0
# ISA by @SLicudis (GitHub)
OPCODES = {
           'hlt'  :[0x00, '',  0],
           'jmp'  :[0x01, 'A', 0],
           'jz'   :[0x02, 'A', 0],
           'jnz'  :[0x03, 'A', 0],
           'jc'   :[0x04, 'A', 0],
           'jnc'  :[0x05, 'A', 0],
           'jx'   :[0x06, 'P', 0],
           'jy'   :[0x07, 'O', 0],
           'jxy'  :[0x08, '',  0],
           'ldaa' :[0x09, 'A', 0],
           'ldax' :[0x0A, 'P', 0],
           'ldaxy':[0x0B, '',  0],
           'lda'  :[0x0C, 'D', 0],
           'ldxa' :[0x0D, 'A', 0],
           'ldx'  :[0x0E, 'D', 0],
           'ldya' :[0x0F, 'A', 0],
           'ldy'  :[0x10, 'D', 0],
           'atx'  :[0x11, '',  0],
           'aty'  :[0x12, '',  0],
           'xta'  :[0x13, '',  0],
           'xty'  :[0x14, '',  0],
           'yta'  :[0x15, '',  0],
           'ytx'  :[0x16, '',  0],
           'sta'  :[0x17, 'A', 0],
           'stax' :[0x18, 'P', 0],
           'staxy':[0x19, '',  0],
           'stx'  :[0x1A, 'A', 0],
           'sty'  :[0x1B, 'A', 0],
           'inx'  :[0x1C, '',  0],
           'iny'  :[0x1D, '',  0],
           'addi' :[0x1E, 'D', 0],
           'add'  :[0x1F, 'A', 0],
           'addx' :[0x20, '',  0],
           'addy' :[0x21, '',  0],
           'adc'  :[0x22, '',  0],
           'subi' :[0x23, 'D', 0],
           'sub'  :[0x24, 'A', 0],
           'subx' :[0x25, '',  0],
           'suby' :[0x26, '',  0],
           'subc' :[0x27, '',  0],
           'multi':[0x28, 'D', 0],
           'mult' :[0x29, 'A', 0],
           'multx':[0x2A, '',  0],
           'multy':[0x2B, '',  0],
           'neg'  :[0x2C, '',  0],
           'andi' :[0x2D, 'D', 0],
           'and'  :[0x2E, 'A', 0],
           'andx' :[0x2F, '',  0],
           'andy' :[0x30, '',  0],
           'ori'  :[0x31, 'D', 0],
           'or'   :[0x32, 'A', 0],
           'orx'  :[0x33, '',  0],
           'ory'  :[0x34, '',  0],
           'xori' :[0x35, 'D', 0],
           'xor'  :[0x36, 'A', 0],
           'xorx' :[0x37, '',  0],
           'xory' :[0x38, '',  0],
           'shli' :[0x39, 'D', 0],
           'shl'  :[0x3A, 'A', 0],
           'shlx' :[0x3B, '',  0],
           'shly' :[0x3C, '',  0],
           'shri' :[0x3D, 'D', 0],
           'shr'  :[0x3E, 'A', 0],
           'shrx' :[0x3F, '',  0],
           'shry' :[0x40, '',  0],
           'roli' :[0x41, 'D', 0],
           'rol'  :[0x42, 'A', 0],
           'rolx' :[0x43, '',  0],
           'roly' :[0x44, '',  0],
           'rori' :[0x45, 'D', 0],
           'ror'  :[0x46, 'A', 0],
           'rorx' :[0x47, '',  0],
           'rory' :[0x48, '',  0],
           'pha'  :[0x49, '',  0],
           'phx'  :[0x4A, '',  0],
           'phy'  :[0x4B, '',  0],
           'ppa'  :[0x4C, '',  0],
           'ppx'  :[0x4D, '',  0],
           'ppy'  :[0x4E, '',  0],
           'clc'  :[0x4F, '',  0],
           'sec'  :[0x50, '',  0],
           'cli'  :[0x51, '',  0],
           'sei'  :[0x52, '',  0],
           'clz'  :[0x53, '',  0],
           'sez'  :[0x54, '',  0],
           'call' :[0x55, 'A', 0],
           'ret'  :[0x56, '',  0],
           'wait' :[0x57, '',  0],
           'brk'  :[0x58, '',  0],
           'rti'  :[0x59, '',  0],
           'res'  :[0x5A, '',  0],
           'nop'  :[0x69, '',  0],
          } # Opcodes

###- PSEUDO-INSTRUCTIONS -###
# Pseudo-instructions
# Format : 'label':['<resolution as formatted string>']
PSEUDOINS = {
             # To be used
            }

###- MACROS (MULTI-LINE PSEUDO-INSTRUCTIONS) -###
# Macros
# Format : 'label':['<resolution as formatted string>']
# - formatted string must be separated by newlines ('\n')
MACROS = {
          # To be used
         }

###- UTILITY -###
# Definition check
def is_definition(word):
    return word == 'define'
# Label check
def is_label(word):
    return (word[0] == '.') | ((word[-1] == ':') << 1)
# Macro check
def is_macro(word):
    return word in MACROS
# Resolve symbols
def resolve(word, line, symbols):
    if word[0] in '-0123456789':
        return int(word)
    if word[0] == '$':
        return int(word[1:], 16)
    if symbols.get(word) is None:
        fatal_error("assembler", f'{assembly_filename}:{line}: Could not resolve \'{word}\'.')
    return symbols[word]
# Strip line of comments
def remove_comment(comment_symbols, line):
    index=strfind(line, comment_symbols)
    if(index==-1):
        return line
    return line[:index]

###- MAIN THING -###
# Assemble function
def assemble(assembly_filename, output_filename):
    try:
        assembly_file = open(assembly_filename, 'r')
    except FileNotFoundError:
        fatal_error('assembler', f'{assembly_filename}: File not found.')
    machine_code_file = open(output_filename, 'w')
    lines = (line.strip() for line in assembly_file)

    # Remove comments and blanklines
    lines = [[remove_comment("/;#", line).strip(), idx+1] for idx, line in enumerate(lines)]

    # Populate symbol table
    symbols = {}

    # Generate register names
    registers = ['r{0}'.format(x) for x in range(NUMBER_OF_REGISTERS)]
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    # Calculate number of operands and add to pseudo-instruction element
    for pop in PSEUDOINS:
        popcodeinfo=PSEUDOINS[pop]
        nums=[int(word[1:len(word)-1]) for word in popcodeinfo[0].split() if word[0]=='{']
        if(len(nums)==0):
            pseudoins[pop].insert(0, 0)
        else:
            PSEUDOINS[pop].insert(0, max(nums)+1)
    
    # Calculate number of operands and add to macro element
    for macro in MACROS:
        macroinfo=MACROS[macro]
        nums=[int(word[1:len(word)-1]) for word in macroinfo[0].split() if word[0]=='{']
        if(len(nums)==0):
            MACROS[macro].insert(0, 0)
        else:
            MACROS[macro].insert(0, max(nums)+1)
    
    # Make opcodes more machine-friendly
    for opcode in OPCODES:
        processed_opcode=[]
        operands=OPCODES[opcode][1]
        idx=0
        minimum_operands=0
        while(idx<len(operands)):
            if(operands[idx]=='['):
                idx_end=operands.find(']', idx)
                if(idx_end==-1):
                    fatal_error('assembler', f"loading stage: syntax error: No closing brace for operand \'{operands[idx+1]}\' in opcode \'{opcode}\'.")
                substr=operands[idx+1:idx_end]
                if(substr[2:]==''):
                    fatal_error('assembler', f"loading stage: wtf: No default defined for operand \'{substr[0]}\' for opcode \'{opcode}\'.")
                processed_opcode.append([substr[0], int(substr[2:])])
                idx=idx_end+1
                minimum_operands-=1
            else:
                idx_end=operands.find('[', idx)
                if(idx_end==-1):
                    idx_end += len(operands) + 1
                substr=operands[idx:idx_end]
                processed_opcode = processed_opcode + [[x] for x in substr]
                idx=idx_end
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
                fatal_error('assembler', f"loading stage: wtf: Optional operand \'{operands[idx-1][0]}\' declared inbetween necessary ones in \'{opcode}\'! (Will cause problems later)")

    for symbol in OPCODES:
        symbols[symbol] = OPCODES[symbol][0] # Add corresponding numeral opcode

    conditions = [ 'eq'  , 'ne'     , 'ge'   , 'lt'      ,
                   '='   , '!='     , '>='   , '<'       ,
                   'z'   , 'nz'     , 'c'    , 'nc'      ,
                   'zero', 'notzero', 'carry', 'notcarry', ] # Possible conditions
    for index, symbol in enumerate(conditions):
        symbols[symbol] = index & 3 #0b11
    
    # Resolve macros
    cont=True
    while(cont):
        new_lines=lines.copy()
        offset=0
        cont=False
        for index, line in enumerate(lines):
            line_number=line[1]
            line=line[0]
            words = [word.lower() for word in line.split()]
            if(len(words)==0): continue
            if is_macro(words[0]):
                cont=True
                macroinfo=macros[words[0]]
                if macroinfo[0] != (len(words)-1):
                    fatal_error('assembler', f"pre-assembly stage: {assembly_filename}:{line_number}: Incorrect number of operands for macro \'{words[0]}\'")
                gen_lines= macroinfo[1].format(*words[1:]).split('\n')
                new_lines.pop(index + offset)
                offset -= 1
                for gline in gen_lines:
                    offset += 1
                    new_lines.insert(index + offset, [gline, line_number])
        lines=new_lines
    
    # Definitions and labels
    offset = 0
    for index, line in enumerate([line for line in lines if line[0]!='']):
        line_number=line[1]
        line=line[0]
        words = [word.lower() for word in line.split()]

        if is_definition(words[0]):
            symbols[words[1]] = int(words[2])
            offset += 1
        elif is_label(words[0]):
            result = is_label(words[0])
            if(result==1):
                symbols[words[0]] = index - offset
            elif(result==2):
                symbols['.'+words[0][:-1]] = index - offset
            elif(result==3):
                symbols[words[0][:-1]] = index - offset
            else:
                fatal_error('assembler', f"pre-assembly stage: UNKNOWN ERROR: {assembly_filename}:{line_number}: I don\'t know what went wrong. You should open an issue about this!")
            # Compensates for code that is not put in the same line as the label definition
            if(len(words)<2):
                offset+=1
    
    # Clean lines of definitions and labels for machine code translation step
    for i, b in enumerate(lines):
        line_number=b[1]
        b=b[0]
        words = [word.lower() for word in b.split()]
        if(len(words)==0): continue
        if(is_label(words[0])!=0):
            end_of_label=strfind(b, " \t")
            if(end_of_label==-1):
                lines[i]=['', line_number]
            else:
                lines[i]=[b[end_of_label:].strip(), line_number]
        elif(is_definition(words[0])):
            lines[i]=['', line_number]
    lines=[[line[0].strip(), line[1]] for line in lines]

    # Start assembling
    for i in range(len(lines)):
        # Decompose instruction
        line_number=lines[i][1]
        words = [word.lower() for word in split_string(lines[i][0], ", ")]
        if len(words)==0: continue
        
        # Resolve pseudo-instructions
        if words[0] in PSEUDOINS:
            popcode     = words[0]
            popcodeinfo = PSEUDOINS[popcode]
            if popcodeinfo[0] != len(words)-1:
                fatal_error("assembler", f"{assembly_filename}:{line_number}: Incorrect number of operands for pseudo-instruction \'{popcode}\'")
            words=popcodeinfo[1].format(*words[1:]).split()
        
        # Begin machine code translation
        current_opcode = words[0]
        # Resolve opcode
        machine_code = 0
        try:
            machine_code |= symbols[current_opcode] << OPCODE_POSITION
        except KeyError:
            fatal_error("assembler", f'{assembly_filename}:{line_number}: Unknown opcode \'{current_opcode}\'')
        # Resolve operands
        words = [resolve(word, line_number, symbols) for word in words]

        # Number of operands check
        if(  OPCODES[current_opcode][1][-2] > (len(words)-1)):
            fatal_error("assembler", f'{assembly_filename}:{line_number}: Not enough operands for \'{current_opcode}\'')
        elif(OPCODES[current_opcode][1][-1] < (len(words)-1)):
            fatal_error("assembler", f'{assembly_filename}:{line_number}: Too many operands for \'{current_opcode}\'')

        # Check operands and assemble instruction
        for idx, opcode in enumerate(OPCODES[current_opcode][1][0]):
            if((len(words)-2)<idx):
                words.append(opcode[1])
            opinfo = OPERANDS[opcode[0]]
            mask   = (1<<opinfo[1]) - 1
            if opinfo[2] and (words[idx+1]<0):
                words[idx+1]=(~words[idx+1])+1
            if words[idx+1] != (words[idx+1] & mask):
                fatal_error("assembler", f'{assembly_filename}:{line_number}: Invalid {opinfo[3]} for \'{current_opcode}\'')
            machine_code |= (words[idx+1] & mask) << opinfo[0] # Just to be safe, it's ANDed with the mask

        # OR with opcode-specific mask
        machine_code |= OPCODES[current_opcode][2]

        # Write to output file
        as_string = bin(machine_code)[2:].rjust(INSTRUCTION_MAX_LENGTH, '0')
        machine_code_file.write(f'{as_string}\n')
