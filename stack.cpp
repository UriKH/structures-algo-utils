#include <iostream>
#include "stack.h"
#include <string>

int main() {
	Stack<std::string> s;
	s.push("hi!");
	std::cout << s.top() << std::endl;
	std::cout << s.length() << std::endl;
	std::cout << s.pop() << std::endl;
	std::cout << s.length() << std::endl;
	std::cout << s.pop() << std::endl;
	std::cout << s.length() << std::endl;
	return 0;
}