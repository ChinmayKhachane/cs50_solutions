#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Enter the mario puzzle height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
//prints out all the spaces before the hashes
        for (int j = height - 1; j > i; j--)
        {
            printf(" ");
        }
//prints out the hashes
        for (int h = 0; h <= i; h++)
        {
            printf("#");
        }
        printf("\n");
    }
}