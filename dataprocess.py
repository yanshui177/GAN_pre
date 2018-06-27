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
        self.savepath = 'D:\\create_data'
        filepath = self.walk_dir(addr)
        print(filepath[0])
        img, pos = self.load_img_and_pts(filepath[0])
        x1, y1, x2, y2, pos_small = self.get_margin(pos)
        face = self.get_face(img, x1, y1, x2, y2)
        mask = self.get_mask(pos_small)
        self.show_img(face, mask)
        # self.save_img(face, mask)

    def load_img_and_pts(self, addr):
        # load img
        if os.path.exists(addr + '.jpg'):
            img = cv2.imread(addr + '.jpg')
        elif os.path.exists(addr + '.png'):
            img = cv2.imread(addr + '.png')
        else:
            return None, None
        # load pts
        f2 = open(addr+'.pts', "r")
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
        if img is not None and pos is not None:
            return img, np.array(pos)
        else:
            return None, None

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
        path_img_face = 'D:/created_data/' + self.savepath.split('/')[-1] + '_face.jpg'
        path_img_mask = 'D:/created_data/' + self.savepath.split('/')[-1] + '_mask.jpg'
        cv2.imwrite(path_img_face, img_face)
        cv2.imwrite(path_img_mask, img_mask)

    def show_img(self, img_face, img_mask):
        cv2.imshow('1', img_face)
        cv2.imshow('2', img_mask)
        cv2.waitKey(0)

    def walk_dir(self, addr):
        datafiles = []
        temp = []
        for (root, dirs, files) in os.walk(addr):  # 列出windows目录下的所有文件和文件名
            for filename in files:
                temp.append(os.path.join(root, filename))
        for dir in temp:
            kind = dir.split('.')[-1]
            name = dir.split('\\')
            if kind == 'jpg' or kind == 'png':
                datafiles.append(dir.split('.')[0])
        for i in range(datafiles.count('')):
            datafiles.remove('')
        datafiles = list(set(datafiles))  # 删除重复文件
        print("共有文件：" + str(len(datafiles))+"个")
        return datafiles

    def normalize_img(self, img, target_size, method='keep_face_size'):
        if method == 'keep_face_size':
            size = img.shape
            if size[0]>target_size[0] or size[1]>target_size[1]:
                temp = cv2.resize(img, (size[0], size[1]), interpolation=cv2.INTER_CUBIC)
        elif method == 'resize':
            return cv2.resize(img, (target_size[0], target_size[1]), interpolation=cv2.INTER_CUBIC)


if __name__ == "__main__":
    addr = "E:\\DateSet\\face alignment"
    data1 = data(addr)

