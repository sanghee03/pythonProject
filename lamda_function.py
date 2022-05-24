# -*- coding: utf-8 -*-
import json, random
import httplib
from botocore.vendored import requests


def lambda_handler(event, context):
    slack_url = "{YOUR_SLACK_INCOMING_WEBHOOK_URL}"

    eat_list = getRandomDatas()
    fields = []

    for data in eat_list:
        tmp_title = data['title']
        if data['url'] != "":
            tmp_title += "<{}>".format(data['url'])
        fields.append({
            "title": tmp_title,
            "value": "{}\n{}\n".format(data['menu'], data['description']),
            "short": False
        })
    title = "안녕. 나는 EAT-BOT이야. 메뉴를 추천해줄께!"


payloads = {
    "attachments": [{
        "pretext": title,
        "color": "#0099A6",
        "fields": fields
    }]
}
response = requests.post(
    slack_url, data=json.dumps(payloads),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


def getRandomDatas():
    json_data = open('data.json').read()
    datas = json.loads(json_data)
    random.shuffle(datas)
    tmp = random.sample(datas, 3)
    return tmp
