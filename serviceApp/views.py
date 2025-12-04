from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Doc
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404, StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Doc 
import os

# 1. 资料列表
def download(request): 
    doc_list = Doc.objects.all().order_by('-publishDate')
    paginator = Paginator(doc_list, 5)
    page = request.GET.get('page', 1)
    
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)
    
    # 构建与模板匹配的分页数据
    page_data = {
        'page': docs.number,
        'total_pages': paginator.num_pages,
        'first': docs.number > 3,
        'last': docs.number < paginator.num_pages - 2,
    }
    
    # 计算分页范围
    if paginator.num_pages <= 7:
        page_data['left'] = list(range(1, docs.number))
        page_data['right'] = list(range(docs.number + 1, paginator.num_pages + 1))
    else:
        if docs.number <= 4:
            page_data['left'] = list(range(1, docs.number))
            page_data['right'] = list(range(docs.number + 1, 6))
            page_data['right_has_more'] = True
            page_data['last'] = True
        elif docs.number >= paginator.num_pages - 3:
            page_data['left'] = list(range(paginator.num_pages - 4, docs.number))
            page_data['left_has_more'] = True
            page_data['first'] = True
            page_data['right'] = list(range(docs.number + 1, paginator.num_pages + 1))
        else:
            page_data['left'] = list(range(docs.number - 2, docs.number))
            page_data['right'] = list(range(docs.number + 1, docs.number + 3))
            page_data['left_has_more'] = True
            page_data['right_has_more'] = True
            page_data['first'] = True
            page_data['last'] = True
    
    return render(request, 'docList.html', {
        'activmenu': 'service',  
        'smenu': 'download',    
        'newName': '资料下载',    
        'docs': docs,            
        'pageData': page_data,
    })


# 2. 文件下载函数
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, Http404
from django.conf import settings
import os

def getDoc(request, id):
    doc = get_object_or_404(Doc, id=id)
    
    # 正确的文件路径获取方式
    file_path = os.path.join(settings.MEDIA_ROOT, doc.file.name)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise Http404("文件不存在")
    
    # 分批读取文件（避免大文件内存溢出）
    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    # 获取文件名
    filename = os.path.basename(file_path)
    
    # 构建下载响应
    response = StreamingHttpResponse(
        file_iterator(file_path),
        content_type='application/octet-stream'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Content-Length'] = os.path.getsize(file_path)
    
    return response

def platform(request):
    return render(request, 'platform.html', {
        'activmenu': 'service', 
        'smenu': 'platform',   
    })

import cv2
import numpy as np
import os
import tempfile
import shutil
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                          "serviceApp", "haarcascade_frontalface_default.xml")

temp_dir = tempfile.gettempdir()
target_path = os.path.join(temp_dir, "haarcascade_frontalface_default.xml")

face_detector = None
try:
    if os.path.exists(source_path):
        shutil.copy2(source_path, target_path)
        face_detector = cv2.CascadeClassifier(target_path)
        if face_detector.empty():
            face_detector = None
except Exception as e:
    print(f"分类器加载失败: {e}")

@csrf_exempt
def facedetect(request):
    if request.method == "POST":
        if "image" not in request.FILES:
            return JsonResponse({"code": -1, "data": {}, "msg": "未找到图像文件"})

        if face_detector is None or face_detector.empty():
            return JsonResponse({"code": -1, "data": {}, "msg": "人脸检测器未正确加载"})

        try:
            img_file = request.FILES["image"]
            img = read_image(img_file)
            if img is None:
                return JsonResponse({"code": -1, "data": {}, "msg": "图像读取失败"})

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            faces_list = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in faces]

            return JsonResponse({
                "code": 0,
                "data": {"faces": faces_list},
                "msg": f"检测到 {len(faces_list)} 个人脸"
            })
            
        except Exception as e:
            return JsonResponse({"code": -1, "data": {}, "msg": f"处理错误: {str(e)}"})
    
    return JsonResponse({"code": -1, "data": {}, "msg": "请使用POST方法"})

def read_image(stream):
    try:
        img_data = stream.read()
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None
    

import base64
@csrf_exempt
def facedetectDemo(request):
    result = {}

    if request.method == "POST":
        if request.FILES.get('image') is not None: #  
            img = read_image(stream = request.FILES["image"])  
        else:  
            result["faceNum"] = -1  
            return JsonResponse(result)  

        if img.shape[2] == 3:  
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 彩色图像转灰度图像  
        else:  
            imgGray = img  

        # 进行人脸检测  
        values = face_detector.detectMultiScale(imgGray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30), flags = cv2.CASCADE_SCALE_IMAGE)  

        # 将检测得到的人脸检测关键点坐标封装  
        values = [(int(a), int(b), int(a + c), int(b + d)) for (a, b, c, d) in values]  

        # 将检测框显示在原图上  
        for (w, x, y, z) in values:  
            cv2.rectangle(img, (w, x), (y, z), (0, 255, 0), 2)  

        retval, buffer_img = cv2.imencode('.jpg', img) # 在内存中编码为 jpg 格式  
        img64 = base64.b64encode(buffer_img) # base64 编码用于网络传输  
        img64 = str(img64, encoding = 'utf-8') # bytes 转换为 str 类型  
        result["img64"] = img64 # json 封装  
        return JsonResponse(result)