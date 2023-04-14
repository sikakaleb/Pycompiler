;------------------------------------------
; void readline
; Read a line from stdin, store string after [$eax]
; WARNING: does not check for buffer overflow - insecure!
readline:    
    push    edx        ; preserve edx on stack to be restored after function
    push    ecx        ; preserve ecx on stack to be restored after function
    push    ebx        ; preserve ebx on stack to be restored after function
    push    eax        ; preserve eax on stack to be restored after function
    mov ecx, eax       ; address where store result
continue_reading:
    mov	eax, 3         ; syscall is read = 3
    mov	ebx, 0         ; fd is stdin = 0    
    mov	edx, 1         ; nb. of bytes to read
    int 80h            ; call interruption
    cmp eax, 0         ; if no byte read, then we reached EOF, stop
    je end_reading    
    cmp BYTE [ecx], 10 ; Found '\n', stop reading string
    je end_reading
    cmp BYTE [ecx], 13 ; Found '\r', stop reading string
    je end_reading
    inc ecx            ; None of above, increment pointer and read next byte
    jmp continue_reading
end_reading:
    mov BYTE [ecx], 0  ; Add zero to yield null-terminated string
    pop     eax        ; restore eax from value pushed onto stack at start
    pop     ebx        ; restore eax from value pushed onto stack at start
    pop     ecx        ; restore eax from value pushed onto stack at start
    pop     edx        ; restore eax from value pushed onto stack at start
    ret

;------------------------------------------
; void iprint(Integer number)
; Integer printing function (itoa)
iprint:
    push    eax             ; preserve eax on the stack to be restored after function runs
    push    ecx             ; preserve ecx on the stack to be restored after function runs
    push    edx             ; preserve edx on the stack to be restored after function runs
    push    esi             ; preserve esi on the stack to be restored after function runs
    
    cmp	    eax, 0
    jge      positive
    push    eax             ; preserve eax value
    mov     ebx, '-'
    push    ebx
    mov     eax, esp    
    call sprint
    pop     eax             ; remove '-' sign
    pop     eax             ; retrieve eax value
    neg     eax
positive:
    mov     ecx, 0          ; counter of how many bytes we need to print in the end 
divideLoop:
    inc     ecx             ; count each byte to print - number of characters
    mov     edx, 0          ; empty edx
    mov     esi, 10         ; mov 10 into esi
    idiv    esi             ; divide eax by esi
    add     edx, 48         ; convert edx to it's ascii representation - edx holds the remainder after a divide instruction
    push    edx             ; push edx (string representation of an intger) onto the stack
    cmp     eax, 0          ; can the integer be divided anymore?
    jnz     divideLoop      ; jump if not zero to the label divideLoop
 
printLoop:
    dec     ecx             ; count down each byte that we put on the stack
    mov     eax, esp        ; mov the stack pointer into eax for printing
    call    sprint          ; call our string print function
    pop     eax             ; remove last character from the stack to move esp forward
    cmp     ecx, 0          ; have we printed all bytes we pushed onto the stack?
    jnz     printLoop       ; jump is not zero to the label printLoop
 
    pop     esi             ; restore esi from the value we pushed onto the stack at the start
    pop     edx             ; restore edx from the value we pushed onto the stack at the start
    pop     ecx             ; restore ecx from the value we pushed onto the stack at the start
    pop     eax             ; restore eax from the value we pushed onto the stack at the start
    ret
 
 
;------------------------------------------
; void iprintLF(Integer number)
; Integer printing function with linefeed (itoa)
iprintLF:
    call    iprint          ; call our integer printing function
 
    push    eax             ; push eax onto the stack to preserve it while we use the eax register in this function
    mov     eax, 0Ah        ; move 0Ah into eax - 0Ah is the ascii character for a linefeed
    push    eax             ; push the linefeed onto the stack so we can get the address
    mov     eax, esp        ; move the address of the current stack pointer into eax for sprint
    call    sprint          ; call our sprint function
    pop     eax             ; remove our linefeed character from the stack
    pop     eax             ; restore the original value of eax before our function was called
    ret
 
 
;------------------------------------------
; int slen(String message)
; String length calculation function
slen:
    push    ebx
    mov     ebx, eax
 
nextchar:
    cmp     byte [eax], 0
    jz      finished
    inc     eax
    jmp     nextchar
 
finished:
    sub     eax, ebx
    pop     ebx
    ret
 
 
;------------------------------------------
; void sprint(String message)
; String printing function
sprint:
    push    edx
    push    ecx
    push    ebx
    push    eax
    call    slen
 
    mov     edx, eax
    pop     eax
 
    mov     ecx, eax
    mov     ebx, 1
    mov     eax, 4
    int     80h
 
    pop     ebx
    pop     ecx
    pop     edx
    ret
 
 
;------------------------------------------
; void sprintLF(String message)
; String printing with line feed function
sprintLF:
    call    sprint
 
    push    eax
    mov     eax, 0AH
    push    eax
    mov     eax, esp
    call    sprint
    pop     eax
    pop     eax
    ret
 
 
;------------------------------------------
; void exit()
; Exit program and restore resources
quit:
    mov     ebx, 0
    mov     eax, 1
    int     80h
    ret

;------------------------------------------
; int atoi(Integer number)
; Ascii to integer function (atoi)
atoi:
    push    ebx             ; preserve ebx on the stack to be restored after function runs
    push    ecx             ; preserve ecx on the stack to be restored after function runs
    push    edx             ; preserve edx on the stack to be restored after function runs
    push    esi             ; preserve esi on the stack to be restored after function runs
    xor     ebx, ebx        ; initialize forming answer
    xor     ecx, ecx        ; initialize sign flag
    mov     esi, eax
atoi1: 
    lodsb                   ; scan off whitespace
    cmp     al, ' '         ; ignore leading blanks
    je atoi1
    cmp al, '+'             ; if + sign proceed
    je atoi2
    cmp al, '-'             ; is it - sign?
    jne atoi3               ; no, test if numeric
    dec ecx                 ; was - sign, set flag for negative result
atoi2: 
    lodsb                   ; get next character
atoi3: 
    cmp al,'0'        ; is character valid?
    jb atoi4          ; jump if not '0' to '9'
    cmp al,'9'
    ja atoi4          ; jump if not '0' to '9'
    and eax, 000fh     ; isolate lower four bits
    xchg ebx, eax      ; multiply answer x 10
    mov edx, 10
    mul edx
    add ebx, eax      ; add this digit
    jmp atoi2         ; convert next digit
atoi4: 
    mov eax,ebx ; result into AX
    jcxz atoi5 ; jump if sign flag clear
    neg eax ; make result negative
atoi5:
    pop     esi             ; restore esi from the value we pushed onto the stack at the start
    pop     edx             ; restore edx from the value we pushed onto the stack at the start
    pop     ecx             ; restore ecx from the value we pushed onto the stack at the start
    pop     ebx             ; restore ebx from the value we pushed onto the stack at the start
    ret
