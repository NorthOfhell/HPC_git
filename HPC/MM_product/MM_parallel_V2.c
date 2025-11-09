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
#define N 100

int main (int argc, char *argv[]) 
{
MPI_Init(&argc, &argv); 
double t0, t1;
double start_time = MPI_Wtime();
int tid, nthreads, i, j, k;
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

// Allocate buffer
double *buffer = malloc(NCB * sizeof(double));


  /*** Initialize matrices ***/
  for (i=0; i<NRA; i++)
    for (j=0; j<NCA; j++)
      a[i][j]= i+j;
  
  for (i=0; i<NCA; i++)
    for (j=0; j<NCB; j++)
      b[i][j]= i*j;

  /* Parallelize the computation of the following matrix-matrix multiplication. 
     How to partition and distribute the initial matrices, the work, and collecting
     final results.
  */

  t0  = MPI_Wtime();
  MPI_Comm_size(MPI_COMM_WORLD, &nthreads);
  MPI_Comm_rank(MPI_COMM_WORLD, &tid);



if  (tid < nthreads - 1)
{
    int min_rows = NRA / (nthreads -1);
    int leftover = NRA - min_rows*(nthreads-1);
    int start = min_rows * tid + ((tid < leftover) ? tid : leftover);
    int end   = start + min_rows + ((tid < leftover) ? 1 : 0);

    double *wait_time = malloc((end-start) * sizeof(double));

    for (int i = start; i < end; i++) {
        // clear buffer for current row of C
        for (int j = 0; j < NCB; j++)
            buffer[j] = 0.0;

        // compute row i of C using buffer
        for (int k = 0; k < NCA; k++) {
            double a_ik = a[i][k];  // local element of A
            for (int j = 0; j < NCB; j++)
                buffer[j] += a_ik * b[k][j];
        }
        //double start_time = MPI_Wtime();
        MPI_Send(buffer, NCB, MPI_DOUBLE, nthreads - 1 , i, MPI_COMM_WORLD);
        //wait_time[i-start] = MPI_Wtime() - start_time;

    }
}
else
{
    // Allocate c
    double **c = malloc(NRA * sizeof(double*));
    for (int i = 0; i < NRA; i++) c[i] = malloc(NCB * sizeof(double));

      for (i=0; i<NRA; i++)
        for (j=0; j<NCB; j++)
            c[i][j]= 0;
    MPI_Status status;
    for (int i=0; i < NRA; i++) 
    {
        MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        MPI_Recv(c[status.MPI_TAG], NCB, MPI_DOUBLE, status.MPI_SOURCE, status.MPI_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
    }
    t1  = MPI_Wtime();

    for (int i = 0; i < NRA; i++) free(c[i]);
    free(c);
}




/*  perform time measurement. Always check the correctness of the parallel results
    by printing a few values of c[i][j] and compare with the sequential output.
*/
for (int i = 0; i < NRA; i++) free(a[i]);
free(a);
for (int i = 0; i < NCA; i++) free(b[i]);
free(b);

free(buffer);
if  (tid == nthreads - 1)
{
    printf("calculation time: %f, total time is: %f, n:%i \n", t1 - t0, MPI_Wtime() - start_time, nthreads);
}

MPI_Finalize();

    return 0; 
}