// Get rid of r4 entirely. We don't need to keep track of its value, it's always the 0 based instruction index.
// Replace instructions that operate on r4 for jmp or rjmp

#include <stdio.h>

int main(void) {
  int r0,r1,r2,r3,r5;
  r0 = 1;
  r1 = r2 = r3 = r5 = 0;
  
  goto lbl17;            // 00 rjmp 16
 lbl1:
  r3 = 1;                // 01 seti 1 3 3
 lbl2:
  r2 = 1;                // 02 seti 1 4 2
 lbl3:
  r1 = r3 * r2;          // 03 mulr 3 2 1
  r1 = r1 == r5 ? 1 : 0; // 04 eqrr 1 5 1
  //goto ???             // 05 rjmp r1
  goto lbl08;            // 06 rjmp 1
  r0 += r3;              // 07 addr 3 0 0
 lbl08:
  r2 += 1;               // 08 addi 2 1 2
  r1 = r2 > r5 ? 1 : 0;  // 09 gtrr 2 5 1
  //goto ???             // 10 rjmp r1
  goto lbl3;             // 11 jmp 2
  r3 += 1;               // 12 addi 3 1 3
  r1 = r3 > r5 ? 1 : 0;  // 13 gtrr 3 5 1
  //goto ???             // 14 rjmp r1
  goto lbl2;             // 15 jmp 1
  //goto ???             // 16 rjmp r4*r4
 lbl17:
  r5 += 2;               // 17 addi 5 2 5
  r5 *= r5;              // 18 mulr 5 5 5
  r5 *= 19;              // 19 mulr 4 5 5
  r5 *= 11;              // 20 muli 5 11 5
  r1 += 4;               // 21 addi 1 4 1
  r1 *= 22;              // 22 mulr 1 4 1
  r1 += 15;              // 23 addi 1 15 1
  r5 += r1;              // 25 addr 5 1 5
  //goto ???             // 26 rjmp r0
  goto lbl1;             // 27 jmp 0
  r1 = 4;                // 28 setr 4 2 1
  r1 *= 29;              // 29 mulr 1 4 1
  r1 += 30;              // 30 addr 4 1 1
  r1 *= 31;              // 31 mulr 4 1 1
  r1 *= 14;              // 32 muli 1 14 1
  r1 *= 33;              // 33 mulr 1 4 1
  r5 += r1;              // 34 addr 5 1 5
  r0 = 0;                // 35 seti 0 8 0
  goto lbl1;             // 36 jmp 0

 end:
  printf("%d\n", r0);
  return 0;
}
