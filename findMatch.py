import cv2
import numpy as np
import math
import sys

from Graph import Graph, Node
from tracker import *


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

    g.save_to_json(filename.split('.')[0])
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


# p1b = g1.nodes[edge1.getP1()].getB() / g1.avgB
# p2b = g1.nodes[edge1.getP2()].getB() / g1.avgB
# p3b = g2.nodes[edge2.getP1()].getB() / g2.avgB
# p4b = g2.nodes[edge2.getP2()].getB() / g2.avgB

def match_stars(g1, g2, file1, file2, dir_detected, dir_matched):
    # eps = 0.00009 / min(g1.get_min_dist(), g2.get_min_dist())
    eps = 0.009
    eps2 = 5
    print(eps)
    tups = []
    l1 = []
    l2 = []
    for edge1 in g1.get_all_edges():
        for edge2 in g2.get_all_edges():
            if abs(edge1.getDist() - edge2.getDist()) < eps:
                tups.append((edge1, edge2))
    for tup1, tup2 in zip(tups[::2], tups[1::2]):
        if tup1[0].m / tup2[0].m - tup1[1].m / tup2[1].m < eps2:
            print(
                f'Star {tup1[0].getP1()} and star {tup1[0].getP2()} in image1 EQUALS to Star {tup1[1].getP1()} and star {tup1[1].getP2()} in image2')
            l1.append((tup1[0].getP1(), tup1[0].getP2()))
            l2.append((tup1[1].getP1(), tup1[1].getP2()))

            print(
                f'Star {tup2[0].getP1()} and star {tup2[0].getP2()} in image1 EQUALS to Star {tup2[1].getP1()} and star {tup2[1].getP2()} in image2')
            l1.append((tup2[0].getP1(), tup2[0].getP2()))
            l2.append((tup2[1].getP1(), tup2[1].getP2()))

    drawLine(g1, l1, filename=file1, dir_src=dir_detected, dir_dest=dir_matched)
    drawLine(g2, l2, filename=file2, dir_src=dir_detected, dir_dest=dir_matched)


def run_all(img1, img2, dir_src):
    dir_images = dir_src
    dir_detected = 'detected_stars'
    dir_matched = 'matched_stars'
    dir_log = 'logs'
    dir_json = 'graphs'
    make_dirs([dir_images, dir_detected, dir_matched, dir_log, dir_json])
    dataset = os.listdir(dir_json)
    j1 = img1.split('.')[0] + '.json'
    j2 = img2.split('.')[0] + '.json'
    if j1 in dataset:
        g1 = Graph(file_name=j1, dir=dir_json)
    else:
        stars1 = detect_img(img1, dir_images, dir_detected, dir_log)
        g1 = buildGraph(stars1, filename=img1, dir=dir_json)
    if j2 in dataset:
        g2 = Graph(file_name=j2, dir=dir_json)
    else:
        stars2 = detect_img(img2, dir_images, dir_detected, dir_log)
        g2 = buildGraph(stars2, filename=img2, dir=dir_json)
    match_stars(g1, g2, file1=img1, file2=img2, dir_detected=dir_detected, dir_matched=dir_matched)


if __name__ == '__main__':
    dir_src = 'images'
    make_dirs([dir_src])
    dataset = os.listdir(dir_src)
    file1 = 'fr1.jpg'
    file2 = 'fr2.jpg'
    if len(sys.argv) > 1:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        run_all(file1, file2, dir_src)
    else:
        print("images:")
        for i in range(len(dataset)):
            print(f"{i + 1}: {dataset[i]}")
        input1 = input("input the number of the first image\n")
        if int(input1) - 1 in range(len(dataset)):
            input2 = input("input the number of the second image\n")
            if int(input2) - 1 in range(len(dataset)):
                run_all(img1=dataset[int(input1) - 1], img2=dataset[int(input2) - 1], dir_src=dir_src)
