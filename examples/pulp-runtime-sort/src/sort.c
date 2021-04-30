#include <stdio.h>

void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void print_array(int* arr, int length) {
    printf("[");
    for (int i=0; i<length-1; ++i) {
        printf("%d, ", arr[i]);
    }

    printf("%d]\r\n", arr[length-1]);

}

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
                swap(&s_arr[left], &s_arr[right]);
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
    puts("** Getting started example! **\r\n");
    int arr[] = { 2, 50, 105, 64, 34, 25, 13, 77, 41, 90 };
    int len = sizeof(arr)/sizeof(arr[0]);
    print_array(arr, len);
    recursive_quick_sort(arr, 0, len-1);
    print_array(arr, len);
    while(1){}
}
