// Transliteration into GNU C (manually)
// It doesn't crash but I'm pretty sure it will crash when it has to exit.
// Moving on...

#include <stdio.h>

int main(void) {
  int r0,r1,r2,r3,r4,r5;
  r0 = 1;
  r1 = r2 = r3 = r4 = r5 = 0;

  void *pc = &&zero_lbl;
  
 zero_lbl:
  r4 += 16;              // addi 4 16 4
  r4++;
  goto *(pc + r4);  
  r3 = 1;                // seti 1 3 3
  r4++;
  r2 = 1;                // seti 1 4 2
  r4++;
  r1 = r3 * r2;          // mulr 3 2 1
  r4++;
  r1 = r1 == r5 ? 1 : 0; // eqrr 1 5 1
  r4++;
  r4 += r1;              // addr 1 4 4
  r4++;
  goto *(pc + r4);
  r4 += 1;               // addi 4 1 4
  r4++;
  goto *(pc + r4);
  r0 += r3;              // addr 3 0 0
  r4++;
  r2 += 1;               // addi 2 1 2
  r4++;
  r1 = r2 > r5 ? 1 : 0;  // gtrr 2 5 1
  r4++;
  r4 += r1;              // addr 4 1 4
  r4++;
  goto *(pc + r4);
  r4 = 2;                // seti 2 2 4
  r4++;
  goto *(pc + r4);
  r3 += 1;               // addi 3 1 3
  r4++;
  r1 = r3 > r5 ? 1 : 0;  // gtrr 3 5 1
  r4++;
  r4 += r1;              // addr 1 4 4
  r4++;
  goto *(pc + r4);
  r4 = 1;                // seti 1 6 4
  r4++;
  goto *(pc + r4);
  r4 *= r4;              // mulr 4 4 4
  r4++;
  goto *(pc + r4);
  r5 += 2;               // addi 5 2 5
  r4++;
  r5 *= r5;              // mulr 5 5 5
  r4++;
  r5 *= r4;              // mulr 4 5 5
  r4++;
  r5 *= 11;              // muli 5 11 5
  r4++;
  r1 += 4;               // addi 1 4 1
  r4++;
  r1 *= r4;              // mulr 1 4 1
  r4++;
  r1 += 15;              // addi 1 15 1
  r4++;
  r5 += r1;              // addr 5 1 5
  r4++;
  r4 += r0;              // addr 4 0 4
  r4++;
  goto *(pc + r4);
  r4 = 0;                // seti 0 9 4
  r4++;
  goto *(pc + r4);
  r1 = 4;                // setr 4 2 1
  r4++;
  goto *(pc + r4);
  r1 += r4;              // mulr 1 4 1
  r4++;
  r1 += r4;              // addr 4 1 1
  r4++;
  r1 *= r4;              // mulr 4 1 1
  r4++;
  r1 += 14;              // muli 1 14 1
  r4++;
  r1 *= r4;              // mulr 1 4 1
  r4++;
  r5 += r1;              // addr 5 1 5
  r4++;
  r0 = 0;                // seti 0 8 0
  r4++;
  r4 = 0;                // seti 0 4 4
  r4++;
  goto *(pc + r4);

 end:
  printf("%d\n", r0);
  return 0;
}
