import numpy as np

## source data
vector1 = [1.1,0.0,-3.0,4.23,-5.0,6.0]
vector2 = [-6,4.2,3.33,-2,7,0]
vector3 = [3,-4,-0.9,7,0,4]

x = np.array([vector1, vector2,vector3])
#print(x)
#print(x.shape)
#print("")
x = np.append(x, [[1,2,3,4,5,6]], axis=0)  # works
#print(x)
#print(x.shape)
#exit(0)
#m1 = np.array([vector1, vector2])
#print(np.transpose(m1))

# zero_matrix = np.zeros((3,4))  # arbitrary matrix.  all its entries are zero.  its shape is arbitrary as it will be overwritten.
music_matrix = np.array([[]])
print(music_matrix.size)
print(music_matrix.shape)

# for checking vector elements are numbers and not strings.
def is_number(a):
    # will be True also for 'NaN'
    try:
        number = float(a)  # if it can be cast to float, then we'll say it IS a number.
        return True
    except ValueError:
        return False


def add_vector(new_vector):

    global music_matrix

    if not (isinstance(new_vector,list)):
        print("The vector must be a Python list.")
        print(f"Bad dog: {new_vector}.  It's type is {type(new_vector)}.")
        exit(-1)

    print(f"The vector {new_vector} is indeed a list...")

    if not (all(is_number(each_element) for each_element in new_vector)):
        print("The vector must be made up of real numbers")
        print(f"Bad dog: {new_vector}.  It probably contains strings or something.")
        exit(-1)

    if (music_matrix.size == 0):  # check if they are same matrix.  numpy's version of close-enough is good-enough.
        music_matrix = np.array(np.transpose([new_vector]))  # overwrite music_matrix as a new array seeded with new_vector.
        print("New Matrix:")
        print(music_matrix)
        #print("New datatype (should be numpy.ndarray):")
        #print(type(music_matrix))

    else:

        matrix_row_length = np.shape(music_matrix)[0]
        vector_length = np.shape(np.transpose(np.array([new_vector])))[0]
        print(f"matrix row length: {matrix_row_length}")
        print(f"vector length: {vector_length}")

        if (len(new_vector) != matrix_row_length):   # np.shape()[0] is # of rows and np.shape()[1] is # of columns.
            print("The vector must be of same dimensionality as all other vectors.")
            print(f"Bad dog: {new_vector}.  Matrix expects dim {matrix_row_length} and this vector is dim {len(new_vector)}")
            exit(-1)

        else:  # ok everything cool. Stand the vector up on its feet and append it as a new column onto the music_matrix.
            print("About to create modified matrix with...")
            print(music_matrix)
            print("and")
            new_col = np.transpose(np.array([new_vector]))
            print(new_col)
            music_matrix = np.append(music_matrix, new_col, axis = 1)
            print("Modified Matrix:")
            print(music_matrix)

## create matrix
print(type(music_matrix))

add_vector(vector1)
print(type(music_matrix))

add_vector(vector2)
print(type(music_matrix))

add_vector(vector3)
print(type(music_matrix))

print("The vectors are columns of this matrix:")
print(music_matrix)

