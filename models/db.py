# -*- coding: utf-8 -*-
from test.test_support import requires
from gluon.validators import IS_IN_SET

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

# auth.settings.extra_fields['auth_user'] = (
#     [Field('user_type',label="用户类别",requires=IS_IN_SET(['省级','市州', '县区'],multiple=False))])
auth.define_tables(username=False, signature=False)
# db.auth_user.last_name.requires=None
db.auth_user.first_name.label="姓名"
# db.auth_user.last_name.label="个人姓名"
db.auth_user.last_name.readable=db.auth_user.last_name.writable=False

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True



# -------------------------------------------------------------------------
# define_parameters
minzu_list=(
"汉族","藏族","回族","蒙古族","撒拉族","土族","哈萨克族","壮族","阿昌族","白族","保安族","布朗族","布依族","朝鲜族","达斡尔族","傣族","德昂族","侗族","东乡族",
"独龙族","鄂伦春族","俄罗斯族","鄂温克族","高山族","仡佬族","哈尼族","赫哲族",
"基诺族","京族","景颇族","柯尔克孜族","拉祜族","黎族","傈僳族","珞巴族","满族","毛南族","门巴族",
"苗族","仫佬族","纳西族","怒族","普米族","羌族","畲族","水族","塔吉克族","塔塔尔族",
"土家族","佤族","维吾尔族","乌兹别克族","锡伯族","瑶族","彝族","裕固族"
              )
#

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
db.define_table('basic', 
                Field('student_ID',type='string',label='学号'),
                Field('name',type='string',label='姓名'),
                Field('gender',type='string',label='性别',requires=IS_IN_SET(['男','女'])),
                Field('grade',type='string',label='年级',requires=IS_IN_SET(['初中七年级','初中八年级','初中九年级','高中一年级','高中二年级','高中三年级'])),
                Field('age',type='string',label='年龄'),
                Field('nation', type='string',label='民族',default='汉族',requires=IS_IN_SET(minzu_list)),
                Field('company1', type='string',default='无',label='公司1',writable=False),
                Field('company2', type='string',default='无',label='公司2',writable=False),
                Field('company3', type='string',default='无',label='公司3',writable=False),
                Field('initial_date', type='date',label='录入日期',default=request.now.date,writable=False),
                )
db.define_table('account', 
                Field('company',type='string',label='公司名称'),
                Field('original_fund', type='string',label='原始资金',writable=False),
                Field('flow', type='string',label='交易名称',requires=IS_IN_SET(['工资开支','购买货物','卖货收入'])),
                Field('category', type='string',label='交易类型',requires=IS_IN_SET(['支出','收入'])),
                Field('amount', type='string',label='数额'),
                Field('trade_time', type='time',label='交易日期',default=request.now,writable=False),
                Field('balance', type='string',label='余额',writable=False),
                )
db.define_table('company', 
                Field('name',type='string',label='公司名称'),
                Field('category', type='string',label='注册类型',writable=False),
                Field('legal_person', type='string',label='法人'),
                Field('status', type='string',label='审核状态',default='待审核',requires=IS_IN_SET(['已通过','未通过','待审核']),writable=False),
                )
db.define_table('goods', 
                Field('company',type='string',label='所属公司'),
                Field('name',type='string',label='货物名称'),
                Field('price', type='string',label='价格'),
                Field('amount', type='string',label='数量'),
                )
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
