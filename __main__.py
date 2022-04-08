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

# пример того как может выглядеть расшифровка токена в кликовой ссылке креатива директа
direct_count_url = "https://yabs.yandex.ru/count/WrqejI_zO743dHe092vNR2qOhgnRbGK0SGGGWY0ntqp4OG00000u109mXfFitvZMxPkV0O01Ww6mnAMcoePOY07oxVBZWm6G0P2ymThLW8200fW1aBp1sbMu0TIdfSKZm05Ss07skFEW0U01tkdfe07e0LAW0iJKn1ZO0WBm0iBfqyaAc0FLrpAGnmJu1D7vAeW5qVaga0NjWyW1e0MVZGse1Thr2h05slKAk0MwxJBIa9da2A2fRcbZXECbgGSjrA1pWQmFQh07W82ODBW7W0Nn1qVVr0xYnliVW0W4Y07W2AAgeWp92c4_JwCBEFO_-0g0jHYg2n3-asEHBTG003Zf0OxDqmK0sGle2z7vAl0B2eWCfgFUlW6f303M_KHMsTC_w0od0k0DWu20m82048aEOt7JvWWewQ3JkiksZE7n9Q0Em8Gzs0u1eG_P3u0GkvhY8FN__m604NJ3ZAhF0Za_iH9MdWUQ7PldF-aISnEvTp6vVw3m4lWI0pAxllwFrfoJu1EwxJA05820W0AW5BhjCgWKxOF80SWK1xENzOq6w1I40j0LwiU7ZWRO5S6AzkoZZxpyO_2W5i2nvuq6oHRmFz0MfgFUlW615m3mFvWNuFJyBQWN2S0Nj1BO5y24FUWN0PaOe1WLi1Yc_f2E1hWO0T0O4FWOhlBjaQUDixdZ0O0PiFIuuj2zaRaWa1a1e1cg0x0Pk1dI6H9vOM9pNtDbSdPbSYzoDZ0rBJ7e6O320_0PWC83WHh__vFpmxNFJeWQm8Gzc1hyy8W2e1gbhil_W9QalFq1i1gxik7iYkZo_Ay1zHe10000WXjDCJOqC38rD3OuDpOqCp8nC2qnC3apDJOmE3WsC3SmD3KsCZarDorpONCoBJ0uCZKjSs5pBMmtBM9XR65kOsLoBJWmE30jGa5CBJGuDJUm6sIu6mNW6-s3o06278WS0kaSW1t_VvaTe1u1g1u1q1wv-FUuhw7XW9y1s1xwsXwW7xkQuY0Z03Y4O536KqHes7w8PEmX1iQbeLFH07TwaOV4PSlj5ZA6ECi5WX7_XZYliFFca2mWveGS98fJ9U17DxQw4GDhAHaCFD8MHUm30KIJnGGnBP_Ot5JlJ-CvEx3rFK2Jy8S7qNZ3wi4fHx0oVgn623m0~1/CPLe094OEOD0/C0YiN6g7aqAgIABINCrhcrcLw=="

import re
import base64
import proto.token_pb2 as token_pb2

token = re.search('(?:https://)?\w+\.yandex\.ru/count/[\w\d\-~]+/(\S+)', direct_count_url).groups()[0]
token_decoded = token_pb2.TToken.FromString(base64.b64decode(token))
print(f"Содержимое расшифрованнго токена из креатива директа:\n{MessageToJson(token_decoded)}\n")
'''
Содержимое расшифрованнго токена из креатива директа:
{
  "Hash": "3956600690",
  "ExternalCampaignId": "96418400",
  "ExternalId": "72057605541342984",
  "Time": "1639759042000"
}
'''