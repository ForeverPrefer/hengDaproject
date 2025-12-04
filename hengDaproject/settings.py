import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ===================== 服务器环境（PythonAnywhere）=====================
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # 1. 允许访问的域名（PythonAnywhere 分配的固定域名）
    ALLOWED_HOSTS = ['ForeverPrefer.pythonanywhere.com']
    # 2. 禁用 DEBUG 模式（避免泄露敏感信息）
    DEBUG = False
    
    # 3. 静态文件配置
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 服务器收集静态文件的目标目录
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),  # 本地自定义静态文件目录
    ]
    
    # 4. 媒体文件配置
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # 5. 数据库配置（免费版仅支持 SQLite）
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# ===================== 本地开发环境=====================
else:
    ALLOWED_HOSTS = ['*', ]
    DEBUG = True
    
    # 静态文件配置（本地开发）
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    
    # 媒体文件配置
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # 数据库配置（您原有的SQLite配置，可替换为MySQL）
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ===================== 通用配置（两个环境都适用）=====================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+a06qqx(rgo%5yy7-s2nm=)qska4-o=p!t&9%f8&ef&%im%@iq"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'homeApp',
    'aboutApp',
    'contactApp',
    'newsApp',
    'productApp',
    'scienceApp',
    'serviceApp',
    'ckeditor',
    'haystack',
    'widget_tweaks',
]

CKEDITOR_UPLOAD_PATH = "uploads/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hengDaproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hengDaproject.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 搜索引擎配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'newsApp.whoosh_backend.MyWhooshEngine',  
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 搜索结果每页显示数量
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# 实时更新索引（当数据变更时自动更新）
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_DEFAULT_OPERATOR = 'AND'
HAYSTACK_DOCUMENT_FIELD = 'text'
HAYSTACK_SEARCH_RESULTS_TEMPLATE = 'search/search.html'

# 邮件配置
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '3502449120@qq.com'
EMAIL_HOST_PASSWORD = 'mbaivymnpodschgc'
EMAIL_USE_TLS = True

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table_home',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 2000
        }
    }
}