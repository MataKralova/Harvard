/**
 * Resizes (i.e., enlarges) 24-bit uncompressed BMPs by a factor of n.
 */
// Done by Mata

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // ensure n is positive max 100
    int n = atoi(argv[1]);
    if (n < 1 || n > 100)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile, where n is a positive int smaller or equal to 100.\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // avoid "minus unsigned long" runtime error by casting it as integer
    int pixel = sizeof(RGBTRIPLE);

    // determine padding for scanlines in infile
    int paddingI = (4 - (bi.biWidth * pixel) % 4) % 4;

    // determine padding for scanlines in outfile
    int paddingO = (4 - (bi.biWidth * n * pixel) % 4) % 4;

    // update values of header fields to be written to outfile
    bi.biWidth = bi.biWidth * n;
    bi.biHeight = bi.biHeight * n;
    bi.biSizeImage = (bi.biSizeImage - (paddingI * abs(bi.biHeight) / n)) * n * n + (paddingO * abs(bi.biHeight));
    bf.bfSize = bi.biSizeImage + 54;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // set back the values to default infile values
    bi.biWidth = bi.biWidth / n;
    bi.biHeight = bi.biHeight / n;

    // determine offset for fseek
    //int offset = SEEK_CUR - (bi.biWidth * pixel) - paddingI;

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // repeat to multiply each line as many times as requested
        for (int r = 0; r < n; r++)
        {
            // return cursor to the beginning of the line
            if (r != 0)
            {
                // determine offset value
                int offset = ftell(inptr) - (bi.biWidth * pixel) - paddingI;
                fseek(inptr, offset, SEEK_SET);
            }

            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile as many times as required
                for (int a = 0; a < n; a++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // skip over padding, if any
            fseek(inptr, paddingI, SEEK_CUR);

            // then add it back (to demonstrate how)
            for (int k = 0; k < paddingO; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
