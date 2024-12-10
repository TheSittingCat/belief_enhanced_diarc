import matplotlib.pyplot as plt

def draw_line(x, y_1, y_2) : 
    fig, ax = plt.subplots()
    ax.plot(x, y_1, label='Partial Match Accuracy')
    ax.plot(x, y_2, label='Jaccard Index')
    ax.set_xlabel('Difficulty')
    ax.set_ylabel('Accuracy')
    ax.set_title('Partial Match Accuracy and Jaccard Index by Difficulty')
    ax.legend()
    plt.show()

def draw_line_triplet(x, y_1, y_2, y_3) : 
    fig, ax = plt.subplots()
    ax.plot(x, y_1, label='Exact Match Accuracy')
    ax.plot(x, y_2, label='Partial Match Accuracy')
    ax.plot(x, y_3, label='Jaccard Index')
    ax.set_xlabel('Difficulty')
    ax.set_ylabel('Accuracy')
    ax.set_title('Exact Match Accuracy, Partial Match Accuracy, and Jaccard Index by Difficulty')
    ax.legend()
    plt.show()


x = ["Easy", "Medium", "Hard"]
y_1 = [0.88, 0.56, 0.36]
y_2 = [0.9545, 0.8053, 0.6374]
y_3 = [0.9223, 0.7336, 0.5803]
draw_line_triplet(x, y_1, y_2, y_3)