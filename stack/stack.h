#pragma once
#include <iostream>
#include <string>

template <typename T>
class Node
{
private:
	T val;
	Node<T>* next;

public:
	template <typename U>
	friend std::ostream &operator<<(std::ostream &output, const Node<U> &obj);

	Node(T val, Node *node) : val(val), next(node) {}
	Node(T val): val(val), next(nullptr) {}
	Node(const Node &other): val(other.val), next(nullptr) {}

	T get_val() const { return val; }
	Node<T>* get_next() const { return next; }
	
	void set_next(Node<T> *next) { this->next = next; }
	void set_val(T val) { this.val = val; }
};

template <typename T>
std::ostream &operator<<(std::ostream &output, const Node<T> &obj)
{
	output << "Value: " << obj.val;
	if (obj.next)
		output << " | Next: " << obj.next;
	else
		output << " | Next: nullptr";
	return output;
}

template <typename T>
class Stack
{
private:
	Node<T> *head;
	size_t size;

public:
	Stack() : head(nullptr), size(0) {}

	Stack(T val) {
		head = new Node<T>(val);
		size = 1;
	}

	Stack(const Stack<T>& s){
		head = new Node<T>();
		size = 0;
		s.reverse();

		for (size_t i = 0; i < s.size; i++)
			this->push(s.pop());
	}

	~Stack(){
		Node<T> *last;
		while (head != nullptr){
			last = head;
			head = head->get_next();
			delete last;
		}
	}

	void push(T val)
	{
		size++;
		head = new Node<T>(val, head);
	}

	T top() const { return head->get_val(); }

	T pop()
	{
		if (size == 0)
			return T();
		size--;

		T val = this->top();
		head = head->get_next();
		return val;
	}

	size_t length() const{
		return size;
	}

	void reverse(){
		// point of view of horizontal Stack
		Node<T> *right = head->get_next();
		if (right == nullptr)
			return;
		
		Node<T> *left = nullptr;
		while (right != nullptr){
			head->set_next(left);
			left = head;
			head = right;
			right = right->get_next();
		}
		head->set_next(left);
	}

	std::string to_string() const
	{
		std::string s = "[ ";
		Node<T> *tmp_head = head;

		while (tmp_head)
		{
			s += std::to_string(tmp_head->get_val()) + " ";
			tmp_head = tmp_head->get_next();
		}
		s += "]";
		return s;
	}
};

template <typename T>
std::ostream &operator<<(std::ostream &output, const Stack<T> &obj)
{
	output << obj.to_string();
	return output;
}