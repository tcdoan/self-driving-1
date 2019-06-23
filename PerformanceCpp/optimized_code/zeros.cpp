#include "headers/zeros.h"

using namespace std;

vector < vector <float> > zeros(int height, int width) { 
	// OPTIMIZATION: Reserve space in memory for vectors
  	// OPTIMIZATION: nested for loop not needed
    // because every row in the matrix is exactly the same

	vector < vector <float> > grid(height, vector<float>(width, 0.0));
	return grid;
}