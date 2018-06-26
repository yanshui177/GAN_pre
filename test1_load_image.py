# -*-coding:utf-8
import matplotlib.pyplot as plt
import numpy.ma as npm
import numpy as np
import cv2


class data:
    def __init__(self, addr):
        self.img = cv2.imread('./261068_2.jpg')
        pos_num, pos = self.read_pts(addr=addr)
        x1, y1, x2, y2, pos = self.get_margin(pos)
        # face_img = self.get_face(self.img, x1, y1, x2, y2)
        # cv2.imshow('22', face_img)  # cv2.imwrite('22.jpg', face_img)

        mask = self.create_mask(pos)
        cv2.imshow('2211', mask)  # cv2.imwrite('22.jpg', face_img)
        cv2.waitKey(0)

    def read_pts(self, addr):
        f2 = open(addr, "r")
        lines = f2.readlines()
        pos_num = 0
        pos = []
        flag = 0
        for line3 in lines:
            if line3.find('n_points')+1:
                pos_num = int(line3.split(' ')[-1])
            if line3.find('{')+1:
                flag += 1
                continue
            if line3.find('}')+1:
                break
            if flag:
                pos.append([int(round(float(line3.split(' ')[0]))), int(round(float(line3.split(' ')[1])))])
        return pos_num, np.array(pos)

    def get_margin(self, pos):
        x2, y2 = np.max(pos, 0)
        x1, y1 = np.min(pos, 0)
        pos -= [x1, y1]
        return [int(x1), int(y1), int(x2), int(y2), pos]

    def get_face(self, img, x1, y1, x2, y2):
        hight = y2 - y1
        width = x2 - x1
        return img[y1:y1 + hight, x1:x1 + width]

    def create_mask(self, pos):
        width, height = np.max(pos, 0)
        img = np.zeros((height, width, 3), dtype=np.uint8)
        print(pos)
        cv2.circle(img, (20,20), 10,(0, 0, 255), thickness=3)
        return img


if __name__ == "__main__":
    addr = "./261068_2.pts"
    data1 = data(addr)
