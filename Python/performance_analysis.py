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


x = ["Easy", "Medium", "Hard"]
y_1 = [0.2775, 0.0594, 0.08]
y_2 = [0.2687, 0.0571, 0.0743]
draw_line(x, y_1, y_2)