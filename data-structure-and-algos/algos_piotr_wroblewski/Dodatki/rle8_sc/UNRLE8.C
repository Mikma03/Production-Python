/* unrle8.c                            */
/* RLE compression, uses 8 bit headers */
/* by Shaun Case 1991 Borland C++ 2.0  */
/* Public Domain                       */

#include <stdio.h>
#include <string.h>

#include "rle8.h"

int main(int argc, char **argv)
{
    register int byte;
    register unsigned short i;
    register unsigned short length;
    int packet_hdr;
    char orig_filename[14]; /* original filename */
    char *infile_name;
    char scratch_space[134];


    FILE *infile, *outfile;

    if (argc != 2)
    {
        puts("Usege: unrle8 filename");
        return 1;
    }
    puts("unlre8   by Shaun Case 1991  public domain");

    infile_name = argv[1];

    if ((infile=fopen(infile_name, "rb")) == NULL)
    {
        strcpy(scratch_space, "Unable to open ");
        strcat(scratch_space, infile_name);
        puts(scratch_space);
        return 1;
    }

    for (i = 0; i < 13; i++)   /* get original filename */
        if ((orig_filename[i] = fgetc(infile)) == EOF)
        {
            puts("Error reading original filename from input file.");
            return 1;
        }

    if ((outfile=fopen(orig_filename, "wb")) == NULL)
    {
        strcpy(scratch_space, "Unable to open ");
        strcat(scratch_space, orig_filename);
        puts(scratch_space);
        return 1;
    }


    while (!feof(infile))
    {
        packet_hdr = fgetc(infile);

        if (feof(infile))
            continue;

        length = MAX_LEN & packet_hdr;

        if (packet_hdr & RUN)  /* if it's a run... */
        {
            byte = fgetc(infile);

            for (i = 0; i < length; i++)
                if (fputc(byte, outfile)== EOF)
                {
                    strcpy(scratch_space, "Error writing to ");
                    strcat(scratch_space, orig_filename);
                    puts(scratch_space);
                    fclose(infile);
                    fclose(outfile);
                    return 1;
                }
        }

        else /* it's a sequence */

            for (i = 0; i < length; i++)
                if (fputc(fgetc(infile), outfile)==EOF)
                {
                    strcpy(scratch_space, "Error writing to ");
                    strcat(scratch_space, orig_filename);
                    puts(scratch_space);
                    fclose(infile);
                    fclose(outfile);
                    return 1;
                }
    }
    fclose(infile);
    fclose(outfile);
    return 0;
}

