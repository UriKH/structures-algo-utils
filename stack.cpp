#include <iostream>

template <typename T>
class Node{
private:
	T val;
	Node *next;

public:
	Node(T val, Node *node): val(val), next(node){}
	
	Node(T val){
		this->val = val;
		this->next = nullptr;
	}

	Node Node(Node other){
		return Node(other.val, nullptr);
	}

	T get_val() const{
		return val;
	}

	Node* get_next() const{
		return next;
	}

	void set_next(Node *next){
		this->next = next;
	}
};

template <typename T>
class Stack: public Node{
private:
	Node *head;

private:
	Stack(T val){
		this->head = new Node(val, nullptr);
	}

	bool append(T val){
		this->head->set_next(new Node(val, nullptr));
	}
};