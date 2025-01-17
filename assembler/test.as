.org $0000

start_label:
    ; setup for the unittest. instruction already tested by previous test
    mw #$41, r1
    ; actual instruction
    mw r1, r3
    ; end unittest
    hlt
