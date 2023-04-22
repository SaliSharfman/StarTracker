import cv2
import numpy as np
import math
import sys

from Graph import Graph, Node
from tracker import *


def drawLine(filename, g, l):
    dir_src = "detected_stars"
    dir_dest = "matched_stars"
    try:
        img = cv2.imread(f'{dir_src}\{filename}')
        img_copy = img.copy()  # Make a copy of the original image
    except:
        print(f"cant open file {filename}")
        return
    for i in l:
        pos1 = tuple(map(int, g.nodes[i[0]].getLocation()))
        pos2 = tuple(map(int, g.nodes[i[1]].getLocation()))
        cv2.line(img_copy, pos1, pos2, (0, 255, 0), 1)
    cv2.imwrite(f'{dir_dest}\detected_{filename}', img_copy)



def buildGraph(stars: list, filename: str, dir: str = ''):
    if dir != '':
        filename = f'{dir}/{filename}'
    g = Graph()
    for i, _, _, _, _ in stars:
        if i == len(stars):
            break
        pos = (stars[i][1], stars[i][2])
        r = stars[i][3]
        b = stars[i][4]
        p = Node(i, pos, r, b)
        g.add_node(p)

    for i in g.nodes:
        for j in g.nodes:
            if i == j:
                continue
            g.add_edge(i, j)
    g.save_to_json(filename)
    return g


def drawLine(g, l, filename, dir_src, dir_dest):
    print(filename)
    print(dir_src)
    try:
        img = cv2.imread(f'{dir_src}/detected_{filename}')
        img_copy = img.copy()  # Make a copy of the original image
    except:
        print(f"cant open file {filename}")
        return
    for i in l:
        pos1 = tuple(map(int, g.nodes[i[0]].getLocation()))
        pos2 = tuple(map(int, g.nodes[i[1]].getLocation()))
        cv2.line(img_copy, pos1, pos2, (0, 255, 0), 1)

    cv2.imwrite(f'{dir_dest}/{filename}', img_copy)


def match_stars(g1, g2, file1, file2, dir_detected, dir_matched):
    # eps = 0.00009 / min(g1.get_min_dist(), g2.get_min_dist())
    eps = 0.009
    print(eps)
    l1 = []
    l2 = []
    for edge1 in g1.get_all_edges():
        for edge2 in g2.get_all_edges():
            if abs(edge1.getDist() - edge2.getDist()) < eps:
                print(
                    f'Star {edge1.getP1()} and star {edge1.getP2()} in image1 EQUALS to Star {edge2.getP1()} and star {edge2.getP2()} in image2')
                l1.append((edge1.getP1(), edge1.getP2()))
                l2.append((edge2.getP1(), edge2.getP2()))
    drawLine("detected_fr1.jpg", g1, l1)
    drawLine("detected_fr2.jpg", g2, l2)


if __name__ == '__main__':
    dir_src = 'images'
    make_dirs([dir_src])
    dataset = os.listdir(dir_src)
    file1 = 'fr1.jpg'
    file2 = 'fr2.jpg'
    if len(sys.argv) > 1:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        run_all(file1, file2)
    else:
        print("images:")
        for i in range(len(dataset)):
            print(f"{i + 1}: {dataset[i]}")
        input1 = input("input the number of the first image\n")
        if int(input1) - 1 in range(len(dataset)):
            input2 = input("input the number of the second image\n")
            if int(input2) - 1 in range(len(dataset)):
                run_all(img1=dataset[int(input2) - 1], img2=dataset[int(input2) - 1])
