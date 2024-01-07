10 PRINT TAB(33);"BATNUM"
20 PRINT TAB(15);"CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"
30 PRINT:PRINT:PRINT
110 PRINT "THIS PROGRAM IS A 'BATTLE OF NUMBERS' GAME, WHERE THE"
120 PRINT "COMPUTER IS YOUR OPPONENT."
130 PRINT 
140 PRINT "THE GAME STARTS WITH AN ASSUMED PILE OF OBJECTS. YOU"
150 PRINT "AND YOUR OPPONENT ALTERNATELY REMOVE OBJECTS FROM THE PILE."
160 PRINT "WINNING IS DEFINED IN ADVANCE AS TAKING THE LAST OBJECT OR"
170 PRINT "NOT. YOU CAN ALSO SPECIFY SOME OTHER BEGINNING CONDITIONS."
180 PRINT "DON'T USE ZERO, HOWEVER, IN PLAYING THE GAME."
190 PRINT "ENTER A NEGATIVE NUMBER FOR NEW PILE SIZE TO STOP PLAYING."
200 PRINT
210 GOTO 330
220 FOR I=1 TO 10
230 PRINT
240 NEXT I
330 INPUT "ENTER PILE SIZE";N
350 IF N>=1 THEN 370
360 GOTO 330
370 IF N<>INT(N) THEN 220
380 IF N<1 THEN 220
390 INPUT "ENTER WIN OPTION - 1 TO TAKE LAST, 2 TO AVOID LAST: ";M
410 IF M=1 THEN 430
420 IF M<>2 THEN 390
430 INPUT "ENTER MIN AND MAX ";A,B
450 IF A>B THEN 430
460 IF A<1 THEN 430
470 IF A<>INT(A) THEN 430
480 IF B<>INT(B) THEN 430
490 INPUT "ENTER START OPTION - 1 COMPUTER FIRST, 2 YOU FIRST ";S
500 PRINT:PRINT
510 IF S=1 THEN 530
520 IF S<>2 THEN 490
530 C=A+B
540 IF S=2 THEN 570
550 GOSUB 600
560 IF W=1 THEN 220
570 GOSUB 810
580 IF W=1 THEN 220
590 GOTO 550
600 Q=N
610 IF M=1 THEN 630
620 Q=Q-1
630 IF M=1 THEN 680
640 IF N>A THEN 720
650 W=1
660 PRINT "COMPUTER TAKES ";N;" AND LOSES."
670 RETURN
680 IF N>B THEN 720
690 W=1
700 PRINT "COMPUTER TAKES ";N;" AND WINS."
710 RETURN
720 P=Q-C*INT(Q/C)
730 IF P>=A THEN 750
740 P=A
750 IF P<=B THEN 770
760 P=B
770 N=N-P
780 PRINT "COMPUTER TAKES ";P;" AND LEAVES ";N
790 W=0
800 RETURN
810 PRINT:PRINT "YOUR MOVE ";
820 INPUT P
830 IF P<>0 THEN 870
840 PRINT "I TOLD YOU NOT TO USE ZERO! COMPUTER WINS BY FORFEIT."
850 W=1
860 RETURN
870 IF P<>INT(P) THEN 920
880 IF P>=A THEN 910
890 IF P=N THEN 960
900 GOTO 920
910 IF P<=B THEN 940
920 PRINT "ILLEGAL MOVE, REENTER IT ";
930 GOTO 820
940 N=N-P
950 IF N<>0 THEN 1030
960 IF M=1 THEN 1000
970 PRINT "TOUGH LUCK, YOU LOSE."
980 W=1
990 RETURN
1000 PRINT "CONGRATULATIONS, YOU WIN."
1010 W=1
1020 RETURN
1030 IF N>=0 THEN 1060
1040 N=N+P
1050 GOTO 920
1060 W=0
1070 RETURN
1080 END
