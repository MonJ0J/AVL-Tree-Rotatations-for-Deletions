import sys
import math
import copy
import time
import random
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

class node:
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
            self.height = 1

        def get_left(self):
            return self.left
        def get_right(self):
            return self.right
        def get_data(self):
            return self.data

        def printNodes(self, level=0):
            print("\t" * level + repr(self.data)+" h:"+str(self.height))
            if self.left:
                self.left.printNodes(level+1)
            if self.right:
                self.right.printNodes(level+1)



#avl tree class which contains insertion ,deletion and traversal operation.

class avl_tree_class(object):

    def insert(self, root, key):
                #if the avl tree is empty make the first node as the root and insert it.
        global rotated
        rotated = 0
        if not root:
            return node(key)
                #if key is less than root's data then traverse to the left side of tree recursively and insert the key.
        elif key < root.data:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        #update the height of parent node.
        root.height = 1 + max(self.getHeight(root.left),self.getHeight(root.right))
                #Get the balance factor
        balance = self.getBalance(root)
                # balance the node using Left Left rotation.
        if balance > 1 and key < root.left.data:
            return self.rightRotate(root)

                # balance the node using right right rotation.
        if balance < -1 and key > root.right.data:
            return self.leftRotate(root)

                # balance the node using left right rotation.
        if balance > 1 and key > root.left.data:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

                # balance the node using right left rotationg
        if balance < -1 and key < root.right.data:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
        return root

    # recursive function to delete a node from the tree.
    def delete(self, root, key):
        global rotated
        rotated = 0

        if not root:
                return root

        elif key < root.data:
            root.left = self.delete(root.left, key)

        elif key > root.data:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMindataueNode(root.right)
            root.data = temp.data
            root.right = self.delete(root.right,temp.data)


        if root is None:
            return root


        root.height = 1 + max(self.getHeight(root.left),self.getHeight(root.right))

                # Get the balance factor
        balance = self.getBalance(root)


        #below are the cases which handles to balance the avl tree accordingly.
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)


        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    #left rotation of node to maintain the tree balanced.
    def leftRotate(self, z):
        global rotated
        rotated+=1

        y = z.right
        T2 = y.left

    # Perform rotation
        y.left = z
        z.right = T2

    #Update heights
        z.height = 1 + max(self.getHeight(z.left),self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),self.getHeight(y.right))


        return y

    #perform right rotation on tree.
    def rightRotate(self, z):
        global rotated
        rotated+=1

        y = z.left
        T3 = y.right

                # Perform rotation
        y.right = z
        z.left = T3

                # Update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    # def getHeight(self,root):
    #     if not root:
    #         return 0
    #     return max(self.getHeight(root.left), self.getHeight(root.left)) + 1

    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMindataueNode(self, root):
        if root is None or root.left is None:
            return root

        return self.getMindataueNode(root.left)

    def preOrder(self, root):

        if not root:
            return

        print("{0} ".format(root.data), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)


#Algorithm:
#Go through each of the leaves, try deleting it and see if it
#causes a rotation. If any such does, return the tree without
#that node and 1. Otherwise, try the function without each
#leaf, recursively, and return the resulting tree after a minimal
#number of deletions such that a rotation needs to be done, along
#with the minimum number of deletions.

#Rework the delete function to keep track of when a rotation occurs

def inorder(root):
    if root == None:
        return ""
    out = ""
    out+=inorder(root.left)
    out+=", "+str(root.data)
    out+=inorder(root.right)
    return out

def leafs(curr_node,leaf = []):
    if curr_node == None:
        return leaf

    if curr_node.get_left() == None and curr_node.get_right() == None:
        leaf.append(curr_node)
        return leaf
    leaf = leafs(curr_node.get_left(),leaf)
    leaf = leafs(curr_node.get_right(),leaf)
    return leaf

def copy_tree(curr_node):#root
    tree_copy = copy.deepcopy(curr_node)
    return tree_copy

def make_nums(n):
    nums = []
    for p in range(n-1, -1, -1): #start at the top layer, where we put in 2^(n-1)
        for i in range(2**(n-1-p)): #we need to put in exactly 2^(n-1-p) numbers
            nums.append((2*i+1)*2**p) #these numbers are precisely the odd numbers, multiplied by 2^p
    return nums

def count_rotations(curr_node, currMin = 3, depth = 0):
    if depth>currMin:
        return curr_node, float("inf")
    global rotated
    global tree
    min_deletions = float("inf")
    res_tree = None
    list_leafs = leafs(curr_node, [])
    for i in list_leafs:
        cp_tree = copy_tree(curr_node)
        cp_tree = tree.delete(cp_tree, i.get_data())
        if rotated!=0:
            return (cp_tree,1)
        temp, cur_dels = count_rotations(cp_tree, min_deletions, depth+1)
        cur_dels+=random.random()
        if min_deletions > cur_dels:
            min_deletions = cur_dels
            res_tree = temp
    if min_deletions == float("inf"):
        return res_tree, min_deletions
    return res_tree, math.floor(min_deletions)+1

def deep_count_rotations(curr_node, currMin = 3, depth = 0):
    if depth>currMin:
        return curr_node, float("inf"), 0
    global rotated
    global tree
    min_deletions = float("inf")
    res_tree = None
    min_rot = 0
    list_leafs = leafs(curr_node, [])
    for i in list_leafs:
        cp_tree = copy_tree(curr_node)
        cp_tree = tree.delete(cp_tree, i.get_data())
        if rotated!=0:
            return (cp_tree,1, rotated)
        temp, cur_dels, tempRotated = deep_count_rotations(cp_tree, min_deletions, depth+1)
        cur_dels+=random.random()
        if min_deletions > cur_dels:
            min_deletions = cur_dels
            res_tree = temp
            min_rot = tempRotated
    if min_deletions == float("inf"):
        return res_tree, min_deletions, min_rot
    return res_tree, math.floor(min_deletions)+1, min_rot

def count_sequence(root):
    # print(inorder(root), root.data)
    sequence = []
    run = 0
    while root:
        temp = copy_tree(root)
        root, count = count_rotations(root)
        sequence.append(count)
        # if count == 3:
        #     temp.printNodes()
        run+=1
        # print("Run "+str(run)+" complete!")
        # print([i.data for i in leafs(root, [])])
    return sequence

def count_deep_sequence(root):
    # print(inorder(root), root.data)
    sequence = []
    run = 0
    while root:
        temp = copy_tree(root)
        root, count, rot = deep_count_rotations(root)
        sequence.append(count)
        if rot>1:
            for i in range(rot):
                sequence.append(0)
        # if count == 3:
        #     temp.printNodes()
        run+=1
        # print("Run "+str(run)+" complete!")
        # print([i.data for i in leafs(root, [])])
    return sequence

def print_tree(root_node):

    cur_level = [root_node]
    levels = [cur_level]
    #While not the last level has elements in it, make the levels
    while cur_level.count(None) < len(cur_level):
        #Make the next level
        new_level = []
        for node in cur_level:
            if node:
                new_level.append(node.get_left())
                new_level.append(node.get_right())
            else:
                new_level += [None, None]
        levels.append(new_level)
        cur_level = new_level

    for i in range(len(levels)-1):
        spacing_between = 3*(2**(len(levels) - i - 2)) - 2
        spacing_before = spacing_between // 2
        #print(spacing_between, spacing_before)
        #Print the current level
        print(end = " "*(spacing_before))
        for node in levels[i]:
            if node:
                write = str(node.get_data())
                if len(write) < 2:
                    write += " "
            else:
                write = "  "
            print(write, end = " " * spacing_between)
        print()

tree = avl_tree_class()

######Visualization:



def main():
    myTree = avl_tree_class()
    root = None
    nums = make_nums(int(sys.argv[1]))
#    nums = [3, 7, 8, 12, 9, 4, 13, 15, 10, 5, 14, 11, 6, 2, 1]
    random.shuffle(nums)
    print("List of numbers to create the tree: ",nums)
    for num in nums:
        
        root = myTree.insert(root, num)
#        print("Insert "+str(num)+(" rotated " if rotated else "")+":")
#            # root.printNodes()
#    print_tree(root)
#    cnt = count_rotations(root)
#    print(cnt)
#    # root.printNodes()
    start = time.time()
    print("#Rotations to cause a deletion",count_sequence(root))
    print("#Rotations:",count_deep_sequence(root))
    end = time.time()
    print("Duration = "+str(end-start)+" seconds... ("+str((end-start)/60)+" minutes, "+str((end-start)/3600)+" hours)")
    
    
######Visualization:
    nr_vertices = len(nums)
    v_label = list(map(str, range(nr_vertices)))
    G = Graph.Tree(nr_vertices, 2) # 2 stands for children number
    lay = G.layout('rt')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label

    rotated = 0


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(210,210,210)', width=1),
                       hoverinfo='none'
                       ))
    fig.add_trace(go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='nodes',
                      marker=dict(symbol='circle-dot',
                                    size=40,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                      text=labels,
                      hoverinfo='text',
                      opacity=0.8
                      ))
    def make_annotations(pos, text, labels,font_size=20, font_color='rgb(250,250,250)'):
        L=len(pos)
        if len(text)!=L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=labels[k], # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2*M-position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations
    
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

    fig.update_layout(title= 'Initial AVL Tree',
                  annotations=make_annotations(position, v_label, nums),
                  font_size=20,
                  showlegend=False,
                  xaxis=axis,
                  yaxis=axis,
                  margin=dict(l=40, r=40, b=85, t=100),
                  hovermode='closest',
                  plot_bgcolor='rgb(248,248,248)'
                  )
    fig.show()
    
    
    
if __name__ == '__main__':
    main()
