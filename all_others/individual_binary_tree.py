class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.child_count = 0


def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        elif key > root.val:
            root.right = insert(root.right, key)
    return root


def update_child_count(node):
    if node is None:
        return 0
    node.child_count = 1 + update_child_count(node.left) + update_child_count(node.right)
    return node.child_count


def find_node_with_max_diff(root):
    max_diff = -1
    target_node = None

    def dfs(node):
        nonlocal max_diff, target_node
        if node is None:
            return

        left_count = node.left.child_count if node.left else 0
        right_count = node.right.child_count if node.right else 0
        diff = abs(left_count - right_count)

        if diff > max_diff or (diff == max_diff and node.val > (target_node.val if target_node else float('-inf'))):
            max_diff = diff
            target_node = node

        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return target_node


def delete_node(root, key):
    if root is None:
        return root
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        min_larger_node = root.right
        while min_larger_node.left is not None:
            min_larger_node = min_larger_node.left

        root.val = min_larger_node.val
        root.right = delete_node(root.right, min_larger_node.val)

    return root


def pre_order_traversal(root, result):
    if root:
        result.append(root.val)
        pre_order_traversal(root.left, result)
        pre_order_traversal(root.right, result)


def main():
    with open('input.txt', 'r') as f:
        keys = list(map(int, f.read().strip().split()))

    root = None
    for key in keys:
        root = insert(root, key)

    update_child_count(root)

    node_to_delete = find_node_with_max_diff(root)

    if node_to_delete:
        root = delete_node(root, node_to_delete.val)

    result = []
    pre_order_traversal(root, result)

    with open('out.txt', 'w') as f:
        f.write('\n'.join(map(str, result)))


if __name__ == '__main__':
    main()
