import time
import csv
from decision_tree import DecisionTree


"""
Load data from csv
"""
def load_csv(path):
    data = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  
        for row in reader:
            processed = []
            for value in row:
                if value.isdigit():
                    processed.append(int(value))
                else:
                    processed.append(value)
            data.append(processed)
    return data, headers

"""
Read data from CSV
"""
data, attributes = load_csv("trainData.csv")
datatest, _ = load_csv("testData.csv")  

"""
Tain and Analyze
"""
for method in ["gini", "entropy"]:
    print(f"\n==== Decision Tree using {method.upper()} ====")

    dtree = DecisionTree(method=method)

    start_time = time.time()
    dtree.fit(data, attributes)
    end_time = time.time()

    # Print tree
    dtree.print_tree()

    # Predict
    preds = dtree.predict(datatest)
    actual = [row[-1] for row in datatest]

    print("\nTest Predictions:", preds)
    print("Actual Labels:   ", actual)
    print("Accuracy:", dtree.accuracy(preds, actual))

    # Count nodes
    num_nodes = dtree.count_nodes()

    print("Number of nodes in tree:", num_nodes)
    print("Training runtime: {:.10f} seconds".format(end_time - start_time))
