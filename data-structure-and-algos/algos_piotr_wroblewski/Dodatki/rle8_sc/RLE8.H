/* rle8.h                       */
/* by Shaun Case 1991           */
/* Public Domain                */
/* header for RLECOMP.C         */
/* and UNRLE.C                  */
/* (8 bit header versions)      */



#define MAX_LEN   (0x7f)              /* maximum length for runs or sequences    */
#define MAX_RUN_HEADER (0xff)         /* bit 7 == 1 : run follows                */
                                      /* bit 6 - 0  : length of run              */

#define MAX_SEQ_HEADER (0x7f)         /* bit 7 == 0 : unencode sequence follows  */
                                      /* bit 6 - 0  : length of sequence         */

#define RUN (0x80)                    /* bit 7 == 1 : run follows                */

#define SEQ (0x00)                    /* bit 7 == 0 : unencoded sequence follows */

