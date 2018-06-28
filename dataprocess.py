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
    def __init__(self, addr, savepath='D:\\create_data'):
        self.savepath = savepath
        self.normal_size = [250, 250]
        filepath = self.walk_dir(addr)
        for j in range(len(filepath)):
            img, pos = self.load_img_and_pts(filepath[j])
            x1, y1, x2, y2, pos_small = self.get_margin(pos)
            face = self.get_face(img, x1, y1, x2, y2)
            facenew, ratio, init_pos = self.normalize_img(face,
                                                          self.normal_size,
                                                          method='keep_face_size')
            mask = self.get_mask(pos_small,
                                 ratio,
                                 self.normal_size,
                                 init_pos)
            # print("init_pos:{}, mask大小：{}".format(init_pos, mask.shape))
            self.show_img([face, facenew, mask])
            self.save_img({'facenew':facenew, 'mask':mask})

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
        # pos_num = 0
        pos = []
        flag = 0
        for line3 in lines:
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

    def get_mask(self, pos_landmarks, ratio, target_size, init_pos):
        pos = np.array([[int(j) for j in i] for i in (pos_landmarks/ratio)]) + np.array(init_pos)
        img = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
        for i in range(len(pos)):
            cv2.circle(img, (pos[i][0], pos[i][1]), 2, (255, 255, 255), thickness=-1)
        return img

    def save_img(self, images):
        for i in range(len(images)):
            path_img_face = 'D:/created_data/' + self.savepath.split('/')[-1] + i + '.jpg'
            cv2.imwrite(path_img_face, images[i])

    def show_img(self, imglist):
        for i in range(len(imglist)):
            cv2.imshow(str(i), imglist[i])
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
            # source image bigger than target size
            ratio = np.max([float(img.shape[0])/float(target_size[0]),
                           float(img.shape[1])/float(target_size[1])])

            temp = cv2.resize(img,
                              (int(img.shape[1]/ratio), int(img.shape[0]/ratio), ),
                              interpolation=cv2.INTER_CUBIC
                              )
            top = int(round((target_size[0]-temp.shape[0])/2.0))
            bottom = target_size[0] - top - temp.shape[0]
            left = int(round((target_size[1]-temp.shape[1])/2.0))
            right = target_size[1] - left - temp.shape[1]
            # print("top:{}, bottom:{}, left:{}, right:{}".format(top, bottom, left, right))
            face = cv2.copyMakeBorder(temp, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            # print("原始人脸大小：{}, 目标大小：{},temp大小：{}，放缩比例：{}, face大小{}：".
            #       format(img.shape, target_size, temp.shape, ratio, face.shape))
            return face, ratio, [top, left]
        else:
            raise TypeError


if __name__ == "__main__":
    addr = "E:\\DateSet\\face alignment"
    data1 = data(addr)

