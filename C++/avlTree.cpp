#include <algorithm>
#include <iostream>
using namespace std;

// AVL tree node: value, height, and two children
struct Node
{
    int key;
    int height;
    Node *left, *right;
    Node(int k) : key(k), height(1), left(nullptr), right(nullptr) {}
};

// Height helper: 0 for null nodes so we never deref a null pointer
int ht(Node* n)
{
    return n ? n->height : 0;
}

// Recompute a node's height from its children
void upd(Node* n)
{
    n->height = 1 + max(ht(n->left), ht(n->right));
}

// Balance factor: positive = heavy left, negative = heavy right
int bal(Node* n)
{
    return n ? ht(n->left) - ht(n->right) : 0;
}

// Rotate right around x (LL case fix)
Node* rotR(Node* x)
{
    Node* y = x->left;  // y becomes new root
    x->left = y->right; // y's right subtree moves under x
    y->right = x;
    upd(x);
    upd(y); // heights changed, recompute bottom-up
    return y;
}

// Rotate left around x (RR case fix)
Node* rotL(Node* x)
{
    Node* y = x->right; // y becomes new root
    x->right = y->left; // y's left subtree moves under x
    y->left = x;
    upd(x);
    upd(y);
    return y;
}

// Rebalance a node assuming only its balance factor is off
Node* fix(Node* n)
{
    upd(n);
    int b = bal(n);
    if (b > 1)
    {                         // left heavy
        if (bal(n->left) < 0) // LR case: inner subtree needs a left turn first
            n->left = rotL(n->left);
        return rotR(n); // LL (or resolved LR)
    }
    if (b < -1)
    {                          // right heavy
        if (bal(n->right) > 0) // RL case: inner subtree needs a right turn first
            n->right = rotR(n->right);
        return rotL(n); // RR (or resolved RL)
    }
    return n; // already balanced
}

// Insert key, returning the (possibly rebalanced) subtree root
Node* ins(Node* n, int k)
{
    if (!n)
        return new Node(k);
    if (k < n->key)
        n->left = ins(n->left, k);
    else if (k > n->key)
        n->right = ins(n->right, k);
    else
        return n;  // duplicate: no change
    return fix(n); // rebalance on the way up
}

// Leftmost node (successor of a node with two children)
Node* leftMost(Node* n)
{
    while (n->left)
        n = n->left;
    return n;
}

// Delete key, returning the (possibly rebalanced) subtree root
Node* del(Node* n, int k)
{
    if (!n)
        return n; // key not found
    if (k < n->key)
        n->left = del(n->left, k);
    else if (k > n->key)
        n->right = del(n->right, k);
    else
    {
        // 0 or 1 child: replace node with whichever child survives
        if (!n->left || !n->right)
        {
            Node* child = n->left ? n->left : n->right;
            delete n;
            return child; // may be null; that's fine
        }
        // 2 children: swap in the inorder successor, delete it from right subtree
        Node* succ = leftMost(n->right);
        n->key = succ->key;
        n->right = del(n->right, succ->key);
    }
    return n ? fix(n) : n; // refresh height / rebalance on the way up
}

// Inorder print: yields keys in sorted order
void in(Node* n)
{
    if (!n)
        return;
    in(n->left);
    cout << n->key << " ";
    in(n->right);
}

int main()
{
    Node* root = nullptr;
    // LL insertion exercise: 30,20,10 triggers a single right rotation
    for (int k : {30, 20, 10, 15, 25, 40, 50})
    {
        root = ins(root, k);
        in(root);
        cout << "\n";
    }
    root = del(root, 20);
    in(root);
    cout << "\n";
    return 0;
}
