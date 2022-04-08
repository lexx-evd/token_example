import hmac
import hashlib
import base64

import proto.token_pb2 as token_pb2
import proto.creative_pb2 as creative_pb2


# ключ для подписи токенов ОРД выдает ЕРИР тем же способом что и авторизационный токен
SECRET_VALUE = b'81HfzOpdfxfZlo4yiorWz5aSIUS1IMdr_U9I6ixsuoU'
# id ключа, нужен для ЕРИР, чтобы понять каким ключем проверять подпись
# (в том числе понадобится для перевыпуска ключа)
SECRET_ID = 1
SIGN_LENGTH = 8  # длина подписи (нет смысла делать значение большим - на криптостойкость не влияет)


def get_creative_proto():
    """
    Заполнение данных креатива и токена на примере тестового креатива от агенства "Перформанс Маркетинг"
    """
    creative = creative_pb2.TCreative()
    # image
    creative.CreativeData.MediaUrl.append("//avatars.mds.yandex.net/get-direct/5331841/JEl_atsADVgo9cpbkfjpDA/y300")
    # body
    creative.CreativeData.TextData.append("Семейные Легенды объединяют семью и сохраняют важные события каждого члена семьи!")
    # title
    creative.CreativeData.TextData.append("Семейные Легенды. Юрий Гагарин")
    creative.CreativeData.TargetingRegion.append("0")
    # href
    creative.Url = "https://family-universe.ru/public/912bdab6-2113-4873-a65c-8afcf9205103/family-tree?utm_source=yandex&utm_medium=cpc&utm_campaign=68717883&utm_content=11503415048&utm_term={PHRASE}"

    # "meta"-поля креатива, кажется, что добавлять их в хеш необходимости нет
    # (тем более ExternalId и ExternalCampaignId будут в токене и так)
    creative.ExternalCampaignId = "96418400"
    creative.ExternalId = "72057605541342984"
    creative.Type = "base"
    creative.Category = "200004017"
    return creative


def get_creative_hash(creative):
    """
    хешировать предлагатся значимые креатива, значения которых невозможно передавать в токене целиком
    """
    def _hash(data):
        """
        Конкретная реализация hash-функции нуждается в согласовании
        """
        return int(hashlib.sha256(data).hexdigest()[-8:], 16)

    creative_meaningfull_fields = creative_pb2.TCreative()
    creative_meaningfull_fields.CreativeData.CopyFrom(creative.CreativeData)
    creative_meaningfull_fields.Url = creative.Url
    return _hash(creative_meaningfull_fields.SerializeToString(deterministic=True))


def get_token_proto(creative, time):
    token = token_pb2.TToken()
    token.Hash = get_creative_hash(creative)
    token.ExternalCampaignId = int(creative.ExternalCampaignId)
    token.ExternalId = int(creative.ExternalId)
    token.Time = time
    return token


def get_token(creative, time):
    token_proto = get_token_proto(creative, time)
    value = base64.b64encode(token_proto.SerializeToString())
    sign = hmac.new(SECRET_VALUE, value, hashlib.sha256).hexdigest()[:SIGN_LENGTH]
    return '.'.join([str(SECRET_ID), sign, value.decode()])


def check_sign(token):
    secret_id, sign, value = token.split('.', 2)
    return sign == hmac.new(SECRET_VALUE, value.encode(), hashlib.sha256).hexdigest()[:SIGN_LENGTH]


def parse_proto_from_token(token):
    secret_id, sign, value = token.split('.', 2)
    return token_pb2.TToken.FromString(
        base64.b64decode(value)
    )
