# Common variables
CFLAGS = -g -static -O2
TARGET = zip2hashcat

# Compiler for Linux
CC = gcc

# List of source files
SOURCES = $(TARGET).c

all: $(TARGET)

# Build target for Linux
$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -f $(TARGET)
