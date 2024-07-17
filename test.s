; multiplication procedure
.Multiply:
  mvi %AX, 0
.mloop:
  cmp %CX, %ZX
  jz [.ret]
  and %CX, %ZX, $0001
  jz [.nadd]
  add %AX, %BX, %AX
.nadd:
  shl %BX, %BX
  shr %CX, %CX
  jmp [.mloop]
.ret:
  jmp [.ret]
ORG reset_vector
  jmp [.Multiply]
