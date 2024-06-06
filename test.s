; test
.Setup:
  LDA $FF
.Loop:
  ADDI $01
  STA $FE01
  JNZ .Loop
  HLT
