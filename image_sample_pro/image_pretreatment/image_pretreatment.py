import cv2
import glob
import numpy as np

images = glob.glob('D:\\nexgen.ai\\AWS-ENV-Monitor\\image_sample_pro\\image_pretreatment\\*.jpg')
for fname in images:
        img = cv2.imread(fname)
        # print(img[2][2][2]) # RGB
        # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # cv2.imshow('gray',gray)
        # cv2.imshow('img',img)
        img_mask = img
        img_size = np.shape(img)
        for x in range(img_size[0]):
            for y in range(img_size[1]):
                if img[x][y][1] <= 100 or img[x][y][1] >= 120 and img[x][y][0] >= 130 and img[x][y][2] >= 130:
                    img_mask[x][y][0] = 0
                    img_mask[x][y][1] = 0
                    img_mask[x][y][2] = 0
        cv2.imshow('Res',img_mask)
        cv2.waitKey(2000)
        # Find the chess board co
cv2.destroyAllWindows()