CC = gcc
OBJECTS = main.o powers_of/power.o shared.o \
          array_manipulation/strrev.o array_manipulation/lzero.o \
          array_manipulation/intrev.o

TARGETS = algorithms

all: $(TARGETS)

%.o: %.c
	$(CC) -Wall -std=gnu99 -c -g -o $@ $<

algorithms: $(OBJECTS)
	$(CC) -o algorithms $(OBJECTS)

clean:
	@echo Cleaning up.
	rm -f *.o
	rm algorithms
	@echo Done.
