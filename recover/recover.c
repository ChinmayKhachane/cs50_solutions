#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage : ./recover image\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input== NULL)
    {
        printf("Error opening file");
        return 2;
    }
    int count = 0;
    BYTE buffer[512];
    FILE *output = NULL;
    char *name = malloc(8 * sizeof(char));

while (fread(buffer, BLOCK_SIZE, 1, input) == 1)
{

    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        if(count == 0)
        {
            sprintf(name, "%03i.jpg", count);
            output = fopen(name, "w");
            fwrite(buffer, BLOCK_SIZE, 1, output);
            count++;
        }

        else if(!(count == 0))
        {
            fclose(output);
            sprintf(name, "%03i.jpg", count);
            output = fopen(name, "w");
            fwrite(buffer, BLOCK_SIZE, 1, output);
            count++;
        }
    }

    else if(!(count == 0))
    {
        fwrite(buffer, BLOCK_SIZE, 1, output);
    }
}
    fclose(input);
    fclose(output);

}