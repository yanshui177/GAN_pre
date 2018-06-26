# -*-coding:utf-8
"""
读取人俩图像数据库，自带的有68个特征点，根据人脸特征点的位置
将人脸图像中人脸区域切割，并重新生成一对方形图像，其中人脸特
征点用 图像表示

from 闫帅帅
"""
import numpy as np
import cv2
import os


class data:
    def __init__(self, addr):
        self.addr = addr

        img, pos = self.load_img_and_pts()
        x1, y1, x2, y2, pos_small = self.get_margin(pos)
        face = self.get_face(img, x1, y1, x2, y2)
        mask = self.get_mask(pos_small)
        self.save_img(face, mask)

    def load_img_and_pts(self):
        # load img
        img = cv2.imread(self.addr + '.jpg')
        # load pts
        f2 = open(self.addr+'.pts', "r")
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
        return img, np.array(pos)

    def get_margin(self, pos):
        x2, y2 = np.max(pos, 0)
        x1, y1 = np.min(pos, 0)
        pos -= [x1, y1]
        return [int(x1), int(y1), int(x2), int(y2), pos]

    def get_face(self, img, x1, y1, x2, y2):
        hight = y2 - y1
        width = x2 - x1
        return img[y1:y1 + hight, x1:x1 + width]

    def get_mask(self, pos):
        width, height = np.max(pos, 0)
        img = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(len(pos)):
            cv2.circle(img, (pos[i][0], pos[i][1]), 2, (255, 255, 255), thickness=-1)
        return img

    def save_img(self, img_face, img_mask):
        path_img_face = 'D:/created_data/' + self.addr.split('/')[-1] + '_face.jpg'
        path_img_mask = 'D:/created_data/' + self.addr.split('/')[-1] + '_mask.jpg'
        cv2.imwrite(path_img_face, img_face)
        cv2.imwrite(path_img_mask, img_mask)

    def show_img(self, img_face, img_mask):
        cv2.imshow('1', img_face)
        cv2.imshow('2', img_mask)
        cv2.waitKey(0)

if __name__ == "__main__":
    addr = "./data/261068_2"
    data1 = data(addr)

