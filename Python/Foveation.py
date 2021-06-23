import sys
import metavision_designer_engine as mvd_engine
import numpy as np
from metavision_designer_engine import Controller, KeyboardEvent
import metavision_designer_cv as mvd_cv
import metavision_designer_core as mvd_core
import metavision_hal as mv_hal
import cv2
from Python.EventProcessor import EventProcessor


def for_int(i, j, k, l, a, b, n_matrix, matrix, divide_size_by):
    n_matrix[i][j] += matrix[a][b]
    return n_matrix[i][j]


def for_tab(i, j, k, l, a, b, n_matrix, matrix, divide_size_by):
    if n_matrix[i][j] is 0:
        n_matrix[i][j] = []
    n_matrix[i][j].append(matrix[a][b])
    return n_matrix[i][j]


# ça me semble pas encore juste, ne gére pas plusieur événement dans une seul case
def for_event(i, j, k, l, a, b, n_matrix, matrix, divide_size_by):
    # event format (x, y, polarity, timestamp)
    if n_matrix[i][j] is 0:
        n_matrix[i][j] = (0, 0, 0, 0)
    event = matrix[a][b]
    # convertie en pourcentage ((100 / (divide_size_by * divide_size_by)) / 100)
    n_matrix[i][j] = (i, j, n_matrix[i][j][2] + event[2] * ((100 / (divide_size_by * divide_size_by)) / 100), n_matrix[i][j][3] + event[3])
    if k == divide_size_by-1 and l == divide_size_by-1:
        n_matrix[i][j][3] = int(n_matrix[i][j][3] / (divide_size_by**2))
    return n_matrix[i][j]


FOR_INT = for_int
FOR_TAB = for_tab
FOR_EVENT = for_event


def high_to_low_resolution(matrix, divide_size_by, fonction):
    n_matrix = np.zeros((int(len(matrix) / divide_size_by), int(len(matrix[0]) / divide_size_by)))  # np.empty
    for i in range(len(n_matrix)):
        for j in range(len(n_matrix[0])):

            for k in range(divide_size_by):
                for l in range(divide_size_by):
                    a = (divide_size_by * i) + k
                    b = (divide_size_by * j) + l
                    # print('i={}   j={}   k={}   l={}   a={}   b={}'.format(i, j, k, l, a, b))
                    n_matrix[i][j] = fonction(i, j, k, l, a, b, n_matrix, matrix, divide_size_by)
    return n_matrix


def convert_bool_matrix_to_int_matrix(matrix):
    # matrix_bool = np.zeros((roi_width, roi_height), dtype=bool)
    matrix_int = np.zeros((len(matrix), len(matrix[0])))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                matrix_int[i][j] = 1
    return matrix_int


def scan_for_event_density(matrix_event, threshold=1):
    matrix_bool = np.zeros((len(matrix_event), len(matrix_event[0])), dtype=bool)
    for i in range(len(matrix_event)):
        for j in range(len(matrix_event[i])):
            if matrix_event[i][j] >= threshold:
                matrix_bool[i][j] = True
    return matrix_bool