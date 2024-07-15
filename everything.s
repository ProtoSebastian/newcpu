; native-instructions
  NOP 
  BRK 
  ALU 1, %r2, %r2, %r2
  ALUI 1, %r2, %r2, 1
  LDI %r2, 1
  LOD %r2, [%r1, $20]
  LOD %r2, [%r1, %r3]
  STR %r2, [%r1, $20]
  STR %r2, [%r1, %r3]
  PSH %r2
  POP %r2
  JMP [$1000]
  JF 1, [$1000]
  RJM [%r1, %r2]
  CALL [$1000]
  RET 
  WAIT 
  STA [$1000]
  LDA [$1000]
; pseudo-instructions
  MOV %r2, %r2
  MOV %r2, 1
  INC %r2
  DEC %r2
  CMP %r2, %r2
  CMP %r2, 1
  SHL %r2, %r2
  ADD %r2, %r2, %r2
  ADD %r2, %r2, 1
  ADDC %r2, %r2, %r2
  ADDC %r2, %r2, 1
  SUB %r2, %r2, %r2
  SUB %r2, %r2, 1
  SUBB %r2, %r2, %r2
  SUBB %r2, %r2, 1
  MULT %r2, %r2, %r2
  MULT %r2, %r2, 1
  AND %r2, %r2, %r2
  AND %r2, %r2, 1
  OR %r2, %r2, %r2
  OR %r2, %r2, 1
  XOR %r2, %r2, %r2
  XOR %r2, %r2, 1
  NAND %r2, %r2, %r2
  NAND %r2, %r2, 1
  NOR %r2, %r2, %r2
  NOR %r2, %r2, 1
  XNOR %r2, %r2, %r2
  XNOR %r2, %r2, 1
  SHR %r2, %r2
  ASR %r2, %r2
  ROL %r2, %r2
  ROR %r2, %r2
  SHRC %r2, %r2
  NEG %r2, %r2 
  NOT %r2, %r2 
  JZ [$1000]
  JC [$1000]
  JO [$1000]
  JS [$1000]
  JGT [$1000]
  JLT [$1000]
  JB [$1000]
  JIRQE [$1000]
  JNZ [$1000]
  JNC [$1000]
  JNO [$1000]
  JNS [$1000]
  JNGT [$1000]
  JNLT [$1000]
  JNB [$1000]
  JNIRQE [$1000]
