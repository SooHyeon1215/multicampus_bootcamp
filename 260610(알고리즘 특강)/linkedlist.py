class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head is None

    def insert(self, index, data):
        new_node = Node(data)

        if index == 0:  #맨 앞에 추가
            new_node.next = self.head
            self.head = new_node
            return
        
        prev = self.head
        for _ in range(index-1):
            if prev is None:
                raise IndexError('Index out of range')
            prev=prev.next

            new_node.next = prev.next
            prev.next = new_node

    def length(self):
        count=0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def delete(self, index):
        if self.head is None:   #리스트가 비어있을 때
            raise IndexError('List is empty')
        
        if index == 0:  #맨 처음 지울 때
            self.head=self.head.next
            return
        
        prev=self.head
        for _ in range(index-1):
            if prev.next is None:
                raise IndexError('Index out of range')
            prev=prev.next

        if prev.next is None:
            raise IndexError('Index out of range')
        
        prev.next=prev.next.next

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=' -> ')
            current=current.next
        print('None')

    def get(self, index):   #get 함수 정의 이게 맞나?
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError('Index out of range')
            current = current.next
        if current is None:
            raise IndexError('Index out of range')
        return current.data

    def update(self, index, item):
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError('Index out of range')
            current = current.next
        
        if current is None:
            raise IndexError('Index out of range')
        
        current.data = item