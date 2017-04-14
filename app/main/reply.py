import time
import logging

class Msg(object):
    def __init__(self, toUserName, fromUserName):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())

    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        Msg.__init__(self, toUserName, fromUserName)
        self._Msg__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        logging.info("Send to", self._Msg__dict['ToUserName'], self._Msg__dict['Content'])
        return XmlForm.format(**self._Msg__dict)
    
class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        Msg.__init__(self, toUserName, fromUserName)
        self._Msg__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self._Msg__dict)

class NewsMsg(Msg):
    def __init__(self, toUserName, fromUserName, title, desc, picUrl, url):
        Msg.__init__(self, toUserName, fromUserName)
        self._Msg__dict['Title'] = title
        self._Msg__dict['Description'] = desc
        self._Msg__dict['PicUrl'] = picUrl
        self._Msg__dict['Url'] = url

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
            <item>
                <Title><![CDATA[{Title}]]></Title> 
                <Description><![CDATA[{Description}]]></Description>
                <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
                <Url><![CDATA[{Url}]]></Url>
            </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self._Msg__dict)