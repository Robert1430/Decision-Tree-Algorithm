# Decision-Tree-Algorithm
This project implements the Decision Tree algorithm from scratch to predict whether a car is profitable based on its attributes. The methos used to build the decision tree are Gini Index and Information Gain (entropy), without using any built in machine learning libraries. The model is trained on a dataset containing categorical attributes such as price, maintenance, capacity, and airbag, and evaluated on a separate test set.

## Project Structure

    Decision-Tree-Algorithm/
    ├── decision_tree.py       # Decision Tree class  
    ├── main.py               # Main execution script  
    ├── trainData.csv        # Training data   
    └── testData.vcsv         # Test data   

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Clone or download the project files
2. Navigate to the project directory:
```bash
git clone https://github.com/Robert1430/Decision-Tree-Algorithm.git
cd Decision-Tree-Algorithm
```
3. No additional installations needed

## How to Run

1. Navigate to the project directory
2. Execute the main program:
```bash
python main.py
```

## Decision Tree Algorithm  
Decision Trees are supervised learning models used for **classification** and **regression**. The model repeatedly splits the dataset based on features to create the most “pure” subsets possible.

---

### Gini Index (Gini Impurity)

#### **What it Measures**
Gini impurity measures how often a randomly chosen element from the set would be incorrectly labeled if it was randomly labeled according to the distribution of labels.

### **Equation**

    Gini(D) = 1 - Σ(p_i²)

Where:  
- \(C\) = number of classes  
- \(p_i\) = probability of class \(i\) in dataset \(D\)

---

### Information Gain (Entropy)

#### **What it Measures**
Entropy measures the uncertainty in a dataset. Information Gain tells us how much entropy decreases after a split.

#### **Entropy Equation**

    Entropy(D) = - Σ( p_i * log2(p_i) )

#### **Information Gain Equation**

    IG(D, A) = Entropy(D) − Σ( |D_v| / |D| * Entropy(D_v) )

Where:  
- \(A\) = attribute (feature)  
- \(D_v\) = subset where attribute \(A\) takes value \(v\)  

---

## Steps in Building a Decision Tree

#### 1 **Calculate impurity of the parent dataset**
- Use **Gini impurity** or **Entropy**, depending on chosen method.

#### 2️ **For each feature, compute impurity of all possible splits**
- For numerical features: evaluate threshold splits (e.g., `< x`, `>= x`).  
- For categorical features: evaluate group-based splits.

#### 3️ **Compute the weighted impurity after the split**
- Gini: weighted average of Gini impurities  
- Entropy: compute Information Gain

#### 4️ **Select the best split**
- **Gini:** choose the split with **lowest Gini** after split  
- **Entropy:** choose the split with the **highest Information Gain**

#### 5️ **Split the dataset**
- Left subset: samples meeting condition  
- Right subset: samples not meeting condition

#### 6️ **Repeat recursively**
- Continue splitting each child node  
- Until one of the following stopping conditions:
  - All samples belong to one class  
  - Max depth reached  
  - No remaining useful features  
  - Node has too few samples

#### 7️ **Assign class labels**
- Leaf nodes get the majority class of that subset.

## Input
The dataset is read from a **CSV file**.

Each row contains feature values followed by the class label (profitable).  
Below is an example.

### **Training Data Example**
| maintenance | price | capacity | airbag | profitable |
|------------|--------|----------|--------|--------|
| low        | low    | 2        | yes    | yes    |
| low        | med    | 4        | no     | no     |
| .....      |.....   | .        | ...    | ..     |
| .....      |.....   | .        | ...    | ..     |

### **Test Data Example**
| maintenance | price | capacity | airbag | profitable |
|------------|--------|----------|--------|--------|
| med        | low    | 2        | no     | yes    |
| high       | high   | 4        | yes    | yes    |
| .....      |.....   | .        | ...    | ..     |
| .....      |.....   | .        | ...    | ..     |

## output
  Below is an example output produced by the decision tree using **Gini**
  
  Where subsequent levels are at increasing indentations from the left
  
      ==== Decision Tree using GINI ====
      maintenance = low : yes
      maintenance != low
      | capacity = 5 : yes
      | capacity != 5
      | | maintenance = high
      | | | price = high : no
      | | | price != high
      | | | | price = low : no
      | | | | price != low : no
      | | maintenance != high
      | | | price = low : no
      | | | price != low
      | | | | airbag = no : no
      | | | | airbag != no
      | | | | | price = high : yes
      | | | | | price != high : yes
      
      Test Predictions: ['yes', 'yes']
      Actual Labels:    ['yes', 'yes']
      Accuracy: 1.0
      Number of nodes in tree: 17
      Training runtime: 0.0009961128 seconds
