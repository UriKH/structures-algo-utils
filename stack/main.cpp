#include <iostream>
#include "stack.h"

int main(){
	Stack<int> s;
	for (int i = 0; i < 5; i++)
		s.push(i);

	std::cout << s.to_string() << std::endl;
	s.reverse();
	std::cout << s.to_string() << std::endl;
}