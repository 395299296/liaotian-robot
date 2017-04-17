try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from datetime import datetime, timedelta

from flask import request, redirect, render_template, url_for, abort, flash, g, session
from flask import current_app, make_response, send_from_directory
from flask.views import MethodView

# from flask.ext.login import login_required, current_user
from flask_login import login_required, current_user

from werkzeug.contrib.atom import AtomFeed
from mongoengine.queryset.visitor import Q


from . import models, signals, forms
from accounts.models import User
from accounts.permissions import admin_permission, editor_permission, writer_permission, reader_permission
from blog.config import RobotBlogSettings

from . import config, reply, receive, chatter
from random import randint
from imp import reload
from urllib.parse import quote, unquote
from collections import deque
from collections import defaultdict
import os

PER_PAGE = RobotBlogSettings['pagination'].get('per_page', 10)
ARCHIVE_PER_PAGE = RobotBlogSettings['pagination'].get('archive_per_page', 10)
BACKGROUND = RobotBlogSettings['background_image']

CACHE_CONTENT = defaultdict(deque)

def get_base_data():
    pages = models.Post.objects.filter(post_type='page', is_draft=False)
    blog_meta = RobotBlogSettings['blog_meta']
    data = {
        'blog_meta': blog_meta, 
        'pages': pages,
        'bg_home': BACKGROUND['home'],
        'bg_post': BACKGROUND['post'],
        'bg_about': BACKGROUND['about'],
        }
    return data

def get_keywords():
    reload(config)
    keywords = config.Config.keys()
    return '、'.join(keywords)

def get_content(content):
    reload(config)
    contentlist = deque()
    for x in config.Config:
        if x in content:
            p = __import__("main.%s"%config.Config[x][0]) # import module
            m = getattr(p,config.Config[x][0])
            reload(m)
            c = getattr(m,config.Config[x][1])
            try:
                contentlist = CACHE_CONTENT[x]
                if not contentlist:
                    contentlist = deque(c().getContent(content))
                    CACHE_CONTENT[x] = contentlist
                return contentlist.popleft()
            except Exception as e:
                print(str(e))
                raise e
            break
    else:
        contentlist = CACHE_CONTENT[content]
        if not contentlist:
            reload(chatter)
            contentlist = deque([chatter.Chatter().getContent(content)])
            CACHE_CONTENT[content] = contentlist
        return contentlist.popleft()

    return {'type':'text', 'content':content}

def index():
    return 'Hello'

def blog_index():
    
    posts = models.Post.objects.filter(post_type='post', is_draft=False).order_by('-pub_time')

    tags = posts.distinct('tags')

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1


    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')
    keywords = request.args.get('keywords')


    if keywords:
        # posts = posts.filter(raw__contains=keywords )
        posts = posts.filter(Q(raw__contains=keywords) | Q(title__contains=keywords))

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)


    #group by aggregate
    category_cursor = models.Post._get_collection().aggregate([
            { '$group' :
                { '_id' : {'category' : '$category' },
                  'name' : { '$first' : '$category' },
                  'count' : { '$sum' : 1 },
                }
            }
        ])

    widgets = models.Widget.objects(allow_post_types='post')


    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    data = get_base_data()
    data['posts'] = posts
    data['cur_category'] = cur_category
    data['category_cursor'] = category_cursor
    data['cur_tag'] = cur_tag
    data['tags'] = tags
    data['keywords'] = keywords
    data['widgets'] = widgets

    return render_template('main/index.html', **data)

def wechat_auth():
    data = request.args
    test = data.get('test','')
    if test != '':
        content = get_content(test)
        return content['content']
    
    signature = data.get('signature','')
    if signature == '':
        return 'error'

    timestamp = data.get('timestamp','')
    nonce = data.get('nonce','')
    echostr = data.get('echostr','')
    s = [timestamp,nonce,config.Token]
    s.sort()
    s = ''.join(s).encode('utf8')
    if (hashlib.sha1(s).hexdigest() != signature):
        return 'failed'
    
    return make_response(echostr)

def wechat_inter():
    xml_str = request.stream.read()
    # print('Coming Post', xml_str)
    recMsg = receive.parse_xml(xml_str)
    toUser = recMsg.FromUserName
    fromUser = recMsg.ToUserName
    replyMsg = reply.Msg(toUser, fromUser)
    if isinstance(recMsg, receive.TextMsg):
        content = recMsg.Content
        response = get_content(content)
        msgType = response['type']
        content = response['content']
        if msgType == 'text':
            replyMsg = reply.TextMsg(toUser, fromUser, content)
        elif msgType == 'news':
            replyMsg = reply.NewsMsg(toUser, fromUser, response['title'], response['content'], response['pic_url'], response['url'])
    elif isinstance(recMsg, receive.ImageMsg):
        pass
    elif isinstance(recMsg, receive.EventMsg):
        if recMsg.Event == 'subscribe':
            content = config.Welcome.format(key=get_keywords())
            replyMsg = reply.TextMsg(toUser, fromUser, content)

    return replyMsg.send()

def girl_download(filename):
    filename = unquote(filename)
    print(filename)
    if os.path.isfile(os.path.join('main/girl', filename)):
        return send_from_directory('main/girl', filename)
    abort(404)

def list_posts():

    if request.method == 'GET':
        data = request.args
        print('Coming Get', data)
        if not data:
            return blog_index()
        else:
            return wechat_auth()

    if request.method == 'POST':
        return wechat_inter()

def list_wechats():
    posts = models.Post.objects.filter(post_type='wechat', is_draft=False).order_by('-pub_time')

    tags = posts.distinct('tags')

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1


    cur_tag = request.args.get('tag')
    keywords = request.args.get('keywords')


    if keywords:
        # posts = posts.filter(raw__contains=keywords )
        posts = posts.filter(Q(raw__contains=keywords) | Q(title__contains=keywords))


    if cur_tag:
        posts = posts.filter(tags=cur_tag)


    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    widgets = models.Widget.objects(allow_post_types='wechat')

    data = get_base_data()
    data['posts'] = posts
    data['cur_tag'] = cur_tag
    data['tags'] = tags
    data['keywords'] = keywords
    data['widgets'] = widgets

    return render_template('main/wechat_list.html', **data)

def post_detail(slug, post_type='post', fix=False, is_preview=False):
    if is_preview:
        if not g.identity.can(reader_permission):
            abort(401)
        post = models.Draft.objects.get_or_404(slug=slug, post_type=post_type)
    else:
        post = models.Post.objects.get_or_404(slug=slug, post_type=post_type) if not fix else models.Post.objects.get_or_404(fix_slug=slug, post_type=post_type)

    # this block is abandoned
    if post.is_draft and current_user.is_anonymous:
        abort(404)

    data = get_base_data()
    data['post'] = post
    data['post_type'] = post_type

    if request.form:
        form = forms.CommentForm(obj=request.form)
    else:
        obj = {'author': session.get('author'), 'email': session.get('email'),'homepage': session.get('homepage'),}
        form = forms.CommentForm(**obj)
        # print session.get('email')


    if request.form.get('oct-comment') and form.validate_on_submit():
        robotblog_create_comment(form, post)
        url = '{0}#comment'.format(url_for('main.post_detail', slug=slug))
        msg = 'Succeed to comment, and it will be displayed when the administrator reviews it.'
        flash(msg, 'success')
        return redirect(url)

    data['allow_donate'] = RobotBlogSettings['donation']['allow_donate']
    data['donation_msg'] = RobotBlogSettings['donation']['donation_msg']
    data['donation_img_url'] = RobotBlogSettings['donation']['donation_img_url']

    data['display_wechat'] = RobotBlogSettings['wechat']['display_wechat']
    data['wechat_msg'] = RobotBlogSettings['wechat']['wechat_msg']
    data['wechat_image_url'] = RobotBlogSettings['wechat']['wechat_image_url']
    data['wechat_title'] = RobotBlogSettings['wechat']['wechat_title']

    data['display_copyright'] = RobotBlogSettings['copyright']['display_copyright']
    data['copyright_msg'] = RobotBlogSettings['copyright']['copyright_msg']

    data['allow_comment'] = RobotBlogSettings['blog_comment']['allow_comment']
    if data['allow_comment']:
        comment_type = RobotBlogSettings['blog_comment']['comment_type']
        comment_shortname = RobotBlogSettings['blog_comment']['comment_opt'][comment_type]
        comment_func = get_comment_func(comment_type)
        data['comment_html'] = comment_func(slug, post.title, request.base_url, comment_shortname, form=form) if comment_func else ''

    data['allow_share_article'] = RobotBlogSettings['allow_share_article']
    # if data['allow_share_article']:
    #     data['share_html'] = jiathis_share()

    # send signal
    if not is_preview:
        signals.post_visited.send(current_app._get_current_object(), post=post)

    templates = {
        'post': 'main/post.html',
        'page': 'main/post.html',
        'wechat': 'main/wechat_detail.html',
    }

    return render_template(templates[post_type], **data)

def post_preview(slug, post_type='post'):
    return post_detail(slug=slug, post_type=post_type, is_preview=True)

def post_detail_general(slug, post_type):
    is_preview = request.args.get('is_preview', 'false')
    is_preview = True if is_preview.lower()=='true' else False
    return post_detail(slug=slug, post_type=post_type, is_preview=is_preview)

def author_detail(username):
    author = User.objects.get_or_404(username=username)

    posts = models.Post.objects.filter(post_type='post', is_draft=False, author=author).order_by('-pub_time')
    cur_page = request.args.get('page', 1)

    posts = posts.paginate(page=int(cur_page), per_page=ARCHIVE_PER_PAGE)

    data = get_base_data()
    data['user'] = author
    data['posts'] = posts
    # data['category_cursor'] = category_cursor
    # data['cur_tag'] = cur_tag
    # data['tags'] = tags
    # data['keywords'] = keywords

    return render_template('main/author.html', **data)


def get_comment_func(comment_type):
    # if comment_type == 'duoshuo':
    #     return duoshuo_comment
    # else:
    #     return None
    comment_func = {
        'robotblog': robotblog_comment,
        'duoshuo': duoshuo_comment,
    }

    return comment_func.get(comment_type)

def robotblog_comment(post_id, post_title, post_url, comment_shortname, form=None, *args, **kwargs):
    template_name = 'main/comments.html'
    comments = models.Comment.objects(post_slug=post_id, status='approved').order_by('pub_time')
    # print comments[0].get_gavatar_url()
    # if not form:
    #     if session.get('author'):
    #         print 'session'
    #         return 'session'
    #         data = {'author': session['author'], 'email': session['email'],'homepage': session['homepage'],}
    #         form = forms.SessionCommentForm(obj=data)
    #     else:
    #         print 'no session'
    #         return 'no session'
    #         form = forms.CommentForm(obj=request.form)
    data = {
        'form': form,
        'comments': comments,
        'slug': post_id,
    }
    return render_template(template_name, **data)

def robotblog_create_comment(form, post):
    comment = models.Comment()
    comment.author = form.author.data.strip()
    comment.email = form.email.data.strip()
    comment.homepage = form.homepage.data.strip() or None
    comment.post_slug = post.slug
    comment.post_title = post.title
    comment.md_content = form.content.data.strip()
    comment.save()

    session['author'] = form.author.data.strip()
    session['email'] = form.email.data.strip()
    session['homepage'] = form.homepage.data.strip()


def duoshuo_comment(post_id, post_title, post_url, duoshuo_shortname, *args, **kwargs):
    '''
    Create duoshuo script by params
    '''
    template_name = 'main/misc/duoshuo.html'
    data = {
        'duoshuo_shortname': duoshuo_shortname,
        'post_id': post_id,
        'post_title': post_title,
        'post_url': post_url,
    }

    return render_template(template_name, **data)

# def jiathis_share():
#     '''
#     Create duoshuo script by params
#     '''
#     template_name = 'main/misc/jiathis_share.html'

#     return render_template(template_name)

def archive():
    posts = models.Post.objects.filter(post_type='post', is_draft=False).order_by('-pub_time')

    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')
    cur_page = request.args.get('page', 1)

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)

    posts = posts.paginate(page=int(cur_page), per_page=ARCHIVE_PER_PAGE)

    data = get_base_data()
    data['posts'] = posts

    return render_template('main/archive.html', **data)

def make_external(url):
    return urljoin(request.url_root, url)

def get_post_footer(allow_donate=False, donation_msg=None,
                    display_wechat=False, wechat_msg=None,
                    display_copyright=False, copyright_msg=None, *args, **kwargs):
    template_name = 'main/misc/post_footer.html'
    data = {}
    data['allow_donate'] = allow_donate
    data['donation_msg'] = donation_msg

    data['display_wechat'] = display_wechat
    data['wechat_msg'] = wechat_msg

    data['display_copyright'] = display_copyright
    data['copyright_msg'] = copyright_msg

    return render_template(template_name, **data)

def recent_feed():
    feed_title = RobotBlogSettings['blog_meta']['name']
    feed = AtomFeed(feed_title, feed_url=request.url, url=request.url_root)

    # data = {}
    # data['allow_donate'] = RobotBlogSettings['donation']['allow_donate']
    # data['donation_msg'] = RobotBlogSettings['donation']['donation_msg']

    # data['display_wechat'] = RobotBlogSettings['wechat']['display_wechat']
    # data['wechat_msg'] = RobotBlogSettings['wechat']['wechat_msg']

    # data['display_copyright'] = RobotBlogSettings['copyright']['display_copyright']
    # data['copyright_msg'] = RobotBlogSettings['copyright']['copyright_msg']

    # post_footer = get_post_footer(**data)

    posts = models.Post.objects.filter(post_type='post', is_draft=False)[:15]
    only_abstract_in_feed = RobotBlogSettings['only_abstract_in_feed']
    content = 'abstract' if only_abstract_in_feed else 'content_html'
    for post in posts:
        # return post.get_absolute_url()
        feed.add(post.title, 
                 # unicode(post.content_html),
                 # post.abstract,
                 getattr(post, content),
                 content_type='html',
                 author=post.author.username,
                 url=post.get_absolute_url(),
                 updated=post.update_time,
                 published=post.pub_time)
    return feed.get_response()

def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages=[]

    #########################
    # static pages
    #########################

    # ten_days_ago=(datetime.now() - timedelta(days=10)).date().isoformat()

    # for rule in current_app.url_map.iter_rules():
    #     if "GET" in rule.methods and len(rule.arguments)==0:
    #         pages.append(
    #                      [rule.rule,ten_days_ago]
    #                      )

    ## user model pages
    # users=User.query.order_by(User.modified_time).all()
    # for user in users:
    #     url=url_for('user.pub',name=user.name)
    #     modified_time=user.modified_time.date().isoformat()
    #     pages.append([url,modified_time])

    ######################
    # Post Pages
    ######################

    posts = models.Post.objects.filter(is_draft=False, post_type='post')
    for post in posts:
        pages.append((post.get_absolute_url(), post.update_time.date().isoformat(), 'weekly', '0.8'))

    ######################
    # Blog-Page Pages
    ######################

    blog_pages = models.Post.objects.filter(is_draft=False, post_type='page')
    for page in blog_pages:
        pages.append((page.get_absolute_url(), page.update_time.date().isoformat(), 'monthly', '0.7'))

    ######################
    # Wechat Pages
    ######################

    posts = models.Post.objects.filter(is_draft=False, post_type='wechat')
    for post in posts:
        pages.append((post.get_absolute_url(), post.update_time.date().isoformat(), 'weekly', '0.6'))

    sitemap_xml = render_template('main/sitemap.xml', pages=pages)
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
