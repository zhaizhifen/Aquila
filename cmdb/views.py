from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from cmdb import forms as cmdb_forms
from django.views import View
from django.utils.decorators import method_decorator


from cmdb import models as cmdb_models
from scripts import functions
import json


def user_manager(request):
    return HttpResponse("用户管理界面尚未完成，尽情期待！！！")


# FBV
def auth(func):
    def inner(request, *args, **kwargs):
        try:
            val = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not val:
                return redirect('/cmdb/login')
            return func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('/cmdb/login')
    return inner

# CBV


@method_decorator(auth, name='dispatch')
class AuthAll(View):
    #@method_decorator(auth)
    def get(self, request):
        try:
            v = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not v:
                return redirect('/cmdb/login')
            return render(request, 'index.html', {'userinfo': v})
        except Exception as e:
            return redirect('/cmdb/login')

    def post(self, request):
        try:
            v = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not v:
                return redirect('/cmdb/login')
            return render(request, 'index.html', {'userinfo': v})
        except Exception as e:
            return redirect('/cmdb/login')


def get_user_cookie(request):
    user_cookie = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
    return user_cookie


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        pass_str = functions.py_password(pwd)
        user = cmdb_models.UserInfo.objects.filter(user_name=username, user_pass=pass_str)
        if user:
            res = redirect('/dbms/index.html')
            res.set_signed_cookie('userinfo', username, salt='adfsfsdfsd')
            return res
        else:
            return render(request, 'login.html', {'user_error': '用户名或密码错误'})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        email = request.POST.get('Email', None)
        user_info = cmdb_models.UserInfo.objects.filter(user_name=user)
        pass_str = functions.py_password(pwd)
        if user_info:
            # username and password is existe
            # 通过 ajax 返回账号已经存在的信息
            return render(request, 'register.html')
        else:
            cmdb_models.UserInfo.objects.create(
                user_name=user,
                user_pass=pass_str,
                user_emails=email,
                role_id=2,
                user_group_id=2,
                permission_id=2
            )
            return redirect('/cmdb/login')
    else:
        return render(request, 'register.html')


@auth
def hostgroup_manage(request):
    user_cookie = get_user_cookie(request)
    request_path = request.get_full_path()
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    host_edit = request.POST.get('host_edit', '')
    result = cmdb_models.HostGroup.objects.all()
    hostgroup_list = []

    if result:
        hostgroup_list = result
    return render(request, 'manage.html', {'userinfo': user_prive,
                                           'hostgroup_list': hostgroup_list,
                                           'host_edit': host_edit,
                                           'request_path': request_path})


@auth
def hostgroup_append(request):
    group_name = request.POST.get('groupname', None)
    group_desc = request.POST.get('groupdesc', None)
    group_id = request.POST.get('groupid', None)
    if group_id and group_name:
        try:
            cmdb_models.HostGroup.objects.filter(id=group_id).update(
                host_group_name=group_name,
                host_group_jd=group_desc)
            result_dict = {'flag': 1, 'msg': 'GroupName: %s update successful' % group_name}
        except Exception:
            result_dict = {'flag': 0, 'msg': 'GroupName: %s already exist' % group_name}
    elif group_name:
        result = cmdb_models.HostGroup.objects.filter(host_group_name=group_name)
        if result:
            result_dict = {'flag': 0, 'msg': 'GroupName: %s already exist' % group_name}
        else:
            cmdb_models.HostGroup.objects.create(
                host_group_name=group_name,
                host_group_jd=group_desc
            )
            result_dict = {'flag': 1, 'msg': 'GroupName: %s append successful' % group_name}
    else:
        result_dict = {'flag': 0, 'msg': 'GroupName: is None'}
    return HttpResponse(json.dumps(result_dict))


@auth
def host_manage(request):
    obj = cmdb_forms.HostAppend()
    request_path = request.get_full_path()
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    result = cmdb_models.HostInfo.objects.all()

    if request.method == 'POST':
        obj = cmdb_forms.HostAppend(request.POST)
        rel = obj.is_valid()
        id = obj.cleaned_data['host_id']
        if rel:
            if id:
                ret = host_append(request.POST)
                return HttpResponse(ret)
            else:
                ip = obj.cleaned_data['host_ip']
                exist_ip = cmdb_models.HostInfo.objects.filter(host_ip=ip).first()
                if exist_ip:
                    ret = {'flag': 0, 'data': {'ip': '主机已经存在'}}
                else:
                    try:
                        r = cmdb_models.HostInfo.objects.create(host_ip=obj.cleaned_data['host_ip'],
                                                                app_type_id=obj.cleaned_data['app_type'],
                                                                host_group_id=obj.cleaned_data['host_group'],
                                                                host_pass=obj.cleaned_data['host_pass'],
                                                                host_port=obj.cleaned_data['host_port'],
                                                                host_user=obj.cleaned_data['host_user'])
                        app_user = obj.cleaned_data['app_user']
                        app_pass = obj.cleaned_data['app_pass']
                        app_port = obj.cleaned_data['app_port']
                        if app_user or app_pass or app_port:
                            cmdb_models.HostInfoAuth.objects.create(app_user=app_user,
                                                                    app_port=app_port,
                                                                    app_pass=app_pass,
                                                                    host=r)
                        ret = {'flag': 1, 'data': None}
                    except Exception as e:
                        ret = {'flag': 0, 'data': e}
                        print('主机添加或更新有问题：', e)
            return HttpResponse(json.dumps(ret))
        else:
            ret = {'flag': 0, 'data': obj.errors}
            return HttpResponse(json.dumps(ret))
    else:
        return render(request, 'manage.html', {'userinfo': user_prive,
                                               'request_path': request_path,
                                               'host_list': result,
                                               'obj': obj})


@auth
def host_append(request):
    host_ip = request.get('host_ip', None)
    app_type_id = request.get('app_type', None)
    host_group_id = request.get('host_group', None)
    host_pass = request.get('host_pass', None)
    host_port = request.get('host_port', None)
    host_user = request.get('host_user', None)
    app_user = request.get('app_user', None)
    app_pass = request.get('app_pass', None)
    app_port = request.get('app_port', None)
    ret = cmdb_forms.HostAppend(request)
    if ret.is_valid():
        try:
            cmdb_models.HostInfo.objects.filter(id=ret.cleaned_data['host_id']).update(
                host_ip=host_ip,
                app_type_id=app_type_id,
                host_group_id=host_group_id,
                host_pass=host_pass,
                host_port=host_port,
                host_user=host_user
            )
            r = cmdb_models.HostInfo.objects.filter(id=ret.cleaned_data['host_id']).first()
            if app_user or app_pass or app_port:
                auth_ret = cmdb_models.HostInfoAuth.objects.filter(host=r).count()
                if auth_ret:
                    cmdb_models.HostInfoAuth.objects.filter(host=r).update(
                        app_port=app_port,
                        app_pass=app_pass,
                        app_user=app_user
                    )
                else:
                    cmdb_models.HostInfoAuth.objects.create(
                        host=r,
                        app_port=app_port,
                        app_pass=app_pass,
                        app_user=app_user
                    )
            result_dict = {'flag': 1, 'msg': None}
        except Exception as e:
            result_dict = {'flag': 0, 'msg': '数据更新失败:%s' % e}
    else:
        result_dict = {'flag': 0, 'msg': 'GroupName: is None'}
    return json.dumps(result_dict)


def backend(request):
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    return render(request, 'backend.html', {'userinfo': user_prive})


@auth
def group_del(request):
    hid_list = request.POST.get('host_list', None)
    gid_list = request.POST.get('group_list', None)
    group_id_list = []
    host_id_list = []
    if len(hid_list):
        for item in hid_list.split(','):
            host_id_list.append(int(item))

    if len(gid_list):
        for item in gid_list.split(','):
            group_id_list.append(int(item))
    data = {'msg': '', 'flag': 1}
    try:
        if len(host_id_list):
            r = cmdb_models.HostInfo.objects.filter(id__in=host_id_list).delete()
            data['msg'] = r
        if len(group_id_list):
            r = cmdb_models.HostGroup.objects.filter(id__in=group_id_list).delete()
            data['msg'] = r
    except Exception as e:
        data['msg'] = e
        data['flag'] = 0
    return HttpResponse(json.dumps(data))