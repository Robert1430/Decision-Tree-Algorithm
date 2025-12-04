import math

"""
Node class
"""
class Leaf:
    def __init__(self, rows):
        counts = {}
        for r in rows:
            lbl = r[-1]
            counts[lbl] = counts.get(lbl, 0) + 1
        self.prediction = max(counts, key=counts.get)

class DecisionNode:
    def __init__(self, col, value, left, right):
        self.col = col
        self.value = value
        self.left = left
        self.right = right

"""
Decision Tree Class
"""
class DecisionTree:
    def __init__(self, method="gini"):
        """
        method: "gini" for Gini index, "entropy" for information gain
        """
        self.method = method
        self.tree = None
        self.attributes = None

    """
    Calculate the Gini impurity.
    Equation:
        Gini = 1 - Σ(p_i²)
    where p_i is the probability of each class label.
    """
    def gini(self, rows):
        counts = {}
        for row in rows:
            label = row[-1]
            counts[label] = counts.get(label, 0) + 1
        impurity = 1
        total = len(rows)
        for lbl in counts:
            p = counts[lbl] / total
            impurity -= p ** 2
        return impurity

    """
    Calculate the entropy of the dataset.
    Equation:
        Entropy = - Σ(p_i * log₂(p_i))
    where p_i is the probability of each class label.
    """
    def entropy(self, rows):
        counts = {}
        for row in rows:
            label = row[-1]
            counts[label] = counts.get(label, 0) + 1
        total = len(rows)
        ent = 0
        for lbl in counts:
            p = counts[lbl] / total
            ent -= p * math.log2(p)
        return ent
    
    """
    splits rows into left or right groups based on column value
    """
    def split(self, rows, col, value):
        left, right = [], []
        for row in rows:
            if row[col] == value:
                left.append(row)
            else:
                right.append(row)
        return left, right

    """
    Calculate total impurity of a split, weighted by group
    """
    def weighted_impurity(self, left, right):
        total = len(left) + len(right)
        if total == 0:
            return 0
        if self.method == "gini":
            return (len(left)/total)*self.gini(left) + (len(right)/total)*self.gini(right)
        else:
            return (len(left)/total)*self.entropy(left) + (len(right)/total)*self.entropy(right)

    """
    Calculate how much impurity is reduced after a split
    """
    def information_gain(self, left, right, current_imp):
        total = len(left) + len(right)
        if total == 0:
            return 0
        p = len(left) / total
        return current_imp - (p * self.entropy(left) + (1 - p) * self.entropy(right))

    """
    Find the best column and value to split the dataset.
    This function evaluates every possible split across all features and all unique values,
    then selects the one that either maximizes information gain (for entropy) or minimizes
    weighted impurity (for Gini).
    Returns:
        best_col (int): Index of the best feature to split on
        best_value: Value of the feature to split on
        best_sides (tuple): Tuple of two lists (left_rows, right_rows) after the split
    """
    def find_best_split(self, rows):
        
        if (self.method == "gini"):
            best_score = 999999
        else:
            best_score = -999999
        
        best_col = None
        best_value = None
        best_sides = None

        if self.method == "entropy":
            current_impurity = self.entropy(rows)
        else:
            None

        features = len(rows[0])-1

        for col in range(features):
            values = set(row[col] for row in rows)
            
            for val in values:
                left, right = self.split(rows, col, val)
                
                if len(left) == 0 or len(right)==0:
                    continue

                if self.method == "entropy":
                    gain = self.information_gain(left,right, current_impurity)
                    if gain > best_score:
                        best_score = gain
                        best_col = col
                        best_value = val
                        best_sides = (left, right)
                else:
                    impurity = self.weighted_impurity(left, right)
                    if impurity < best_score:
                        best_score = impurity
                        best_col = col
                        best_value = val
                        best_sides = (left, right)
        return best_col, best_value, best_sides
                    
                
    """
    Recursively buil a decision tree fromt he dataset
    """
    def build_tree(self, rows):
        col, value, sides = self.find_best_split(rows)
        if col is None:
            return Leaf(rows)
        left, right = sides
        left_branch = self.build_tree(left)
        right_branch = self.build_tree(right)
        return DecisionNode(col, value, left_branch, right_branch)

    """
    Stores the attribute names and builds the decision tree
    """
    def fit(self, rows, attributes):
        self.attributes = attributes
        self.tree = self.build_tree(rows)

    """
    Predict the label for a single row using the decision tree.
    """    
    def predict_row(self, row, node=None):
        if node is None:
            node = self.tree
        if isinstance(node, Leaf):
            return node.prediction
        if row[node.col] == node.value:
            return self.predict_row(row, node.left)
        else:
            return self.predict_row(row, node.right)

    """
    Predicts multiple rows
    """
    def predict(self, rows):
        return [self.predict_row(row) for row in rows]

    """
    calculate the accuraty of predictions
    """
    def accuracy(self, preds, actual):
        correct = sum(1 for p,a in zip(preds, actual) if p==a)
        return correct / len(actual)

    """
    Counts the total number of nodes in the decision tree
    """
    def count_nodes(self, node=None):
        if node is None:
            node = self.tree
        if isinstance(node, Leaf):
            return 1
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    """
    Prints a readable format of the decision tree 
    """
    def print_tree(self, node=None, header=None, indent=""):
        if node is None:
            node = self.tree
        if isinstance(node, Leaf):
            if header is not None:
                print(f"{indent}{header} : {node.prediction}")
            else:
                print(f"{indent}{node.prediction}")
            return
        if header is not None:
            print(f"{indent}{header}")
            new_indent = indent + "| "
        else:
            new_indent = ""
        current_label = f"{self.attributes[node.col]} = {node.value}"
        self.print_tree(node.left, current_label, new_indent)
        not_equal_label = f"{self.attributes[node.col]} != {node.value}"
        self.print_tree(node.right, not_equal_label, new_indent)
