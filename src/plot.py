import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time

def plot_data():
	y = []
	data = []
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	fig.text(0.5, 0.95, 'Customer Emotion Diagram', ha='center', va='center')
	fig.text(0.5, 0.04, 'Time', ha='center', va='center')
	fig.text(0.06, 0.5, 'Angry Level', ha='center', va='center', rotation='vertical')

	def update(i):
	    data = read_data()
	    yi = float(data[i])
	    y.append(yi)
	    x = range(len(y))
	    ax.clear()
	    ax.plot(x, y)
	    time.sleep(1)

	a = anim.FuncAnimation(fig, update, frames=35, repeat=False)
	plt.show()

def read_data():
	file = open("data.txt", "r")
	dataStr = file.read()
	file.close()
	return dataStr.split(",")

time.sleep(7.5)
plot_data()