.fill $0FFF, $00

.equ start, $1000
.org start

start_label:
    hlt

.byte $01, $02, $03
.word $1234, $5678

.fill $FFFF, $00