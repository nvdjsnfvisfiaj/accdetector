import logging
import re
import asyncio
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import ChannelPrivateError
from telethon.tl.types import PeerChannel

# Настройки
api_id = 20909352  # Ваш API ID, полученный с https://my.telegram.org
api_hash = "a3be2584a77447cfc0c7d1595076e9dc"  # Ваш API Hash, полученный с https://my.telegram.org
phone_number = '+923559486166'

# ID каналов
source_channel_id = -1002452764624
target_channel_id = -1002212238461
source_channel_id_2 = -1002335869892
target_channel_id_2 = -1002283473746

# ID для групп из первого кода
SOURCE_GROUP_ID = -1002459101321
DESTINATION_GROUP_ID = -1002680292174

# Словарь для слов и соответствующих ID топиков
WORD_TO_TOPIC_ID = {
    "B-Day Candle": 227,
    "Desk Calendar": 224,
    "Homemade Cake": 221,
    "Sakura Flower": 218,
    "Lol Pop": 215,
    "Spy Agaric": 212,
    "Eternal Candle": 209,
    "Witch Hat": 206,
    "Scared Cat": 203,
    "Voodoo Doll": 200,
    "Flying Broom": 197,
    "Crystall Ball": 194,
    "Skull Flower": 191,
    "Trapped Heart": 188,
    "Mad Pumpkin": 185,
    "Sharp Tongue": 182,
    "Ion Gem": 179,
    "Evil Eye": 176,
    "Hex Pot": 173,
    "Hypno Lollipop": 170,
    "Kissed Frog": 167,
    "Electric Skull": 164,
    "Magic Potion": 161,
    "Record Player": 158,
    "Vintage Cigar": 155,
    "Berry Box": 152,
    "Eternal Rose": 149,
    "Mini Oscar": 146,
    "Perfume Bottle": 143,
    "Love Candle": 140,
    "Durov's Cap": 137,
    "Hanging Star": 134,
    "Jelly Bunny": 131,
    "Spiced Wine": 127,
    "Plush Pepe": 124,
    "Precious Peach": 121,
    "Astral Shard": 118,
    "Genie Lamp": 115,
    "Signet Ring": 112,
    "Swiss Watch": 109,
    "Bunny Muffin": 106,
    "Star Notepad": 103,
    "Jester Hat": 100,
    "Sleigh Bell": 97,
    "Snow Mittens": 94,
    "Snow Globe": 91,
    "Santa Hat": 88,
    "Winter Wreath": 85,
    "Ginger Cookie": 82,
    "Jingle Bells": 79,
    "Party Sparkler": 76,
    "Cookie Heart": 73,
    "Candy Cane": 69,
    "Tama Gadget": 66,
    "Lunar Snake": 63,
    "Loot Bag": 60,
    "Diamond Ring": 57,
    "Toy Bear": 54,
    "Love Potion": 51,
    "Top Hat": 48,
    "Neko Helmet": 45
}

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)

# Функция для форматирования supply
def format_supply(supply):
    supply = int(supply)
    if supply >= 1000:
        supply = f"{supply // 1000}k"
    return supply

# Обработчик сообщений для SOURCE_GROUP_ID (из первого кода)
@client.on(events.NewMessage)
async def handle_messages(event):
    try:
        if event.chat_id == SOURCE_GROUP_ID:
            for word, topic_id in WORD_TO_TOPIC_ID.items():
                if word in event.message.message:
                    logging.info(f"Найдено слово: '{word}', пересылаем в топик ID: {topic_id}")
                    await client.send_message(
                        entity=PeerChannel(DESTINATION_GROUP_ID),
                        message=event.message.message,
                        reply_to=topic_id
                    )
                    logging.info(f"Сообщение успешно переслано в топик ID: {topic_id}")
                    return
            logging.warning("Слово для пересылки не найдено в сообщении.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

# Обработчик сообщений для лимитированных подарков
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    message = event.message.message
    gift_id = ""

    if "A new limited gift has appeared" in message:
        price = ""
        supply = ""
        for line in message.split('\n'):
            if "№" in line:
                gift_id = re.search(r'\((.*?)\)', line).group(1)
            if "Price:" in line:
                price = line.split(': ')[1].split(' ')[0]
            if "Total amount:" in line:
                supply = format_supply(line.split(': ')[1].replace(',', ''))

        new_message = f"⬆️ <b>New gift! Новый подарок!</b>\n\nPrice: <code>{price}</code>★ (<b>limited:</b> {supply} gifts only)\n\n<b>@TGGiftsNews • @InsiderDurova</b>"
        try:
            await client.send_message(target_channel_id, new_message, buttons=[
                [Button.inline("Copy Gift ID", data=gift_id)]
            ], parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    elif "A new gift has appeared" in message:
        price = ""
        for line in message.split('\n'):
            if "№" in line:
                gift_id = re.search(r'\((.*?)\)', line).group(1)
            if "Price:" in line:
                price = line.split(': ')[1].split(' ')[0]

        new_message = f"⬆️ <b>New gift! Новый подарок!</b>\n\nPrice: <code>{price}</code>★ (non-limited)"
        try:
            await client.send_message(target_channel_id, new_message, buttons=[
                [Button.inline("Copy Gift ID", data=gift_id)]
            ], parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    if event.message.sticker or (event.message.file and event.message.file.mime_type == "application/x-tgsticker"):
        try:
            await client.send_file(target_channel_id, event.message.media)
        except ChannelPrivateError:
            print("Failed to send sticker: Bot lacks permission to access the target channel.")

# Обработчик CallbackQuery
@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    await event.answer(f"Gift ID: {data}", alert=True)

# Обработчик сообщений для source_channel_id_2
@client.on(events.NewMessage(chats=source_channel_id_2))
async def handler_2(event):
    message = event.message.message
    if "Roxman @borz bought" in message:
        parts = message.split()
        number_of_stars = parts[3]
        amount_ton = parts[6]
        date_time_str = message.split('— ')[1]
        new_message = f"Roxman купил <b>{number_of_stars}⭐</b> за <b>{amount_ton}</b> TON — {date_time_str}"
        try:
            await client.send_message(target_channel_id_2, new_message, parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    if event.message.sticker or (event.message.file and event.message.file.mime_type == "application/x-tgsticker"):
        try:
            await client.send_file(target_channel_id_2, event.message.media)
        except ChannelPrivateError:
            print("Failed to send sticker: Bot lacks permission to access the target channel.")

# Функция для перезапуска клиента
async def restart_client():
    while True:
        await asyncio.sleep(600)
        if not client.is_connected():
            await client.connect()
            print("Client Reconnected")

# Основная функция
async def main():
    await client.start(phone=phone_number)
    logging.info("Клиент Telegram запущен.")
    asyncio.create_task(restart_client())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())