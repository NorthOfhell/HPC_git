/******************************************************************************
* FILE: mm.c
* DESCRIPTION:  
*   This program calculates the product of matrix a[nra][nca] and b[nca][ncb],
*   the result is stored in matrix c[nra][ncb].
*   The max dimension of the matrix is constraint with static array declaration,
*   for a larger matrix you may consider dynamic allocation of the arrays, 
*   but it makes a parallel code much more complicated (think of communication),
*   so this is only optional.
*   
******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
// #define NRA 1000                 /* number of rows in matrix A */
// #define NCA 1000                 /* number of columns in matrix A */
// #define NCB 1000                  /* number of columns in matrix B */
#define N 1000

int main (int argc, char *argv[]) 
{
MPI_Init(&argc, &argv);
double start_time = MPI_Wtime();
int     tid, nthreads, i, j, k;
/* for simplicity, set NRA=NCA=NCB=N  */
int NRA=N;
int NCA=N;
int NCB=N;



// Allocate a
double **a = malloc(NRA * sizeof(double*));
for (int i = 0; i < NRA; i++) a[i] = malloc(NCA * sizeof(double));

// Allocate b
double **b = malloc(NCA * sizeof(double*));
for (int i = 0; i < NCA; i++) b[i] = malloc(NCB * sizeof(double));

// Allocate c
double **c = malloc(NRA * sizeof(double*));
for (int i = 0; i < NRA; i++) c[i] = malloc(NCB * sizeof(double));

  /*** Initialize matrices ***/
  
  for (i=0; i<NRA; i++)
    for (j=0; j<NCA; j++)
      a[i][j]= i+j;
  
  for (i=0; i<NCA; i++)
    for (j=0; j<NCB; j++)
      b[i][j]= i*j;
  
  for (i=0; i<NRA; i++)
    for (j=0; j<NCB; j++)
      c[i][j]= 0;

  /* Parallelize the computation of the following matrix-matrix multiplication. 
     How to partition and distribute the initial matrices, the work, and collecting
     final results.
  */
double t0  = MPI_Wtime();
  for (i=0; i<NRA; i++)    
    for(j=0; j<NCB; j++)       
      for (k=0; k<NCA; k++)
        c[i][j] += a[i][k] * b[k][j];

        
double t1 = MPI_Wtime();
/*  perform time measurement. Always check the correctness of the parallel results
    by printing a few values of c[i][j] and compare with the sequential output.
*/
for (int i = 0; i < NRA; i++) free(a[i]);
free(a);
for (int i = 0; i < NCA; i++) free(b[i]);
free(b);
for (int i = 0; i < NRA; i++) free(c[i]);
free(c);

printf("calculation time: %f, total time is: %f\n",t1 - t0, MPI_Wtime() - start_time);
MPI_Finalize();
    return 0; 
}
 
