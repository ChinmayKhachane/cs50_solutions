#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;
            float avg = (red + green + blue) / 3;
            int gray = round(avg);
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;

        }

    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;
            int sepiaRed = round(0.393 * red + 0.769 * green + 0.189 * blue);
            int sepiaGreen = round(0.349 * red + 0.686 * green + 0.168 * blue);
            int sepiaBlue = round(0.272 * red + 0.534 * green + 0.131 * blue);
            if(sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if(sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if(sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }

    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width /2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;


        }

    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
        copy[i][j] = image[i][j];
        }

    }
        for(int i = 0; i < height; i++)
        {
            for(int j = 0; j < width; j++)
            {
                int wholeLottaRed = 0;
                int wholeLottaGreen = 0;
                int wholeLottaBlue = 0;
                float count = 0.00;
                for(int k = -1; k <= 1; k++)
                {
                    for(int m = -1; m <= 1; m++)
                    {
                        int currRow = i + k;
                        int currCol = j + m;
                        if(currRow < 0 || currRow > height - 1 || currCol < 0 || currCol > width - 1)
                        {
                            continue;
                        }

                        wholeLottaRed += image[currRow][currCol].rgbtRed;
                        wholeLottaGreen += image[currRow][currCol].rgbtGreen;
                        wholeLottaBlue += image[currRow][currCol].rgbtBlue;
                        count++;
               }
           }
              copy[i][j].rgbtRed = round(wholeLottaRed / count);
              copy[i][j].rgbtGreen = round(wholeLottaGreen / count);
              copy[i][j].rgbtBlue = round(wholeLottaBlue / count);
        }
    }
for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
        image[i][j].rgbtRed = copy[i][j].rgbtRed;
        image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
        }

    }
    return;
}
