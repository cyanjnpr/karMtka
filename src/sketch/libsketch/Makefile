CC = gcc
CFLAGS = -Wall -std=c17 -fPIC
LDFLAGS = -shared
TARGET = libsketch.so
SRC = libsketch.c
OBJS = $(SRC:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ -lm -lpotrace

%.o: %.c %.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

