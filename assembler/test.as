.equ start, $0000
.equ write_location, $1007
.org start

start_label:
    mw #$13, r1
    mw r1, r2
    lw $1000, r5
    sw $1007, r5
    jmp jump_to
jump_back:
    hlt

.fill $0FFF, $00

.org $0500

jump_to:
    mw #$F0, r15
    sw write_location, r15
    jmp jump_back

.org $1000

.byte $01, $02, $03
.word $1234, $5678
.fill $FFFF, $00