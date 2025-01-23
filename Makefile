# Common variables
CFLAGS = -g -static -O2
CC = gcc

# Target executables
TARGETS = zip2hashcat combinator

# Source files
SOURCES_ZIP2HASHCAT = zip2hashcat.c
SOURCES_COMBINATOR = combinator.c

all: $(TARGETS)

# Build target for zip2hashcat
zip2hashcat: $(SOURCES_ZIP2HASHCAT)
	$(CC) $(CFLAGS) $^ -o $@

# Build target for combinator
combinator: $(SOURCES_COMBINATOR)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -f $(TARGETS)
