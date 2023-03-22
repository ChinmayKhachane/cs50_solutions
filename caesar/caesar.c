#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
        int key = atoi(argv[1]);
        string word = get_string("Plaintext: ");
        printf("Ciphertext: ");

        for (int k = 0; k < strlen(word); k++)
        {
            if (islower(word[k]))
            {
                printf("%c", (word[k] + key - 97) % 26 + 97);
            }

            else if (isupper(word[k]))
            {
                printf("%c", (word[k] + key - 65) % 26 + 65);
            }

            else
            {
                printf("%c", word[k]);
            }
         }
         printf("\n");
}