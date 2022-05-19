# AVL-Tree-Rotatations-for-Deletions
This programs counts the amount of rotations that re required to person a rotation in order to rebalance the tree:


## Dependencies:

* **sys**
* **math**
* **time**
* **copy**
* **random**
* **igraph**

## How to use:

* On the CLI: navigate to the the file and type ```python3 AVL_Tree.py #amount_of_layers``` This would generate a tree of different hight based on the number you gave as an input. The estimated time for 7 or more layers is around 20 minutes. It will generate a visual representation of the tree online. 

### example command:
```python3 AVL_Tree.py 3```
```python3 AVL_Tree.py 4```
```python3 AVL_Tree.py 5```


### example output:
```
List of numbers to create the tree:  [8, 5, 2, 9, 15, 10, 14, 11, 7, 4, 1, 3, 13, 12, 6]
#Rotations to cause a deletion [1, 2, 1, 2, 1, 1, 3, 1, inf]
#Rotations: [1, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 0, 3, 1, 0, 0, inf]
Duration = 0.03815412521362305 seconds... (0.0006359020868937174 minutes, 1.059836811489529e-05 hours)
```
