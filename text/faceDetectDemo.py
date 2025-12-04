import cv2
import requests

url = "http://localhost:8000/serviceApp/facedetect/"

# 上传图像并检测
imgPath = "face.jpg"  # 图像路径
files = {
    "image": ("face.jpg", open(imgPath, "rb"), "image/jpeg"),
}

req = requests.post(url, files=files).json()
print("获取信息：{}".format(req))

# 将检测结果显示在图像上
img = cv2.imread(imgPath)
for (x1, y1, x2, y2) in req["data"]["faces"]:
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Face detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()