import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(x, y):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Learning Curve')
    plt.xlabel('n Gen')
    plt.ylabel('Score')
    plt.plot(x)
    plt.plot(y)
    plt.ylim(ymin=0)
    plt.text(len(x)-1,x[-1], str(x[-1]))
    plt.text(len(y)-1,y[-1], str(y[-1]))
    plt.grid()
    plt.show(block=False)
    plt.pause(0.1)  # Pause to allow the plot to update
