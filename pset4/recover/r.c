/**
* Program that recovers JPEG photos from .raw file.
*
**/

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }
    
    // define input file name
    char *infile = argv[1];
    
    // define output file name
    char *outfile = 0;
    
    // define filename
    char filename[7];
    
    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // counter of .jpg files created
    int image = 0;
    
    // name the outfile
    sprintf(filename, "%03i.jpg", image);

    // open output file
    FILE *outptr = fopen(filename, "w");
    if (outptr == NULL)
    {
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }
    
    // temporary storage for 512-byte chunk of data, called "block"
    BYTE block[512];
    
    int start = 0;

    // find first JPEG
    while (start == 0)
    {
        // read block
        fread(&block, sizeof(BYTE), 512, inptr);
        
        // check if it's the beginning of a JPEG
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            fwrite(&block, sizeof(BYTE), 512, outptr);
            start++;
        }
    }
 
    // iterate 5000 times, hoping to copy way into the file, but not reaching (nor treating) EOF
    for (int i = 0; i < 5000; i++)
    {
        fread(&block, sizeof(BYTE), 512, inptr);
        
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xff) == 0xe0)
        {
            fclose(outptr);
            image++;
            
            // create new output file
            sprintf(filename, "%03i.jpg", image);

            // open new output file
            fopen(filename, "w");
            if (outptr == NULL)
            {
                fprintf(stderr, "Could not create %s.\n", outfile);
                return 3;
            }
            
            // copy 512 bytes to output file
            fwrite(&block, sizeof(BYTE), 512, outptr);
            i++;
        }
        else
       {
            fwrite(&block, sizeof(BYTE), 512, outptr);
            i++;
        }
    }





    //    fwrite(&block, sizeof(BYTE), 512, outptr);
    //}
 
 
 
    // stop if EOF reached
    //while (fread(&block, sizeof(BYTE), 512, inptr) == 512)
    //{
    //    fread(&block, sizeof(BYTE), 512, inptr);
        
    //    if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xff) == 0xe0)
    //    {
    //        fclose(outptr);
    //        image++;
            
            // create new output file
    //        sprintf(filename, "%03i.jpg", image);

            // open new output file
    //        fopen(filename, "w");
    //        if (outptr == NULL)
    //        {
    //            fprintf(stderr, "Could not create %s.\n", outfile);
    //            return 3;
    //        }
            
            // copy 512 bytes to output file
    //        fwrite(&block, sizeof(BYTE), 512, outptr);
    //    }
    //    else
    //   {
    //        fwrite(&block, sizeof(BYTE), 512, outptr);
    //    }
    //}

    // close the outfile
    fclose(outptr);

    // close infile
    fclose(inptr);
    
    // success
    return 0;
}
