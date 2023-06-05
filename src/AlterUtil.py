import requests
import json


# 飞书
def feishu(text, url):
    json_text = {
        "msg_type": "text",
        "content": {
            "msg": "数据质量检测-告警通知",
            "text": text
        }
    }
    # Webhook地址替换成自己的
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    print(requests.post(url, json.dumps(json_text), headers=headers).content)


# 判断是什么类型
def alter(type, text, url):
    if type == 'feishu':
        feishu(text, url)
    else:
        raise Exception(f'告警不支持 {type}')


if __name__ == '__main__':
    alter('feishu', '这是测试告警', 'https://open.feishu.cn/open-apis/bot/v2/hook/b3fd988a-cc12-457e-89f2-xxxx')
