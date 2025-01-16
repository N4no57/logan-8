.equ start, $0000
.org start

start_label:
    mw #$13, r1
    mw r1, r2
    lw $1000, r5
    sw $1007, r5
    hlt

.fill $0FFF, $00

.org $1000

.byte $01, $02, $03
.word $1234, $5678
.fill $FFFF, $00