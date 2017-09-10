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
    error = ""
    if list_dir.find('.xlsx') == -1 and list_dir.find('.xls') == -1:
        error += "你读取的不是excel文件"
        os.remove(list_dir)
        return error
    list = []
    data = xlrd.open_workbook(list_dir)
    table = data.sheets()[0]
    num_rows = table.nrows
    if menger.insurance:
        for rows in range (num_rows):
            if rows == 0:
                continue
            try:
                insured_date = datetime(*xldate_as_tuple(table.cell_value(rows,4),0)).strftime('%Y-%m-%d').decode('utf-8')
                expired_date = datetime(*xldate_as_tuple(table.cell_value(rows,5),0)).strftime('%Y-%m-%d').decode('utf-8')
                if Account_insurer.objects.filter(number=table.cell_value(rows,0),
                                                  insurer=table.cell_value(rows,1),
                                                  ship_name=table.cell_value(rows,2),
                                                  Clerk=table.cell_value(rows,3),
                                                  Insured_date=insured_date,
                                                  Expired_date= expired_date):
                                                  pass
                else:
                     list.append(Account_insurer(number=table.cell_value(rows,0),
                     insurer=table.cell_value(rows, 1),
                     ship_name=table.cell_value(rows, 2),
                     Clerk=table.cell_value(rows, 3),
                     Insured_date=insured_date,
                     Expired_date=expired_date,
                     due_notice="1"))
            except(ValueError,IndexError):
                error +="第%d行数据格式不支持，请检查格式是否正确在上传"%(rows+1)
                break
        Account_insurer.objects.bulk_create(list)

    if menger.financing:
        for rows in range(num_rows):
            if rows == 0 :
                continue
            try:
                expired_date = datetime(*xldate_as_tuple(table.cell_value(rows,7),0)).strftime('%Y-%m-%d').decode('utf-8')
                if Account_financing.objects.filter(number=table.cell_value(rows,0),
                                                    Blank=table.cell_value(rows,1),
                                                    ship_name=table.cell_value(rows,2),
                                                    Clerk=table.cell_value(rows,3),
                                                    sum = table.cell_value(rows,4),
                                                    Borrower_user=table.cell_value(rows,5),
                                                    Borrower_Tel=table.cell_value(rows,6),
                                                    Expired_date= expired_date
                                                    ):
                    pass
                else:
                    list.append(Account_financing(number=table.cell_value(rows,0),
                                                  Blank=table.cell_value(rows, 1),
                                                  ship_name=table.cell_value(rows, 2),
                                                  Clerk=table.cell_value(rows, 3),
                                                  sum=table.cell_value(rows, 4),
                                                  Borrower_user=table.cell_value(rows, 5),
                                                  Borrower_Tel=table.cell_value(rows, 6),
                                                  Expired_date=expired_date,
                                                  due_notice='1'))

            except(ValueError,IndexError):
                error +="第%行数据格式不支持，请检查格式是否正确再上传"%(rows+1)
                break
        Account_financing.objects.bulk_create(list)
    return error


#信息列表
@login_required
def info_list(request):

    user = request.user
    menger = Menger.objects.get(user= user)
    page = request.GET.get('page')
    page_items = 10

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
			{'form':form, 'contacts': contacts, 'user':user,'menger_insurance':menger.insurance,'menger_financing':menger.financing})

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

    elif menger.financing:
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












