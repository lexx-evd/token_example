from google.protobuf.json_format import MessageToJson, Parse

import proto.creative_pb2 as creative_pb2
import utils


creative_proto = utils.get_creative_proto()
creative_json = MessageToJson(creative_proto, ensure_ascii=False)
print(f"Данные, которые отправляются в ЕРИР (/creative):\n{creative_json}\n")
'''
Данные, которые отправляются в ЕРИР (/creative):
{
  "externalCampaignId": "96418400",
  "externalId": "72057605541342984",
  "type": "base",
  "url": "https://family-universe.ru/public/912bdab6-2113-4873-a65c-8afcf9205103/family-tree?utm_source=yandex&utm_medium=cpc&utm_campaign=68717883&utm_content=11503415048&utm_term={PHRASE}",
  "category": "200004017",
  "creativeData": {
    "mediaUrl": [
      "//avatars.mds.yandex.net/get-direct/5331841/JEl_atsADVgo9cpbkfjpDA/y300"
    ],
    "textData": [
      "Семейные Легенды объединяют семью и сохраняют важные события каждого члена семьи!",
      "Семейные Легенды. Юрий Гагарин"
    ],
    "targetingRegion": [
      "0"
    ]
  }
}
'''

token = utils.get_token(creative_proto, time=1639759042000)
print(f"Значение токена, которое будет доступно при показе банера:\n{token}\n")
'''
Значение токена, которое будет доступно при показе банера:
1.968b1821.CPLe094OEOD0/C0YiN6g7aqAgIABINCrhcrcLw==
'''

print(f"Подпись корректна: {utils.check_sign(token)}")
token_decoded = utils.parse_proto_from_token(token)
print(f"Содержимое расшифрованнго токена:\n{MessageToJson(token_decoded)}\n")
'''
Подпись корректна: True
Содержимое расшифрованнго токена:
{
  "Hash": "3956600690",
  "ExternalCampaignId": "96418400",
  "ExternalId": "72057605541342984",
  "Time": "1639759042000"
}
'''

creative_proto_from_json = Parse(creative_json, creative_pb2.TCreative())
print(f"Hash в токене соотвествует данным креатива: {token_decoded.Hash == utils.get_creative_hash(creative_proto_from_json)}")
'''
Hash в токене соотвествует данным креатива: True
'''
