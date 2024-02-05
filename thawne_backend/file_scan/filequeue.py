class FileQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.items:
            return self.items.pop(0)
        else:
            return False
    
    def is_empty(self):
        if not self.items:
            return True
        return False

    def size(self):
        return len(self.items)
    
    def peek(self):
        if self.items:
            return self.items[0]
        else:
            return False
        
    def display(self):
        return self.items