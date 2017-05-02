from __future__ import unicode_literals
import os, sys, datetime

RobotBlogSettings = {
    'post_types': ('post', 'page'), # deprecated
    'allow_registration': os.environ.get('allow_registration', 'true').lower() == 'true',
    'allow_su_creation': os.environ.get('allow_su_creation', 'true').lower() == 'true',
    'allow_donate': os.environ.get('allow_donate', 'true').lower() == 'true',
    'auto_role': os.environ.get('auto_role', 'reader').lower(),
    'blog_meta': {
        'name': os.environ.get('name') if os.environ.get('name') else 'Robot Blog',
        'subtitle': os.environ.get('subtitle') if os.environ.get('subtitle') else '技术服务生活',
        'description': os.environ.get('description') if os.environ.get('description') else '生活蕴藏科学 技术服务生活',
        'wechat_name': os.environ.get('wechat_name') if os.environ.get('wechat_name') else 'Robot Blog Wechat Root',
        'wechat_subtitle': os.environ.get('wechat_subtitle') if os.environ.get('wechat_subtitle') else 'Robot Blog Wechat Subtitle',
        'owner': os.environ.get('owner') if os.environ.get('owner') else 'Hin',
        'keywords': os.environ.get('keywords') if os.environ.get('keywords') else 'python,flask,ML',
        'google_site_verification': os.environ.get('google_site_verification') or '12345678',
        'baidu_site_verification': os.environ.get('baidu_site_verification') or '87654321',
        'sogou_site_verification': os.environ.get('sogou_site_verification') or '87654321',
    },
    'search_engine_submit_urls':{
        'baidu': os.environ.get('baidu_submit_url')
    },
    'pagination':{
        'per_page': int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
        'archive_per_page': int(os.environ.get('admin_per_page', 20)),
    },
    'blog_comment':{
        'allow_comment': os.environ.get('allow_comment', 'true').lower() == 'true',
        'comment_type': os.environ.get('comment_type', 'robotblog').lower(), # currently, RobotBlog only supports duoshuo comment
        'comment_opt':{
            'robotblog': 'robot-blog', # shotname of robotblog
            'duoshuo': 'robot-blog', # shotname of duoshuo
            }
    },
    'donation': {
        'allow_donate': os.environ.get('allow_donate', 'true').lower() == 'true',
        'donation_msg': os.environ.get('donation_msg', 'You can donate to me if the article makes sense to you'),
        'donation_img_url': os.environ.get('donation_img_url') or '/static/img/weixin-pay.png'
    },
    'wechat': {
        'display_wechat': os.environ.get('display_wechat', 'true').lower() == 'true',
        'wechat_msg': os.environ.get('wechat_msg', 'Welcome to follow my wechat'),
        'wechat_image_url': os.environ.get('wechat_image_url') or '/static/img/liaotian-view.jpg',
        'wechat_title': os.environ.get('wechat_title', 'GevinView'),
    },
    'copyright': {
        'display_copyright': os.environ.get('allow_display_copyright', 'true').lower() == 'true',
        'copyright_msg': os.environ.get('copyright_msg', 'The article is not allowed to repost unless author authorized')
    },
    'only_abstract_in_feed': os.environ.get('only_abstract_in_feed', 'false').lower() == 'true',
    'allow_share_article': os.environ.get('allow_share_article', 'true').lower() == 'true',
    'gavatar_cdn_base': os.environ.get('gavatar_cdn_base', '//cdn.v2ex.com/gravatar/'),
    'gavatar_default_image': os.environ.get('gavatar_default_image', '/static/img/user-avatar.jpg'),
    'background_image': {
        'home': os.environ.get('bg_home') or '/static/img/robotblog-bg.jpg',
        'post': os.environ.get('bg_post') or '/static/img/robotblog-bg.jpg',
        'about': os.environ.get('bg_about') or '/static/img/robotblog_about.jpg'
    },

}

class Config(object):
    DEBUG = False
    TESTING = False

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJDL08_80jflKzcznv*c'
    MONGODB_SETTINGS = {'DB': 'RobotBlog'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')
    EXPORT_PATH = os.path.join(BASE_DIR, 'exports').replace('\\', '/')

    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=3)


    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

class PrdConfig(Config):
    # DEBUG = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
            'db': os.environ.get('DB_NAME') or 'RobotBlog',
            'host': os.environ.get('MONGO_HOST') or 'localhost',
            # 'port': 12345
        }

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGODB_SETTINGS = {'DB': 'RobotBlogTest'}
    WTF_CSRF_ENABLED = False

config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
