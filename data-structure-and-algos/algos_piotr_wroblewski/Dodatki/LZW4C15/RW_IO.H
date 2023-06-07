/* RW_IO.H */

int ReaderOpen(char *);
int Reader(void);
long ReaderCount(void);
void ReaderClose(void);
void ReaderFlush(void);

int WriterOpen(char *);
int Writer(char);
long WriterCount(void);
void WriterClose(void);
void WriteFlush(void);
