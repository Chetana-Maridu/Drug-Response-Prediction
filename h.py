import matplotlib.pyplot as plt

# Data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create the plot
plt.plot(x, y, marker='o', color='b', linestyle='-')

# Add title and labels
plt.title("Basic Plot Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Show grid
plt.grid(True)

# Display the plot
plt.show()
