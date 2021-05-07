import numpy as np          # mathematical library, particularly matrixes and matrix calcs.
import pandas as pd       # use pandas for manipulating dataframes
from scipy import spatial   # use for computing similarity of vectors
from scipy.spatial import distance   # use for computing similarity of vectors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_distances
from functools import reduce

#################################################################################
# Module name: similarity_calc_demo2
#################################################################################
# Description:
#   This module does same as its predecesor, "similarity_calc_demo1" but
#   formalizes the code by putting all m=7 vectors each with size n=6 and
#   put them into a single matrix ("n x m" matrix = "n rows, m columns").
#
#   When we do similarity on vectors we can now do it more generally rather
#   than reference expicit vectors "vector1", "vector2", etc.  Imagine if
#   we have 3000 vectors.  Your wrists will get too sore writing them all out.
#
#   Also, we will be sourcing our data from Wikidata API calls.  We dont know
#   how much data they will return so its easiest just to have a program that
#   can read in "m" vectors and not get too fussed about the value of m.
#
#   As for the value of "n" (the size of each vector) we'll see that we need
#   more and more dimensions as we figure out what will give us the best results.
##################################################################################

music_matrix = np.array([[]])  # start with empty matrix of size 0.

# for checking vector elements are numbers and not strings.
def is_number(a):
    # will be True also for 'NaN'
    try:
        number = float(a)  # if it can be cast to float, then we'll say it IS a number.
        return True
    except ValueError:
        return False

# create a handy function that adds vectors to our music matrix.
def add_vector(new_vector):

    global music_matrix


    if not (isinstance(new_vector,list)):
        print("The vector must be a Python list.")
        print(f"Bad dog: {new_vector}.  It's type is {type(new_vector)}.")
        exit(-1)

    if not (all(is_number(each_element) for each_element in new_vector)):
        print("The vector must be made up of real numbers")
        print(f"Bad dog: {new_vector}.  It probably contains strings or something.")
        exit(-1)

    matrix_size = music_matrix.size

    if (matrix_size == 0):  # check if they are same matrix.  numpy's version of close-enough is good-enough.
        music_matrix = np.transpose(np.array([new_vector]))  # overwrite music_matrix as a new array seeded with new_vector.

    else:

        matrix_row_length = np.shape(music_matrix)[0]

        if (len(new_vector) != matrix_row_length):   # np.shape()[0] is # of rows and np.shape()[1] is # of columns.
            print("The vector must be of same dimensionality as all other vectors.")
            print(f"Bad dog: {new_vector}.  Matrix expects dim {matrix_row_length} and this vector is dim {len(new_vector)}")
            exit(-1)

        else:  # ok everything cool. Stand the vector up on its feet and append it as a new column onto the music_matrix.
            new_col = np.transpose(np.array([new_vector]))  # this is actually a matrix not a column but it's vertical.
            music_matrix = np.append(music_matrix, new_col, axis = 1)


def load_data():

    ########################################################################
    ## Source data (assumes it is already converted to a vector)
    ########################################################################
    vector1 = [1.1,0.0,-3.0,4.23,-5.0,6.0]
    vector2 = [-6,4.2,3.33,-2,7,0]
    vector3 = [3,-4,-0.9,7,0,4]   # this is fine.
    # these two vectors are 90 degrees to one another (note how they dont share any dimensional values)
    ##vector4 = [0,1,1,0,1,0]  # for testing
    ##vector5 = [0,0,0,1,0,0]  # for testing
    vector4 = [0, 4, 1, 0, 3, 0]
    vector5 = [0, 0, 0, 5, 0, 0]

    # here are two very similar vectors. Their angle should be small.
    vector6 = [1.0,2.0,3.0,-4.0,5.0,-6.0]
    vector7 = [1.1,1.5,3.3,-4.4,5.5,-8.0]

    ########################################################################
    ## Convert vectors to matrix, for processing generality
    ## (Getting code ready for when we have m=10000 vectors)
    ########################################################################
    add_vector(vector1)
    add_vector(vector2)
    add_vector(vector3)
    add_vector(vector4)
    add_vector(vector5)
    add_vector(vector6)
    add_vector(vector7)

    print("\nThe raw vectors are assembled as the columns of this matrix:")
    print(music_matrix)


def calculate_similarities():

    ########################################################################
    ## calculate similarities, pairwise.
    ########################################################################

    # We will create a similarity matrix - cell (r,c) in matrix will be comparing vector "r" with vector "c".
    # Since similarity of cell(r,c) will equal similarity of cell(c,r) and since I dont care about
    # similarity(c,c) I only look at the upper triangle of the matrix, using np.triu()
    # https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat

    a = music_matrix
    n = np.linalg.norm(a, axis=0).reshape(1, a.shape[1])
    cosine_sims = (a.T.dot(a) / n.T.dot(n))  # calculate cosine similarity.  libraries also exist which calc this tho
    np.fill_diagonal(cosine_sims, 1.0)       # the formula above is putting floating point numbers slightly above 1.000 which is impossible.

    ###The calc from cosine_similarity() was saying that vectors 4 and 5 werent orthogonal, so i used the linalg calc above, instead.
    ###similarity_matrix = np.degrees(np.arccos(cosine_similarity(music_matrix))) # may require music_matrix to be cast as numpy sparse array.

    similarity_matrix = np.degrees(np.round(np.arccos(cosine_sims),2)) # may require music_matrix to be cast as numpy sparse array.
    similarity_matrix = np.round(np.triu(similarity_matrix),1)  # just keeping data in upper triangle of matrix, rest is ignorable.
    print('\nHere are the Pairwise similarities, in degrees:\n {}'.format(similarity_matrix))

    ## convert similarities to tuples
    a = similarity_matrix

    # I add (+1) so that vectors arent numbered 0..(n-1) but instead 1..(n)
    list_of_tuples = [(ix+1,iy+1, a[ix,iy]) for ix, row in enumerate(a) for iy, i in enumerate(row) if ix<iy]

    #print("Similarity Tuples:")
    #print(list_of_tuples)

    return list_of_tuples


def pretty_print(vector):

    pretty_string = "[" + reduce(lambda x, y: str(x) + ", " + str(y), vector) + "]"

    return pretty_string


def interpret_similarities(list_of_tuples):

    ## Each tuple is of the form: (vectorA, vectorB, similarity(vectorA,vectorB))

    sorted_tuples = sorted(list_of_tuples, key=lambda x: x[2])
    print("\nHere ar the SORTED pairwise tuples of format (v1,v2,similarity(v1,v2):")
    print(f"{sorted_tuples}")
    print(f"  ^  ^  ^^^^ : the most similar vectors and the angle between them!")

    # Convert matrix of original vectors to dataframe just so we can print them easier.

    df_matrix = pd.DataFrame(music_matrix)
    #df_matrix = pd.DataFrame(np.transpose(music_matrix))
    #print(df_matrix)  # for debug

    # I subtract (-1) because pandas expects indices numbered 0..(n-1), not 1..(n)
    vectorA = df_matrix.iloc[:, sorted_tuples[0][0]-1].values.tolist()
    vectorB = df_matrix.iloc[:, sorted_tuples[0][1]-1].values.tolist()
    similarity_AB = sorted_tuples[0][2]

    print(f"\nThe most similar pair of vectors have an angle of {similarity_AB} degrees between them:")
    print(f"Vector #{str(sorted_tuples[0][0])}: {vectorA}")
    print(f"Vector #{str(sorted_tuples[0][1])}: {vectorB}")


if __name__ == '__main__':

    load_data()

    #returns tuples: (vectorA, vectorB, similarity(vectorA, vectorB)
    list_of_tuples = calculate_similarities()

    # Final step is to conclude which vectors are most/least similar.
    interpret_similarities(list_of_tuples)
