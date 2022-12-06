/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
// Done by Mata

bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm

    int left = 0;
    int right = n - 1;
    int middle = (left + right) / 2;

    while (right >= left)
    {
        if (values[middle] == value)
        {
            return true;
        }
        else if (values[middle] > value)
        {
            right = middle - 1;
            middle = (left + right) / 2;
        }
        else if (values[middle] < value)
        {
            left = middle + 1;
            middle = (left + right) / 2;
        }
    }

    return false;
}

/**
 * Sorts array of n values.
 */
// Done by Mata

void sort(int values[], int n)
{
    // TODO: implement an O(n^2) sorting algorithm

    int swaps = 1;
    int left = 0;
    int right = 1;
    int holder;

    while (swaps != 0)
    {
        swaps = 0;

        for (left = 0, right = 1; right < n; left++, right++)
        {
            if (values[left] > values[right])
            {
                holder = values[left];
                values[left] = values[right];
                values[right] = holder;
                swaps++;
            }
        }
    }

    return;
}
