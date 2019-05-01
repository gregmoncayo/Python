//
//  main.cpp
//  OpenMP
//
//  Created by Gregory Moncayo on 4/24/19.
//  Copyright © 2019 Gregory Moncayo. All rights reserved.
//
#include <iostream>
#include <omp.h>
#include <cstdlib>
#include <iomanip>
using namespace std;

// Function to find contiguous sub-array with the largest sum
// in given set of integers
int kadane(int arr[], int n)
{
    int i = 0;
    int j = 0;
    // stores maximum sum sub-array found so far
    int max_so_far = 0;
    
    // stores maximum sum of sub-array ending at current position
    int max_ending_here = 0;
    
    // traverse the given array
    for (int i = 0; i < n; i++)
    {
        // update maximum sum of sub-array "ending" at index i (by adding
        // current element to maximum sum ending at previous index i-1)
        max_ending_here = max_ending_here + arr[i];
        
        // if maximum sum is negative, set it to 0 (which represents
        // an empty sub-array)
        max_ending_here = max(max_ending_here, 0);
        
        // update result if current sub-array sum is found to be greater
        max_so_far = max(max_so_far, max_ending_here);
    }
   
	#pragma openmp parallel	private(i, j) share(n) 
	{	
		for (i = 0; i < n; i++)
		{
			max_ending_here = max_ending_here + arr[i];

			for (j = 0; j < i; j++)
			{
				max_so_far = max(max_ending_here, max_so_far); 
			}
		}
	}

    return max_so_far;
}

// main function
int main()
{
    double wtime = 0.0;
    int num = 0;
    double high = 1.0;
    cout << "Enter a number of size: ";
    cin >> num;
    
    int * array = new int[num];
    
    for (int i = 0; i < num; i++)
    {
        cout << "Enter integer values for the array: ";
        cin >> array[i];
        cout << endl;
    }
    
    
    cout << "The sum of contiguous sub-array with the largest sum is " << kadane(array, num) << endl;

	cout << "The time it takes to run the program: " << endl;

	for (int j = 0; j < num; j++)
	{
		wtime = omp_get_wtime();
		high = omp_get_wtime() - wtime;
		cout << "Time: " << high << endl;
	}
		cout << "Original Time:" << wtime << endl;

    delete [] array;
    
    return 0;
}
