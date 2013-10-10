all: scheduling

scheduling: main.o
	g++ main.o -o scheduling

main.o: main.cpp
	g++ -c main.cpp

clean:
	rm -rf *o scheduling

