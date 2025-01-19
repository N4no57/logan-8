.org $0000

start_label:
    ; setup for the unittest. instruction already tested by previous test
    mw #$17, r1
    ; actual instruction
    sw ($1000), r1
    ; end unittest
    hlt
