#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{

string test = get_string("What string do you want me to test\n");

int letters = 0;
int sentences = 0;
int words = 1;

for (int i = 0; i < strlen(test); i++)
{
    if (isalpha(test[i]) > 0){
        letters++;
    }
    if (test[i] == ' ')
    {
        words++;
    }
    if (test[i] == '.' || test[i] == '!' || test[i] == '?')
    {
        sentences++;
    }
}
    float let = (float) letters / words * 100;
    float sen = (float) sentences / words * 100;
    int score = round( 0.0588 * let - 0.296 * sen - 15.8);

    if (score > 16)
    {
        printf("Grade 16+\n");
    }
    else if (score < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", score);
    }
}

