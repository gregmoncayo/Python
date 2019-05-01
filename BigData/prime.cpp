# include <cstdlib>
# include <iostream>
# include <iomanip>

# include <omp.h>

using namespace std;

void prime_number_sweep ( int n_lo, int n_hi, int n_factor );
int prime_number ( int n );

//****************************************************************************80

int main ( int argc, char *argv[] )
{
  int n_factor;
  int n_hi;
  int n_lo;

  cout << "\n";
  cout << "PRIME_OPENMP\n";
  cout << "  C++/OpenMP version\n";

  cout << "\n";
  cout << "  Number of processors available = " << omp_get_num_procs ( ) << "\n";
  cout << "  Number of threads =              " << omp_get_max_threads ( ) << "\n";

  n_lo = 1;
  n_hi = 131072;
  n_factor = 2;

  prime_number_sweep ( n_lo, n_hi, n_factor );

  n_lo = 5;
  n_hi = 500000;
  n_factor = 10;

  prime_number_sweep ( n_lo, n_hi, n_factor );
  cout << "\n";
  cout << "PRIME_OPENMP\n";
  cout << "  Normal end of execution.\n";

  return 0;
}
//****************************************************************************80

void prime_number_sweep ( int n_lo, int n_hi, int n_factor )
{
  int n;
  int primes;
  double wtime;

  cout << "\n";
  cout << "TEST01\n";
  cout << "  Call PRIME_NUMBER to count the primes from 1 to N.\n";
  cout << "\n";
  cout << "         N        Pi          Time\n";
  cout << "\n";

  n = n_lo;

  while ( n <= n_hi )
  {
    wtime = omp_get_wtime ( );

    primes = prime_number ( n );

    wtime = omp_get_wtime ( ) - wtime;

    cout << "  " << setw(8) << n
         << "  " << setw(8) << primes
         << "  " << setw(14) << wtime << "\n";

    n = n * n_factor;
  }
 
  return;
}
//****************************************************************************80

int prime_number ( int n )
{
  int i;
  int j;
  int prime;
  int total = 0;

# pragma omp parallel \
  shared ( n ) \
  private ( i, j, prime )

# pragma omp for reduction ( + : total )
  for ( i = 2; i <= n; i++ )
  {
    prime = 1;

    for ( j = 2; j < i; j++ )
    {
      if ( i % j == 0 )
      {
        prime = 0;
        break;
      }
    }
    total = total + prime;
  }

  return total;
}
