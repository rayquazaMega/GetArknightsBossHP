import cv2
import numpy as np

def find_and_mark_red_rectangle(image):
    # 读取图像
    height, width = image.shape[:2]
    if image is None:
        return None

    # 预处理图像：提取红色通道
    red_channel = image[:, :, 2]
    green_channel = image[:, :, 1]
    blue_channel = image[:,:,0]

    # 阈值化红色通道
    _, binary_red = cv2.threshold(red_channel, 175, 255, cv2.THRESH_BINARY)
    _, binary_green = cv2.threshold(green_channel, 70, 255, cv2.THRESH_BINARY_INV)
    _, binary_blue = cv2.threshold(blue_channel, 70, 255, cv2.THRESH_BINARY_INV)
    binary_mask = binary_red * binary_green * binary_blue
    #cv2.imwrite('pure_red.png',binary_mask)

    # 查找轮廓
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 过滤轮廓，选择最佳匹配
    best_match = None
    best_match_y = 0

    # 防止匹配到中间红色出怪点，红点大概在屏幕下方中心位置
    red_point_x = 0.352*width
    red_point_y = 0.7*height
    red_point_h = 0.3*height
    red_point_w = 0.148*width
    #print(red_point_x,red_point_y,red_point_w)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # 先验，以下每一个序号对应一组判断条件
        # 1.血条应该是个长条 2.防止匹配到下方红点 3.血条高度 4.小埃受伤时也是红色的，防止匹配到小埃
        if (w/h>1.5)\
                and (x<red_point_x or x>red_point_x+red_point_w or y<red_point_y) \
                and (h>5 and h<15)\
                and (y>best_match_y)\
                and np.sum(binary_mask[y:y + h,x:x + w])>200*w*h:
            #print(np.sum(binary_mask[y:y + h,x:x + w])>200*w*h)
            #print(np.sum(binary_mask[y:y + h,x:x + w]))
            best_match_y = y
            best_match = contour

    # 在原始图像上标记红色长条矩形
    if best_match is not None:
        x, y, w, h = cv2.boundingRect(best_match)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)  # 使用绿色矩形标记

        # 保存标记后的图像
        #marked_image_file = "marked_image.png"
        #cv2.imwrite(marked_image_file, image)

        return x, y, w, h,image

    return None,None,None,None,None

def preprocess(original_image,rate=0.59):
    height, width = original_image.shape[:2]
    # 计算裁剪后图像的起始点坐标
    start_x = int(width * (1-rate)/2)
    start_y = int(height* (1-rate)/2)

    # 计算裁剪后图像的结束点坐标
    end_x = int(start_x + width * rate)
    end_y = int(start_y + height * rate)

    # 裁剪图像
    cropped_image = original_image[start_y:end_y, start_x:end_x]

    return cropped_image

def GetBossHP(image):
    '''
    :param image: (cv2::image) picture with Arknights Boss
    :return: (float) percentage HP of Arknights Boss
    '''
    stand_HP = 15.428571428571429  # 满血时埃克提尔尼尔的血量宽/长
    processed_image = preprocess(image,rate=0.59)
    x, y, w, h, textimage = find_and_mark_red_rectangle(processed_image)

    if x is not None:
        now_HP = w / 7  # h的估计可能有较大误差，此处用7来代替
        percentage_HP = now_HP / stand_HP
        return percentage_HP, textimage
    else:
        return None, None

if __name__ == "__main__":
    image_file = "F:\pycharm\pythonProject\MuMu12-20230926-230817.png"  # 替换为你的待匹配图片文件路径
    image = cv2.imread(image_file)
    GetBossHP(image)




