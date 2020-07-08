from whatsgramstickers.WhatsGramSticker import WhatsGramSticker
from telegram.utils import request

request.CON_POOL_SIZE = 10

WGS = WhatsGramSticker()
