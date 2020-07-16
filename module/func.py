from django.conf import settings
import requests
from linebot import LineBotApi

import http.client, json
from qnaapi.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
from linebot.models import TextSendMessage, TemplateSendMessage,\
    ButtonsTemplate, URITemplateAction, MessageTemplateAction, CarouselTemplate, CarouselColumn

host = 'welab.azurewebsites.net'  #主機
endpoint_key = "1a987b52-37c3-4698-ad8d-1db1d210ef47"  #授權碼
kb = "bb50c33f-5cbe-4904-8559-13bede325c7b"  #GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

#from firebase import firebase
#url = 'https://mybot-65922.firebaseio.com/'
#fb = firebase.FirebaseApplication(url, None)
import datetime

import pymongo
from pymongo import MongoClient
import urllib.parse
Authdb='bot'







def senduse(event):  #使用說明
    try:
        text1 ='歡迎繼續輸入關於LINE機器人的相關問題!'
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQnA2(event):  #使用說明
    try:
        text1 ='謝謝您的詢問,我們的資料庫會進行更新!'
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQnA(event, mtext):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！我們會進行更新!\n請再輸入其他問題。'
        #將沒有解答的問題寫入資料庫
#        line_bot_api.reply_message(event.reply_token,text1)
#        userid = event.source.user_id
#        unit = users.objects.create(uid=userid, question=mtext)
#        unit.save()

#        t=datetime.date.today()
#        qq=[{'id':userid,'message':mtext,'date':t}]
#        for q in qq:
#            fb.post('/qna', q)

#        profile = line_bot_api.get_profile(event.source.user_id)
#        uid = profile.user_id #使用者ID
#        usespeak=str(event.message.text)
#        mongodb.write_user_stock_fountion(userid,t,mtext)

        client = MongoClient('mongodb://roly:dayi3774@cluster0-shard-00-00.0mtts.mongodb.net:27017,cluster0-shard-00-01.0mtts.mongodb.net:27017,cluster0-shard-00-02.0mtts.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-da52w8-shard-0&authSource=admin&retryWrites=true&w=majority')

        db = client[Authdb]

        collect = db['mydb']
        collect.insert({"id": event.source.user_id,
                        "date": datetime.datetime.utcnow(),
                        "buy": 'no',
                        "text": mtext
                        })
    else:
        result2 = result1[2:]  #移除「A：」
        text1 = result2  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token,message)



#def firebase(event, mtext, user_id):
#    t=datetime.date.today()
#    qq=[{'id':user_id,'message':mtext,'date':t}]
#    for q in qq:
#        fb.post('/qna', q)    

def manageForm(event, mtext, user_id):  #處理LIFF傳回的FORM資料
    try:
        a5 = mtext[3:]
        flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串
        a1 = flist[0]  #取得輸入資料
        a2 = flist[1]
        a3 = flist[2]


        text1 = "您的機器人已預訂成功，資料如下："
        text1 += "\n您的姓名：" + a1
        text1 += "\n您的email：" + a2
        text1 += "\n機器人類型：" + a3

        unit = users.objects.create(uid=user_id, buy=a5)  #寫入資料庫
        unit.save()
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='24HBOT',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/0a65QKx.jpg',  #顯示的圖片
                title='中小企業24H客服機器人',  #主標題
                text='微軟人工智慧機器學習系統\n24H全自動客服\n完全取代傳統客服',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='收費標準及額外贈送功能',
                        text='*中小企業24H客服機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:9000元(限時促銷價) \n訂閱收費:每月388元'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='更多了解功能',
                        uri='https://www.youtube.com/watch?v=bGAY-IY90H4'
                    ),
                    URITemplateAction(
                        label='免費試用或訂購',
                        uri='https://unitbesto.wixsite.com/mysite'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))     



def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='linebot',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/UAyXMUj.jpg',
                        title='美髮/美甲/美容店預約機器人-----1.預約(24小時接單) 2.選擇設計師',
                        text='24小時接單預約/取消預約/選擇剪,燙,染設計師/店面介紹/查詢預約日天氣/客戶名單管理/以星座遊戲吸引來客',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*美髮美甲美容預約機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                            ),
                            URITemplateAction(
                                label='更多了解美髮美容預約功能',
                                uri='https://www.youtube.com/watch?v=PT3Rgv5ZiJA'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Ywp1PKq.jpg?1',
                        title='旅館 / 民宿 訂房專用機器人',
                        text='1.訂房(24小時)2.旅館房型介紹3.外國客翻譯4.查詢天氣交通5.房客名單管理6.以廣告訊息吸引來客',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*旅館民宿訂房機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                            ),
                            URITemplateAction(
                                label='更多了解旅館民宿訂房功能',
                                uri='https://www.youtube.com/watch?v=FU98sfU9an8'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/gPOrzYH.jpg',
                        title='早餐店 / 攤商 外帶專用機器人',
                        text='建置中!',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*早餐店攤商外帶機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                            ),
                            URITemplateAction(
                                label='更多了解功能',
                                uri='https://www.youtube.com/watch?v=FU98sfU9an8'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    )
                ]
            )
        )



        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendCarousel2(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='linebot',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/d1NI8MA.jpg',
                        title='股匯價即時報價/指定價到價主動通知機器人/AI選股機器人',
                        text='股匯價即時報價\n指定價到價主動通知\nAI選股/基本面/技術面/籌碼面分析',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*股匯機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:9000元(限時促銷價) \n訂閱收費:每月388元'
                            ),
                            URITemplateAction(
                                label='更多了解AI選股功能',
                                uri='https://www.youtube.com/watch?v=bGAY-IY90H4'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    ),
    
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/AVBEUCy.jpg',
                        title='建商仲介買房族查詢房地產資訊機器人',
                        text='建置中!',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*建商仲介買房族查詢機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:9000元(限時促銷價) \n訂閱收費:每月388元'
                            ),
                            URITemplateAction(
                                label='更多了解功能',
                                uri='https://www.youtube.com/watch?v=bGAY-IY90H4'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendCarousel3(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='linebot',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/9BEvhR0.png',
                        title='Youtuber圈粉專用機器人',
                        text='1.將youtube粉絲吸引至你的LINE2.建立你的LINE粉絲名單3.經營LINE粉絲4.在LINE建立你的通訊官網',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*Youtuber圈粉機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                            ),
                            URITemplateAction(
                                label='Youtuber圈粉功能',
                                uri='https://www.youtube.com/watch?v=FU98sfU9an8'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/SFm5pZW.jpg',
                        title='團購訂單推播機器人',
                        text='建置中!',
                        actions=[
                            MessageTemplateAction(
                                label='收費標準及額外贈送功能',
                                text='*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                            ),
                            URITemplateAction(
                                label='更多了解功能',
                                uri='https://www.youtube.com/watch?v=PT3Rgv5ZiJA'
                            ),
                            URITemplateAction(
                                label='免費試用或訂購',
                                uri='https://unitbesto.wixsite.com/mysite'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendCarousel4(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='linebot',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/QFyEi4h.jpg',
                        title='LINE Chatbot將會是下一個世代的App',
                        text='與App相比之下，Chatbot不占手機儲存空間，以投資成本來說，也很適合中小企業主投入。',
                        actions=[
                            URITemplateAction(
                                label='科技防疫機器人媒體報導',
                                uri='https://liff.line.me/1654140247-0LZB6qkj'
                            ),
                            URITemplateAction(
                                label='聊天機器人成功案例',
                                uri='https://liff.line.me/1654140247-QO7r5X2e'
                            ),
                            URITemplateAction(
                                label='聊天機器人媒體報導',
                                uri='https://liff.line.me/1654140247-9BQeydjX'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/AdQIFR7.png',
                        title='聊天機器人再進化！不只搞定客服，更在互動時勾住消費者的心!',
                        text='LINE在台灣擁有2100萬用戶,對台灣的企業主而言，有90%的使用者不需要額外下載新的App，就可以與其溝通互動。',
                        actions=[
                            URITemplateAction(
                                label='免費體驗多國語言翻譯機器人',
                                uri='https://lin.ee/4FAdjAYoC'
                            ),
                            URITemplateAction(
                                label='免費使用統一發票兌獎機器人',
                                uri='https://lin.ee/3CKJGe75V'
                            ),
                            URITemplateAction(
                                label='公司網站',
                                uri='https://www.chatbizz.biz'
                            )

                        ]
                    ),    
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/QFyEi4h.jpg',
                        title='各行各業的聊天機器人陸續開發中',
                        text='開發中:\n團購訂單推播機器人\n建商仲介買房族查詢房地產資訊機器人\n早餐店/攤商 外帶專用機器人',
                        actions=[
                            MessageTemplateAction(
                                label='公司介紹',
                                text='*瑋士科技由跨領域的團隊組成，一同打造不同功能的聊天機器人，致力將機器人建模模組化，協助企業積極掌握顧客足跡的數據，幫助企業快速與陌生人展開深度談話並建立信任關係。聊天機器人與微軟的人工智慧引擎結合透過語意分析及深度學習技術，對話式廣告模式協助廣告主與顧客互動。我們的團隊成員多元活潑、激勵創新、樂於挑戰為公司文化。'
                            ),
                            MessageTemplateAction(
                                label='本公司機器人功能說明',
                                text='*我們可以在您的手機通訊軟體 LINE Messenger上面新增加附有:24H自動接收預約, 訂房, 訂位, 外帶的功能。24H自動回覆客服, 客戶訂單紀錄, 訊息廣告推播, 紀錄客戶資料足跡的功能。24H自動查詢股價, 天氣, 交通.........等功能的小網站。24H讓機器人代替您在 LINE Messenger上面做生意, 回覆客戶問題, 完全不漏接任何一筆訂單。最重要的是:您甚麼都不用做, 就可以直接在您的手機上使用, 我們會把所有的事都做好做滿。'
                            ),
                            MessageTemplateAction(
                                label='留言/e-mail/TEL',
                                text='*留言:請輸入您的留言!\n*Email:unitbesto@gmail.com\n*TEL:0936587188'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendCarousel5(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='24HBOT',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/CQZixLR.jpg',  #顯示的圖片
                title='各國朋友LINE群組翻譯機器人',  #主標題
                text='LINE群組內各國朋友留言即時互相翻譯\n適用交友群組,適用外國員工群組',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='收費標準及額外贈送功能',
                        text='*各國朋友LINE群組機器人\n*額外贈送功能:\n1.免費自動推播文字訊息給客戶(不受500則訊息限制)\n2.您可以設定以後的時間以line訊息提醒自己該辦的事情\n*收費標準:\n訂做收費:4000元(限時促銷價) \n訂閱收費:每月188元'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='更多了解功能',
                        uri='https://www.youtube.com/watch?v=bGAY-IY90H4'
                    ),
                    URITemplateAction(
                        label='免費試用或訂購',
                        uri='https://unitbesto.wixsite.com/mysite'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))     

def lineNotifyMessage(token, message, picurl):

      header = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
      payload = {
          'message':message,
          'imageThumbnail':picurl,
          'imageFullsize':picurl
      }
      r = requests.post("https://notify-api.line.me/api/notify", headers = header, data = payload)
      return r.status_code
