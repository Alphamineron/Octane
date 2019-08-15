from treelib import Tree
from treelib.exceptions import DuplicatedNodeIdError
tree = Tree()
try:
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    tree.create_node("Mark", "mark", parent="jane")
    tree.create_node("Mark", "mark", parent="jane")
except DuplicatedNodeIdError as e:
    pass
tree.show()

node = tree.get_node("bill")
node.data = []
for i in ["A", "B", "C", "D"]:
    node.data.append(i)
print(node)
for node in tree.expand_tree(mode=Tree.ZIGZAG):
    print(node)
