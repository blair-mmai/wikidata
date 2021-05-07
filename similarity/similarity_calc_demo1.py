# import pandas as pd       # use pandas for manipulating dataframes
from scipy import spatial   # use for computing similarity of vectors
import math                 # to calculate angle (in degrees) from the similarity metric.

nbr_dimensions_of_each_vector = 6

vector1 = [1.1,0,-3,4.23,-5,6]
vector2 = [-6,4.2,3.33,-2,7,0]
# vector3 = [9,-9,-9]         # note: the dimensionality of vectors must be same (eg all 6, all 3, or all 1000)
vector3 = [3,-4,-0.9,7,0,4]   # this is fine.

# these two vectors are 90 degrees to one another (note how they dont share any dimensional values)
vector4 = [0,4,1,0,3,0]
vector5 = [0,0,0,5,0,0]

# here are two very similar vectors. Their angle should be small.
vector6 = [1.0,2.0,3.0,-4.0,5.0,-6.0]
vector7 = [1.1,1.5,3.3,-4.4,5.5,-8.0]

print("The vectors are:")
# print(f"{vector1=}")  #this method works but only with Python 3.8 and greater.
print(f"vector1: {vector1}")
print(f"vector2: {vector2}")
print(f"vector3: {vector3}")
print("")
print(f"vector4: {vector4}")
print(f"vector5: {vector5}")
print("")
print(f"vector6: {vector6}")
print(f"vector7: {vector7}")
print("")

## calculate similarities, for some of the pairs.  A better way to do this is by making a matrix with each
# column representing each vector.  I'll demonstrate this later.
similarity12 = 1 - spatial.distance.cosine(vector1, vector2)
similarity23 = 1 - spatial.distance.cosine(vector2, vector3)
similarity13 = 1 - spatial.distance.cosine(vector1, vector3)

# i'll compute the similarity of vector 4 and 5 just to show it's 90 degrees.
similarity45 = 1 - spatial.distance.cosine(vector4, vector5)

# i'll compute the similarity of vector 6 and 7 just to show they're "fairly close to zero" degrees
similarity67 = 1 - spatial.distance.cosine(vector6, vector7)

print("Angles between vectors in degrees (rounded to 1 decimal place):")
print(f"similarity 1-2: {round(math.degrees(math.acos(similarity12)),1)}")
print(f"similarity 2-3: {round(math.degrees(math.acos(similarity23)),1)}")
print(f"similarity 1-3: {round(math.degrees(math.acos(similarity13)),1)}")
print("...So, vectors 1-3 are most similar (pointing in roughly same direction) with an angle between of about 50 degrees.")

print("\n...and just as a test these two should be orthogonal to each other...")
print(f"similarity 4-5: {round(math.degrees(math.acos(similarity45)),1)}")

print("\n...and just as a test these two should be close to each other, i.e. angle 'close' to zero degrees...")
print(f"similarity 6-7: {round(math.degrees(math.acos(similarity67)),1)}")

