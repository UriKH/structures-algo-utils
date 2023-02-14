#pragma once
#include <iostream>

template <typename T>
class Node
{
private:
	T val;
	Node* next;

public:
	Node(T val, Node *node) : val(val), next(node) {}
	Node(T val): val(val), next(nullptr){}
	Node(const Node &other): val(other.val), next(nullptr) {}

	T get_val() const { return val; }

	Node* get_next() const { return next; }

	void set_next(Node *next)
	{
		this->next = next;
	}
};

template <typename T>
class Stack
{
private:
	Node<T> *head;
	size_t size;

public:
	Stack() : head(nullptr), size(0) {}

	Stack(T val) {
		head = new Node<T>(val, nullptr);
		size = 0;
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

	T top() { return head->get_val(); }

	T pop()
	{
		if (size == 0)
			return T();
		size--;

		T val = this->top();
		head = head->get_next();
		return val;
	}

	size_t length(){
		return size;
	}
};