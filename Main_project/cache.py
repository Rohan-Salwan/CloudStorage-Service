class Node:
    def __init__(self,val,key):
        self.val=val
        self.prev=None
        self.next=None
        self.key=key    
class Cache:
    def __init__(self):
        self.head=None
        self.tail=None
        self.Map={}
        self.count=0
    
    def Put(self,key,value):
        node=Node(value,key)
        self.Map[key]=node
        if self.head==None:
            self.head=node
            self.tail=node
            self.count+=1
        else:
            if self.count==100:
                # condition for page fault.
                # evicting least recent usage page(LRU) and adding most recent page.
                key=self.head.key
                self.head=self.head.next
                self.head.prev=None
                self.count-=1
                self.Map.pop(key,None)
            # adding pages according to its requesting priority
            self.tail.next=node
            self.tail.next.prev=self.tail
            self.tail=self.tail.next
            self.count+=1
                
    def get(self,Key,Update_Node=None):
        if Update_Node:
            self.Map[Key].val=Update_Node
        node=self.Map[Key]
        if node.prev and node.next is None or node.prev is None and node.next is None:
            pass
        elif node.prev is None:
            node.next.prev=None
            node.next=None
            self.tail.next=node
            self.tail=self.tail.next
        else:
            node.prev.next=node.next
            node.next.prev=node.prev
            self.tail.next=node
            node.prev=self.tail
            self.tail=self.tail.next
            self.tail.next=None
        # return requested page and also update it to most recent page.
        if Update_Node is None:
            return self.tail.val

    def delete(self,key):
        node=self.Map[key]
        if node.prev and node.next is None:
            node.prev=None
        elif node.prev is None and node.next is None:
            node=None
        elif node.prev is None and node.next:
            node.next.prev=None
        else:
            node.prev.next=node.next
            node.next.prev=node.prev
        self.Map.pop(key,None)
