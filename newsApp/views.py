from django.shortcuts import render, get_object_or_404
from .models import MyNew
from django.core.paginator import Paginator
from pyquery import PyQuery as pq

def news(request, newName):
    submenu = newName
    # 解析新闻类型
    if newName == 'company':
        newName = '企业要闻'
        newType = '企业要闻'
    elif newName == 'industry':
        newName = '行业新闻'
        newType = '行业新闻'
    else:
        newName = '通知公告'
        newType = '通知公告'
    
    # 获取并处理新闻列表
    newList = MyNew.objects.filter(newType=newType).order_by('-publishDate')
    for mynew in newList:
        html = mynew.description
        doc = pq(html)
        mynew.mytext = doc.text()[:110]  # 截取摘要
    
    # 分页逻辑
    p = Paginator(newList, 5)
    pageData = ''
    if p.num_pages > 1:
        page = int(request.GET.get('page', 1))
        newList = p.page(page)
        # 分页数据处理（保持原逻辑）
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        
        if page == 1:
            right = page_range[page:page + 2]
            if right and right[-1] < total_pages - 1:
                right_has_more = True
            if right and right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left and left[0] > 2:
                left_has_more = True
            if left and left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left and left[0] > 2:
                left_has_more = True
            if left and left[0] > 1:
                first = True
            if right and right[-1] < total_pages - 1:
                right_has_more = True
            if right and right[-1] < total_pages:
                last = True
        
        pageData = {
            'left': left, 'right': right, 'left_has_more': left_has_more,
            'right_has_more': right_has_more, 'first': first, 'last': last,
            'total_pages': total_pages, 'page': page
        }
    
    return render(request, 'news.html', {
        'activmenu': 'news',
        'smenu': submenu,
        'newName': newName,
        'newList': newList,
        'pageData': pageData,
    })

def newDetail(request, id):
    mynew = get_object_or_404(MyNew, id=id)
    mynew.views += 1  # 增加阅读量
    mynew.save()
    return render(request, 'newDetail.html', {
        'activmenu': 'news',
        'mynew': mynew,
    })

