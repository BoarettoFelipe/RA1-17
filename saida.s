.data
    .align 3

    @ === CONSTANTES NUMÉRICAS (IEEE 754, 64 bits) ===
    const_0:  .word 0x00000000, 0x40140000    @ 5.0
    const_1:  .word 0x00000000, 0x40080000    @ 3.0
    const_2:  .word 0x00000000, 0x40250000    @ 10.5
    const_3:  .word 0x00000000, 0x40000000    @ 2.0
    const_4:  .word 0x00000000, 0x40340000    @ 20.0
    const_5:  .word 0x00000000, 0x40100000    @ 4.0
    const_6:  .word 0x00000000, 0x40240000    @ 10.0
    const_7:  .word 0x00000000, 0x402E0000    @ 15.0
    const_8:  .word 0x51EB851F, 0x40091EB8    @ 3.14
    const_9:  .word 0x00000000, 0x40590000    @ 100.0
    const_um:  .word 0x00000000, 0x3FF00000    @ 1.0
    const_zero:  .word 0x00000000, 0x00000000    @ 0.0

    @ === VARIÁVEIS DE MEMÓRIA ===
    var_MEM:  .word 0x00000000, 0x00000000    @ variável MEM

    @ === HISTÓRICO DE RESULTADOS (para comando RES) ===
    hist_0:  .word 0x00000000, 0x00000000    @ resultado linha 0
    hist_1:  .word 0x00000000, 0x00000000    @ resultado linha 1
    hist_2:  .word 0x00000000, 0x00000000    @ resultado linha 2
    hist_3:  .word 0x00000000, 0x00000000    @ resultado linha 3
    hist_4:  .word 0x00000000, 0x00000000    @ resultado linha 4
    hist_5:  .word 0x00000000, 0x00000000    @ resultado linha 5
    hist_6:  .word 0x00000000, 0x00000000    @ resultado linha 6
    hist_7:  .word 0x00000000, 0x00000000    @ resultado linha 7
    hist_8:  .word 0x00000000, 0x00000000    @ resultado linha 8
    hist_9:  .word 0x00000000, 0x00000000    @ resultado linha 9

    @ === RESULTADOS FINAIS ===
    res_0:  .word 0x00000000, 0x00000000    @ resultado linha 0
    res_1:  .word 0x00000000, 0x00000000    @ resultado linha 1
    res_2:  .word 0x00000000, 0x00000000    @ resultado linha 2
    res_3:  .word 0x00000000, 0x00000000    @ resultado linha 3
    res_4:  .word 0x00000000, 0x00000000    @ resultado linha 4
    res_5:  .word 0x00000000, 0x00000000    @ resultado linha 5
    res_6:  .word 0x00000000, 0x00000000    @ resultado linha 6
    res_7:  .word 0x00000000, 0x00000000    @ resultado linha 7
    res_8:  .word 0x00000000, 0x00000000    @ resultado linha 8
    res_9:  .word 0x00000000, 0x00000000    @ resultado linha 9

    @ === CONTROLE DE ERROS ===
    total_linhas:  .word 10    @ total de linhas no programa
    error_flag:    .word 0               @ 0=ok, 1=erro RES fora do limite


.text
.global _start

@ === SUB-ROTINA: Potenciação (d0 ^ d1) ===
@ d0 = base, d1 = expoente inteiro positivo
@ Resultado em d0
sub_pot:
    PUSH {r0, r1, lr}
    VCVT.S32.F64 s4, d1
    VMOV r1, s4
    LDR r0, =const_um
    VLDR d2, [r0]
    CMP r1, #0
    BLE sub_pot_fim
sub_pot_loop:
    VMUL.F64 d2, d2, d0
    SUBS r1, r1, #1
    BNE sub_pot_loop
sub_pot_fim:
    VMOV.F64 d0, d2
    POP {r0, r1, lr}
    BX lr

@ === SUB-ROTINA: Divisão Inteira (d0 // d1) ===
@ Usa VFP: divide como double, trunca para int, volta para double
@ Resultado em d0
sub_div_int:
    PUSH {lr}
    VDIV.F64 d0, d0, d1        @ d0 = a / b (double)
    VCVT.S32.F64 s4, d0        @ s4 = truncar para inteiro
    VCVT.F64.S32 d0, s4        @ d0 = inteiro como double
    POP {lr}
    BX lr

@ === SUB-ROTINA: Resto da Divisão (d0 % d1) ===
@ Usa VFP: resto = a - trunc(a/b) * b
@ Resultado em d0
sub_mod:
    PUSH {lr}
    VMOV.F64 d2, d0             @ d2 = a (backup)
    VDIV.F64 d3, d0, d1         @ d3 = a / b
    VCVT.S32.F64 s4, d3         @ s4 = trunc(a / b)
    VCVT.F64.S32 d3, s4         @ d3 = trunc como double
    VMUL.F64 d3, d3, d1         @ d3 = trunc(a/b) * b
    VSUB.F64 d0, d2, d3         @ d0 = a - trunc(a/b)*b = resto
    POP {lr}
    BX lr

@ === PROGRAMA PRINCIPAL ===
_start:

    @ --- Linha 0: ( 5 3 + ) ---
    LDR r0, =const_0
    VLDR d0, [r0]             @ d0 = 5
    VPUSH {d0}               @ empilha 5
    LDR r0, =const_1
    VLDR d0, [r0]             @ d0 = 3
    VPUSH {d0}               @ empilha 3
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VADD.F64 d0, d0, d1       @ d0 = a + b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 0
    LDR r0, =hist_0
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_0
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 1: ( 10.5 2 * ) ---
    LDR r0, =const_2
    VLDR d0, [r0]             @ d0 = 10.5
    VPUSH {d0}               @ empilha 10.5
    LDR r0, =const_3
    VLDR d0, [r0]             @ d0 = 2
    VPUSH {d0}               @ empilha 2
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VMUL.F64 d0, d0, d1       @ d0 = a * b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 1
    LDR r0, =hist_1
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_1
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 2: ( 20 4 / ) ---
    LDR r0, =const_4
    VLDR d0, [r0]             @ d0 = 20
    VPUSH {d0}               @ empilha 20
    LDR r0, =const_5
    VLDR d0, [r0]             @ d0 = 4
    VPUSH {d0}               @ empilha 4
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VDIV.F64 d0, d0, d1       @ d0 = a / b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 2
    LDR r0, =hist_2
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_2
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 3: ( 10 3 // ) ---
    LDR r0, =const_6
    VLDR d0, [r0]             @ d0 = 10
    VPUSH {d0}               @ empilha 10
    LDR r0, =const_1
    VLDR d0, [r0]             @ d0 = 3
    VPUSH {d0}               @ empilha 3
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    BL sub_div_int             @ d0 = a // b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 3
    LDR r0, =hist_3
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_3
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 4: ( 2 3 ^ ) ---
    LDR r0, =const_3
    VLDR d0, [r0]             @ d0 = 2
    VPUSH {d0}               @ empilha 2
    LDR r0, =const_1
    VLDR d0, [r0]             @ d0 = 3
    VPUSH {d0}               @ empilha 3
    VPOP {d1}                @ expoente
    VPOP {d0}                @ base
    BL sub_pot                 @ d0 = base ^ exp
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 4
    LDR r0, =hist_4
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_4
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 5: ( 15 4 % ) ---
    LDR r0, =const_7
    VLDR d0, [r0]             @ d0 = 15
    VPUSH {d0}               @ empilha 15
    LDR r0, =const_5
    VLDR d0, [r0]             @ d0 = 4
    VPUSH {d0}               @ empilha 4
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    BL sub_mod                 @ d0 = a %% b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 5
    LDR r0, =hist_5
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_5
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 6: ( 10 MEM ) ---
    LDR r0, =const_6
    VLDR d0, [r0]             @ d0 = 10
    VPUSH {d0}               @ empilha 10
    VPOP {d0}                @ valor a armazenar
    LDR r0, =var_MEM
    VSTR d0, [r0]             @ MEM = d0
    VPUSH {d0}               @ re-empilha
    VPOP {d0}                @ resultado linha 6
    LDR r0, =hist_6
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_6
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 7: ( 0 RES 5 + ) ---
    LDR r0, =const_zero
    VLDR d0, [r0]             @ d0 = 0
    VPUSH {d0}               @ empilha 0
    VPOP {d0}                @ N = linhas atrás
    VCVT.S32.F64 s4, d0
    VMOV r1, s4                @ r1 = N
    MOV r2, #7
    SUB r2, r2, #1
    SUB r2, r2, r1             @ r2 = índice no histórico
    CMP r2, #0
    BLT _error                 @ índice negativo → erro
    CMP r2, #7
    BGE _error                 @ índice >= linha atual → erro
    LDR r0, =hist_0
    ADD r0, r0, r2, LSL #3    @ r0 = &hist_0 + idx*8
    VLDR d0, [r0]             @ d0 = resultado referenciado
    VPUSH {d0}               @ empilha valor do RES
    LDR r0, =const_0
    VLDR d0, [r0]             @ d0 = 5
    VPUSH {d0}               @ empilha 5
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VADD.F64 d0, d0, d1       @ d0 = a + b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 7
    LDR r0, =hist_7
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_7
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 8: ( 3.14 2.0 * ) ---
    LDR r0, =const_8
    VLDR d0, [r0]             @ d0 = 3.14
    VPUSH {d0}               @ empilha 3.14
    LDR r0, =const_3
    VLDR d0, [r0]             @ d0 = 2.0
    VPUSH {d0}               @ empilha 2.0
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VMUL.F64 d0, d0, d1       @ d0 = a * b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 8
    LDR r0, =hist_8
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_8
    VSTR d0, [r0]             @ salva em resultados

    @ --- Linha 9: ( 100 10 / ) ---
    LDR r0, =const_9
    VLDR d0, [r0]             @ d0 = 100
    VPUSH {d0}               @ empilha 100
    LDR r0, =const_6
    VLDR d0, [r0]             @ d0 = 10
    VPUSH {d0}               @ empilha 10
    VPOP {d1}                @ b = topo
    VPOP {d0}                @ a = abaixo
    VDIV.F64 d0, d0, d1       @ d0 = a / b
    VPUSH {d0}               @ empilha resultado
    VPOP {d0}                @ resultado linha 9
    LDR r0, =hist_9
    VSTR d0, [r0]             @ salva no histórico
    LDR r0, =res_9
    VSTR d0, [r0]             @ salva em resultados

    @ === TRATAMENTO DE ERRO ===
    @ Se RES apontar para índice inválido, cai aqui
_error:
    LDR r0, =error_flag
    MOV r1, #1
    STR r1, [r0]               @ error_flag = 1

    @ === FIM ===
    @ Resultados em res_0 a res_N na memória
    @ Se error_flag = 1, houve erro de RES
_end:
    B _end
