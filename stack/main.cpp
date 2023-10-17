#include <iostream>
#include "stack.h"

int main(){
	Stack<int> s;
	for (int i = 0; i < 5; i++)
		s.push(i);

	std::cout << s << std::endl;
	s.reverse();
	std::cout << s << std::endl;

	std::cout << "-------" << std::endl;

	Node<int> n(1);
	std::cout << n << std::endl;
}