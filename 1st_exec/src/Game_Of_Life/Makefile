# GIF?=-DOUTPUT
GIF?=

all: Game_Of_Life

Game_Of_Life: Game_Of_Life.c
	gcc -O3 $(GIF) -fopenmp -o Game_Of_Life Game_Of_Life.c

clean:
	rm Game_Of_Life
