#include <stdio.h> 

void recursive_quick_sort(int *s_arr, int first, int last)
{
    if (first < last)
    {
        int left = first, right = last, middle = s_arr[(left + right) / 2];
        do
        {
            while (s_arr[left] < middle) left++;
            while (s_arr[right] > middle) right--;
            if (left <= right)
            {
                int tmp = s_arr[left];
                s_arr[left] = s_arr[right];
                s_arr[right] = tmp;
                left++;
                right--;
            }
        } while (left <= right);
        recursive_quick_sort(s_arr, first, right);
        recursive_quick_sort(s_arr, left, last);
    }
}

int main() 
{
    int arr[] = { 2, 50, 105, 64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr)/sizeof(arr[0]);
    recursive_quick_sort(arr, 0, n-1);
    while(1){}
} 

