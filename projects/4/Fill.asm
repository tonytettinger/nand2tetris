// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
@SCREEN
D=A
@screen_position
M=D

@8192
D=A

@max
M=D

@i
M=0

// Check keyboard

(CHECK_KBD)
@i
M=0
@KBD
D=M
@BLACK_LOOP
D; JNE

@WHITE_LOOP
0; JMP

(BLACK_LOOP)
@screen_position
D=M

@i
D=M

@screen_position
A=D+M
M=-1

@i
M=M+1
D=M
@max
D=D-M

@CHECK_KBD
D; JGE

@BLACK_LOOP
0; JMP


(WHITE_LOOP)
@screen_position
D=M

@i
D=M

@screen_position
A=D+M
M=0

@i
M=M+1
D=M
@max
D=D-M
@CHECK_KBD
D; JGE

@WHITE_LOOP
0; JMP

(STOP)
@STOP
0; JMP