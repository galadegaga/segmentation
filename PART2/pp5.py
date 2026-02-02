import cv2
import numpy as np
import os
import csv


image_path = r"F:\pywork119\pythonProject\Ziqiang-main\DU1\pred\6.png"      #要求路径没有中文
save_dir = r"F:\pywork119\pythonProject\contour"                            #要求路径没有中文
scale_factor = 2
group_size = 20
contour_thickness = 1
contour_color = (0, 255, 0)
text_color = (0, 0, 255)
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 0.5 * scale_factor
text_thickness = 1
min_area = 25

csv_path = r"F:\pywork119\pythonProject\0122图像分割\coordinates.csv"
output_all = False


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    print(f"创建目录：{path}")


def resize_img(img, factor):
    h, w = img.shape[:2]
    new_h = int(h * factor)
    new_w = int(w * factor)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


def get_outside_contours(binary_img):
    contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    outside_contours = []

    for i, cnt in enumerate(contours):
        if hierarchy[0][i][3] == -1 and cv2.contourArea(cnt) > min_area:
            outside_contours.append(cnt)

    return outside_contours


img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"图片不存在：{image_path}")

original_h, original_w = img.shape[:2]
print(f"原始尺寸: {original_w}x{original_h}")

scaled_img = resize_img(img, scale_factor)
gray_img = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2GRAY)
_, binary_img = cv2.threshold(gray_img, 120, 255, cv2.THRESH_BINARY)

white_contours = get_outside_contours(binary_img)
inverted = cv2.bitwise_not(binary_img)
black_contours = get_outside_contours(inverted)

all_contours = white_contours + black_contours
total = len(all_contours)
print(f"找到独立区域：{total}")

h, w = scaled_img.shape[:2]
mask = np.zeros((h, w), dtype=np.uint32)

for idx, cnt in enumerate(all_contours, start=1):
    temp = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(temp, [cnt], -1, 255, thickness=cv2.FILLED)
    mask[temp > 0] = idx

print(f"掩码尺寸: {w}x{h}")

try:
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['# 像素坐标表'])
        writer.writerow([f'# 图片: {image_path}'])
        writer.writerow([f'# 原尺寸: {original_w}x{original_h}'])
        writer.writerow([f'# 缩放后: {w}x{h}'])
        writer.writerow([f'# 区域数: {total}'])
        writer.writerow(['#=' * 30])
        writer.writerow(['X', 'Y', '区域ID', '属性'])

        attrs = []
        for i in range(1, total + 1):
            attr = input(f"区域 {i} 属性: ")
            attrs.append(attr)

        count = 0

        if output_all:
            for y in range(h):
                for x in range(w):
                    rid = int(mask[y, x])
                    attr = attrs[rid - 1] if rid > 0 else '背景'
                    writer.writerow([x, y, rid, attr])
                    count += 1
        else:
            for y in range(h):
                for x in range(w):
                    rid = int(mask[y, x])
                    if rid > 0:
                        attr = attrs[rid - 1]
                        writer.writerow([x, y, rid, attr])
                        count += 1

    print(f"CSV保存: {csv_path}")
    print(f"输出点数: {count}")

except Exception as e:
    print(f"CSV保存失败: {e}")

make_folder(save_dir)
groups = (total + group_size - 1) // group_size

for g in range(groups):
    start = g * group_size
    end = min((g + 1) * group_size, total)
    current = all_contours[start:end]

    group_img = np.zeros_like(scaled_img)
    area_mask = np.zeros((scaled_img.shape[0], scaled_img.shape[1]), np.uint8)

    for cnt in current:
        cv2.drawContours(area_mask, [cnt], -1, 255, thickness=cv2.FILLED)

    group_img[area_mask > 0] = scaled_img[area_mask > 0]

    for local, cnt in enumerate(current):
        cv2.drawContours(group_img, [cnt], -1, contour_color, contour_thickness)
        num = start + local + 1
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            text_size = cv2.getTextSize(str(num), text_font, text_scale, text_thickness)[0]
            tx = max(0, cx - text_size[0] // 2)
            ty = min(scaled_img.shape[0] - 1, cy + text_size[1] // 2)
            cv2.putText(group_img, str(num), (tx, ty),
                        text_font, text_scale, text_color, text_thickness)

    save_name = f"group_{g + 1}.jpg"
    save_path = os.path.join(save_dir, save_name)
    try:
        cv2.imwrite(save_path, group_img)
        print(f"保存第{g + 1}组图片：{save_path}")
    except Exception as e:
        print(f"保存失败：{e}")

if groups > 0:
    cv2.imshow(f"第{groups}组结果", group_img)

    color_mask = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(1, total + 1):
        color = np.random.randint(50, 255, 3).tolist()
        color_mask[mask == i] = color

    color_mask_path = os.path.join(save_dir, "colored_regions.jpg")
    try:
        cv2.imwrite(color_mask_path, color_mask)
        print(f"保存colored_regions：{color_mask_path}")
    except Exception as e:
        print(f"colored_regions保存失败：{e}")

    cv2.imshow("colored_regions", color_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()