# Import libraries
import numpy as np


# Creating dataset
a = np.random.randint(100, size =(50))
print(a)

hist, bins = np.histogram(a, bins = [0,5])

# printing histogram
print()
print (hist)
print (bins)
print()
