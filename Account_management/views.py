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
from forms import insurerForm,financingForm ,SearchForm
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.contrib.auth.decorators import login_required


# Create your views here.

#查询excel数据
@login_required
def inquire(request):
    user = request.user
    menger = Menger.objects.get(user=user)
    if request.method =='POST':
        search = request.POST.get('search')
        if menger.insurance ==1:
            obj = Account_insurer
        elif menger.financing ==1:
            obj = Account_financing
        if search:
            lists = obj.objects.filter(Q(number__contains=search)|Q(ship_name__contains=search)|Q(Clerk__contains=search))
            return render(request, 'list.html', {"lists": lists,'menger_insurance':menger.insurance,'menger_financing':menger.financing})
    return render(request,'list.html',{})

#文件上传
@login_required
def file_upload(request):
    user = request.user
    menger = Menger.objects.get(user=user)
    if request.method == 'POST':
        file = request.FILES.get('excel_file')
        file_path = "upload/file"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = ""
        file_path += '/'
        file_dir = file_path + file.name
        f_obj = open(file_dir, 'wb+')
        for chunk in file.chunks():
            f_obj.write(chunk)
        f_obj.close()
        base_dir = os.path.abspath('.')
        list_dir = base_dir.replace('\\', '/') + '/' + file_dir
        data = read_excel(list_dir,menger)
        if not data.strip():
            os.remove(list_dir)  # 删除文件
            success = "上传成功"
            go_url_name = '返回'
            go_url = "/index/"
            return render_to_response('ok.html', {'success': success, 'go_url_name': go_url_name, 'go_url': go_url})
        else:
            os.remove(list_dir)  # 删除文件
            return render(request, 'file_uplod.html', {'error': data})

    return render(request, 'file_uplod.html', {})


#读取文件内容
def read_excel(list_dir,menger):
    error= ''
    data = xlrd.open_workbook(list_dir)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(0)
    List = []
    x = y = z = 0
    for i in range(1, nrows):
        row = table.row_values(i)
        for j in range(0, ncols):
            if type(row[j]) == float:
                row[j] = int(row[j])
        if menger.insurance == 1:
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

        if menger.insurance == 1:
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

#信息列表
@login_required
def info_list(request):

    user = request.user
    menger = Menger.objects.get(user= user)
    page = request.GET.get('page')
    page_items = 30

    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.data['keyword']
            page = form.data['current_page']
            if menger.insurance == 1:
                obj = Account_insurer
            elif menger.financing ==1:
                obj = Account_financing
            lists = obj.objects.filter(Q(shipname__contains=keyword)|Q(number__number__contains=keyword))

            contacts_tmp = list(set(lists))
            paginator = Paginator(contacts_tmp, page_items) # Show 25 contacts per page

            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)

            return render(request, 'info_list.html',\
			{'form':form, 'contacts': contacts, 'user':user})

    else:

        lists = Account_insurer.objects.all()
        paginator = Paginator(lists, page_items) # Show 25 contacts per page
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'info_list.html',\
		{'form':form, 'contacts': contacts, 'user':user})


#信息录入
@login_required
def Entry_information(request):
    user =request.user
    menger = Menger.objects.get(user=user)
    if menger.insurance:
        if request.method == 'POST':
            form = insurerForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                insurer = form.cleaned_data['insurer']
                ship_name = form.cleaned_data['ship_name']
                Clerk = form.cleaned_data['clerk']
                Insured_date = form.cleaned_data['insured_date']
                Expired_date = form.cleaned_data['expired_date']
                if Account_insurer.objects.filter(number=number,ship_name=ship_name):
                    error = "数据已存在。请不要重复填写"
                    return render(request,'new.html',{'form':form,'error':error,'menger_insuere':menger.insurance})
                else:
                    Account_insurer.objects.create(
                        number= number,
                        ship_name=ship_name,
                        insurer = insurer,
                        Clerk=Clerk,
                        Insured_date =Insured_date,
                        Expired_date = Expired_date
                        )
                    success = "录入成功"
                    go_url_name = '返回'
                    go_url= '/list/'
                    return render_to_response('OK.html',{'success':success,'go_url_name':go_url_name,'go_url':go_url})

            else:
                error = form.errors
                return render(request, 'new.html',{'form': form,  'error': error,'menger_insuere':menger.insurance})
        else:
            form = insurerForm()
        return render(request, 'new.html', {'form': form, 'menger_insuere':menger.insurance})

    elif menger.financing :
        if request.method == 'POST':
            form = financingForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                Blank = form.cleaned_data['blank']
                ship_name = form.cleaned_data['ship_name']
                Clerk = form.cleaned_data['clerk']
                sum = form.cleaned_data['sum']
                Borrower_user = form.cleaned_data['borrower_user']
                Borrower_tel = form.cleaned_data['borrower_tel']
                Expired_date  = form.cleaned_data['expired_date']
                if Account_financing.objects.filter(number=number,
                                                          ship_name=ship_name,
                                                        ):
                    error = '你填写的数据已存在，请不要重复填写！'
                    return render(request, 'new.html',
                                  {'form': form, 'error': error, 'menger_financing': menger.financing})
                else:
                    Account_financing.objects.create(number=number,
                                                     ship_name=ship_name,
                                                     Blank=Blank,
                                                     Clerk =Clerk,
                                                     sum = sum,
                                                     Borrower_user=Borrower_user,
                                                     Borrower_Tel =Borrower_tel,
                                                     Expired_date =Expired_date

                                                            )
                    success = "录入成功"
                    go_url_name = '返回'
                    go_url = "/list/"
                    return render_to_response('OK.html',
                                              {'success': success, 'go_url_name': go_url_name, 'go_url': go_url})
            else:
                error = form.errors
                return render(request, 'new.html',
                              {'form': form, 'error': error, 'menger_financing': menger.financing})
        else:
            form = financingForm()
        return render(request, 'new.html', {'form': form, 'menger_financing': menger.financing})

#表单修改
@login_required
def Modify_content(request,id=''):
    user = request.user
    menger  = Menger.objects.get(user=user)
    if menger.insurance:
        list = Account_insurer.objects.get(id =id)
        if request.method =='POST':
            form = insurerForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                numbers = Account_insurer.objects.filter(number__contains=number).exclude(number=list.number)
                if numbers:
                    error = '编号存在！'
                    return render(request,'NO.html',{'error':error})
                else:
                    insurer = form.cleaned_data['insurer']
                    ship_name =form.cleaned_data['ship_name']
                    clerk = form.cleaned_data['clerk']
                    insurer_date = form.cleaned_data['insurer_date']
                    expired_date = form.cleaned_data['expired_date']

                    avalue = Account_insurer.objects.get(id=id)
                    avalue.insurer = insurer
                    avalue.ship_name =ship_name
                    avalue.number = number
                    avalue.Clerk =clerk
                    avalue.Insured_date =insurer_date
                    avalue.Expired_date = expired_date
                    avalue.save()
                    success = '修改成功'
                    go_url_name = '返回列表'
                    go_url = '/index/'
                    return render_to_response('OK.html', {'success':success, 'go_url_name':go_url_name, 'go_url':go_url})
            else:
                error = '修改失败'
                return render_to_response('NO.html', {'error':error})
        else:
            form = insurerForm(initial={
                'number':list.number,
                'insurer':list.insurer,
                'ship_name':list.ship_name,
                'clerk':list.Clerk,
                'insured_date':list.Insured_date,
                'expired_date':list.Expired_date

            })
        return render(request,'new_data.html',{'form':form,'list':list})

    elif menger.financing:
        list = Account_financing.objects.get(id =id)
        if request.method =='POST':
            form = financingForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                numbers = Account_financing.objects.filter(number__contains=number).exclude(number=list.number)
                if numbers:
                    error = '编号存在！'
                    return render(request,'NO.html',{'error':error})
                else:
                    blank = form.cleaned_data['blank']
                    ship_name =  form.cleaned_data['ship_name']
                    clerk = form.cleaned_data['clerk']
                    sum =  form.cleaned_data['sum']
                    borrower_user =  form.cleaned_data['borrower_user']
                    borrower_tel =  form.cleaned_data['borrower_tel']
                    expired_date =  form.cleaned_data['expired_date']

                    avalue = Account_financing.objects.get(id=id)
                    avalue.number =number,
                    avalue.Blank = blank,
                    avalue.Clerk =clerk,
                    avalue.sum = sum
                    avalue.ship_name =ship_name,
                    avalue.Borrower_Tel = borrower_tel
                    avalue.Borrower_user = borrower_user
                    avalue.Expired_date = expired_date
                    avalue.save()
                    success = '修改成功'
                    go_url_name = '返回列表'
                    go_url = '/index/'
                    return render_to_response('OK.html',{'success': success, 'go_url_name': go_url_name, 'go_url': go_url})
            else:
                error = '修改失败'
                return render_to_response('NO.html', {'error': error})
        else:
            form = financingForm(initial={
                'number':list.number,
                'blank':list.Blank,
                'ship_name':list.ship_name,
                'clerk':list.Clerk,
                'sum':list.sum,
                'borrower_user':list.Borrower_user,
                'borrower_tel':list.Borrower_Tel,
                'expired_date':list.Expired_date
            })
        return render(request, 'new_data.html', {'form': form, 'list': list})

@login_required
def ship_delete(request, id=''):
    """
    删除船舶
    """
    try:
        avalue = Account_insurer.objects.get(id=id)
        if avalue:
            avalue.delete()
            return HttpResponse("船舶删除成功！")
        else:
            return HttpResponse("船舶删除失败！")
    except LookupError, error:
        print error
        return HttpResponse("船舶删除失败！")












