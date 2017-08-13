# -*-coding:utf-8 -*-
from django.shortcuts import render ,HttpResponse ,render_to_response
from User_Management.models import Menger
from models import Account_insurer
from models import Account_financing
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","www.settings")
import time
from datetime import datetime
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime
from django.db.models import Q
import django
if django.VERSION>=(1,7):
	django.setup()


# Create your views here.

#查询excel数据
def inquire(request):
    if request.method =='POST':
        search = request.POST.get('search')
        print search
        if search:
            lists = Account_insurer.objects.filter(Q(number__contains=search)|Q(ship_name__contains=search)|Q(Clerk__contains=search))
            return render(request, 'list.html', {"lists": lists})
        else:
            print '110'
    return render(request,'list.html',{})



#文件上传
def file_upload(request):
	user = request.user
	if request.method =='POST':
		file = request.FILES.get('excel_file')
		file_path = "upload/file"
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		file_name = ""
		file_path +='/'
		file_dir =file_path+file.name
		f_obj = open(file_dir,'wb+')
		for chunk in file.chunks():
			f_obj.write(chunk)
		f_obj.close()
		base_dir =os.path.abspath('.')
		list_dir = base_dir.replace('\\','/')+'/'+file_dir
		data = read_excel(list_dir)
		if not data.strip():
			os.remove(list_dir)#删除文件
			success = "上传成功"
			go_url_name = '返回'
			go_url = "/index/"
			return render_to_response('ok.html',{'success':success,'go_url_name':go_url_name,'go_url':go_url})
		else:
		 	os.remove(list_dir)#删除文件
		 	return render(request,'file_uplod.html',{'error':data})

	return render(request,'file_uplod.html',{})


def read_excel(list_dir):
    error= ''
    data = xlrd.open_workbook(list_dir)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(0)
    List = []
    x = y = z = 0
    if Menger.insurance == 1:
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:  # 查看行值是否为空
                if Account_insurer.objects.filter(number=row[0]).exists():  # 判断该行值是否在数据库中重复
                    x = x + 1  # 重复值计数
                else:
                    y = y + 1  # 非重复计数
                    row[4] = str(datetime(*xldate_as_tuple(row[4],0)))[0:10]#xrld读取xls文件时间整数值转换为达特形式
                    row[5] = str(datetime(*xldate_as_tuple(row[5],0)))[0:10]
                    List.append(Account_insurer(number=row[0], insurer=row[1],
                                                ship_name=row[2], Clerk=row[3],
                                                Insured_date=row[4],Expired_date=row[5]))
            else:
                z = z + 1  # 空行值计数
                error +="导入失败"
        Account_insurer.objects.bulk_create(List)
        print 'Successfully imported ' + str(x) + 'data, repeat' + str(y) + 'there are' + str(z) + 'lines of empty'

    if row:
        if Account_financing.objects.filter(number=row[0]).exists(): #判断该行值是否在数据库中重复
            x= x+1
        else:
            y=y+1
            row[7] = str(datetime(*xldate_as_tuple(row[7],0)))[0:10]
            List.append(Account_financing(number=row[0],Blank=row[1],
                                           ship_name=row[2],Clerk=row[3],
                                           sum=row[4],Borrower_user=row[5],
                                           Borrower_Tel=row[6],Expired_date=row[7]))
    else:
        z = z+1
        error +="导入失败"
    Account_financing.objects.bulk_create(List)
    print 'Successfully imported ' + str(x) + 'data, repeat' + str(y) + 'there are' + str(z) + 'lines of empty'
    return error











