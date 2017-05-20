from django import forms
from django.forms import widgets
from django.forms import fields
from dbms import models as dbms_models
from cmdb import models as cmdb_models


class InceForm(forms.Form):
    db_ip = fields.CharField(
        label='数据库地址',
        widget=widgets.Select(choices=[], attrs={'class': 'form-control',
                                                 'style': 'min-width:200px;'
                                                          ' max-width:500px'
                                                          ''})
    )
    db_port = fields.IntegerField(
        widget=widgets.TextInput(attrs={'class': 'form-control',
                                    'style': 'min-width:200px; max-width:500px'}),
        label='端口',
        max_value=65530,
        min_value=1025,
        error_messages={'invalid': '请输入有效端口号',
                        'min_value': '请输入一个大于或等于1025的端口号',
                        'max_value': '请输入一个小于或等于65530的端口号'})
    db_name = fields.CharField(
        label='库名',
        strip=True,
        widget=widgets.TextInput(attrs={'class': 'form-control',
                                    'style': 'min-width:200px; max-width:500px'})
    )
    review_user = fields.CharField(
        label='审核人',
        widget=widgets.Select(choices=[], attrs={'class': 'form-control',
                                                 'style': 'min-width:200px; max-width:500px'})
    )
    sql_text = fields.CharField(
        label='SQL 内容',
        widget=widgets.Textarea(attrs={'class': 'form-control',
                                       'style': 'min-width:200px;'
                                                'max-width:800px'})
    )

    def __init__(self, *args, **kwargs):
        super(InceForm, self).__init__(*args, **kwargs)
        self.fields['db_ip'].widget.choices = cmdb_models.HostInfo.objects.values_list('id', 'host_ip')
        self.fields['review_user'].widget.choices = cmdb_models.UserInfo.objects.values_list('id', 'user_name')



