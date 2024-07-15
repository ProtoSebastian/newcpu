; display 'Hello, World!' when '1' is input
DEFINE TERMINAL, $8000
DEFINE KEYBOARD, $8001

ORG $0000
  JMP  [.START]
  JMP  [.INT]
START:
  LDI   %SPX, .STRING[0]
  LDI   %SPY, .STRING[1]
  LDI   %CSY, $40
  LDI   %SR,  $80
  WAIT
INT:
  LDA  [KEYBOARD]
  CMP   %RA, '1'
  JNZ  [.START]
  CALL [.PRINT_CHAR, +$1]
  JMP  [.START]
PRINT_CHAR:
  LDI   %SPX, $00
NOT_NULL_CHAR:
  POP   %RA
  STA  [TERMINAL]
  CMP   %RA,  %R0
  JNZ  [.NOT_NULL_CHAR]
  RET
ORG $0200
STRING:
DB "Hello World!", 10, $00
