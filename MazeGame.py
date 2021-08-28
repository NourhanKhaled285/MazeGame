from math import sqrt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from csv import reader
from math import sqrt
import random
import pygame
import random
import sys
import math
from collections import deque
from queue import LifoQueue




# region SearchAlgorithms
class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.

    maze = ""
    rows_num = 1
    columns_num = 0

    def __init__(self, mazeStr):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.maze = mazeStr

    def convert_to_2Darray(self):
        for i in range(len(self.maze)):
            if (self.maze[i] == ' '):
                self.rows_num += 1
        for i in range(len(self.maze)):
            if (self.maze[i] == ' '):
                break
            if (self.maze[i] != ','):
                self.columns_num += 1

        arr2D = np.array([[str(j) for j in i.split(',')] for i in self.maze.split(' ')])

        return arr2D

    def create_nodes(self):

        arr = self.convert_to_2Darray()

        node_list = []

        for i in range(self.rows_num):
            row = []
            for j in range(self.columns_num):
                nod = Node(0)
                row.append(nod)
            node_list.append(row)

        for i in range(self.rows_num):
            for j in range(self.columns_num):
                node_list[i][j].value = arr[i][j]

        counter2 = 0

        for i in range(self.rows_num):
            for j in range(self.columns_num):
                node_list[i][j].id = counter2
                counter2 += 1

        for i in range(self.rows_num):
            for j in range(self.columns_num):

                if (j == 0):
                    node_list[i][j].left = None
                else:
                    node_list[i][j].left = node_list[i][j - 1].id
                if (i == 0):
                    node_list[i][j].up = None
                else:
                    node_list[i][j].up = node_list[i - 1][j].id
                if (i == self.rows_num - 1):
                    node_list[i][j].down = None
                else:
                    node_list[i][j].down = node_list[i + 1][j].id
                if (j == self.columns_num - 1):
                    node_list[i][j].right = None
                else:
                    node_list[i][j].right = node_list[i][j + 1].id
        return node_list

    def DFS(self):
        node_list_maze = self.create_nodes()
        stack = []
        i = 0
        j = 0
        start_position = node_list_maze[0][0]
        node_list_maze[0][0].previousNode = -1

        stack.append(start_position)
        while len(stack) != 0:
            current_position = stack.pop()
            self.fullPath.append(current_position.id)
            i = current_position.id // self.columns_num
            j = current_position.id % self.columns_num

            if (current_position.value == 'E'):

                break

            if (current_position.right != None and node_list_maze[i][ j + 1].value != '#' and current_position.right not in self.fullPath):
                node_list_maze[i][j + 1].previousNode = current_position.id
                stack.append(node_list_maze[i][j + 1])

            if (current_position.left != None and node_list_maze[i][j - 1].value != '#' and current_position.left not in self.fullPath):
                node_list_maze[i][j - 1].previousNode = current_position.id
                stack.append(node_list_maze[i][j - 1])

            if (current_position.down != None and node_list_maze[i + 1][j].value != '#' and current_position.down not in self.fullPath):
                node_list_maze[i + 1][j].previousNode = current_position.id
                stack.append(node_list_maze[i + 1][j])

            if (current_position.up != None and node_list_maze[i - 1][ j].value != '#' and current_position.up not in self.fullPath):
                node_list_maze[i - 1][j].previousNode = current_position.id
                stack.append(node_list_maze[i - 1][j])


        # get path = direct path
        first = self.fullPath[0]
        self.path.append(first)

        for k in range(1, len(self.fullPath)):
            m = first // self.columns_num
            n = first % self.columns_num
            if (first < self.fullPath[k]):
                self.path.append(self.fullPath[k])
                first = self.fullPath[k]
            else:

              first_node = node_list_maze[m][n]

              if (self.fullPath[k]!=first_node.left  and first_node.up != self.fullPath[k]):
                self.path.pop()
                previous_of_first = first_node.previousNode

                m1 = previous_of_first // self.columns_num
                n1 = previous_of_first % self.columns_num
                previous_node_of_first = node_list_maze[m1][n1]


                while first_node.previousNode > self.fullPath[k] and previous_node_of_first.left != self.fullPath[k] \
                   and previous_node_of_first.up != self.fullPath[k]:
                            if (len(self.path) != 0):
                                y = self.path.pop()
                                m2 = y // self.columns_num
                                n2 = y % self.columns_num
                                first_node = node_list_maze[m2][n2]

                                m1 = first_node.previousNode // self.columns_num
                                n1 = first_node.previousNode % self.columns_num
                                previous_node_of_first = node_list_maze[m1][n1]
                self.path.append(self.fullPath[k])
                first = self.fullPath[k]
              else:

                    self.path.append(self.fullPath[k])
                    first = self.fullPath[k]
        return self.fullPath, self.path


# endregion

#################################### Algorithms Main Functions #####################################
# region Search_Algorithms_Main_Fn
def SearchAlgorithm_Main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    fullPath, path = searchAlgo.DFS()
    print('**DFS**\n Full Path is: ' + str(fullPath) +'\n Path is: ' + str(path))

# endregion

######################## MAIN ###########################33
if __name__ == '__main__':

    SearchAlgorithm_Main()
