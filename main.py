import asyncio
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import ChannelPrivateError
import re

# Настройки
api_id = '20909352'
api_hash = 'a3be2584a77447cfc0c7d1595076e9dc'
phone_number = '+923559486166'

# ID каналов
source_channel_id = -1002355660075
target_channel_id = -1002464185343
source_channel_id_2 = -1002335869892
target_channel_id_2 = -1002283473746

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)

# Функция для форматирования supply
def format_supply(supply):
    supply = int(supply)
    if supply >= 1000:
        supply = f"{supply // 1000}k"
    return supply

@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    message = event.message.message
    gift_id = ""

    if "A new limited gift has appeared" in message:
        price = ""
        supply = ""
        
        # Извлечение значений из сообщения
        for line in message.split('\n'):
            if "№" in line:
                gift_id = re.search(r'\((.*?)\)', line).group(1)
            if "Price:" in line:
                price = line.split(': ')[1].split(' ')[0]
            if "Total amount:" in line:
                supply = format_supply(line.split(': ')[1].replace(',', ''))

        # Формирование нового сообщения для лимитированных подарков
        new_message = f"⬆️ <b>New gift! Новый подарок!</b>\n\nPrice: <code>{price}</code>★ (<b>limited:</b> {supply} gifts only)\n\n<b>@TGGiftsNews • @InsiderDurova</b>"
        
        try:
            await client.send_message(target_channel_id, new_message, buttons=[
                [Button.inline("Copy Gift ID", data=gift_id)]
            ], parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    elif "A new gift has appeared" in message:
        price = ""
        
        # Извлечение значения цены из сообщения
        for line in message.split('\n'):
            if "№" in line:
                gift_id = re.search(r'\((.*?)\)', line).group(1)
            if "Price:" in line:
                price = line.split(': ')[1].split(' ')[0]

        # Формирование нового сообщения для нелимитированных подарков
        new_message = f"⬆️ <b>New gift! Новый подарок!</b>\n\nPrice: <code>{price}</code>★ (non-limited)"

        try:
            await client.send_message(target_channel_id, new_message, buttons=[
                [Button.inline("Copy Gift ID", data=gift_id)]
            ], parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    # Проверка на наличие стикера или анимированного стикера в сообщении
    if event.message.sticker or (event.message.file and event.message.file.mime_type == "application/x-tgsticker"):
        try:
            await client.send_file(target_channel_id, event.message.media)
        except ChannelPrivateError:
            print("Failed to send sticker: Bot lacks permission to access the target channel.")

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    await event.answer(f"Gift ID: {data}", alert=True)

@client.on(events.NewMessage(chats=source_channel_id_2))
async def handler_2(event):
    message = event.message.message
    if "Roxman @borz bought" in message:
        parts = message.split()
        number_of_stars = parts[3]  # Количество звезд идет после слова "bought"
        amount_ton = parts[6]  # Сумма TON идет перед словом "TON"
        # Извлечение даты после символа "—"
        date_time_str = message.split('— ')[1]
        new_message = f"Roxman купил <b>{number_of_stars}⭐</b> за <b>{amount_ton}</b> TON — {date_time_str}"
        try:
            await client.send_message(target_channel_id_2, new_message, parse_mode='html')
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    # Проверка на наличие стикера или анимированного стикера в сообщении
    if event.message.sticker or (event.message.file and event.message.file.mime_type == "application/x-tgsticker"):
        try:
            await client.send_file(target_channel_id_2, event.message.media)
        except ChannelPrivateError:
            print("Failed to send sticker: Bot lacks permission to access the target channel.")

async def restart_client():
    while True:
        await asyncio.sleep(600)  # 10 минут
        if not client.is_connected():
            await client.connect()
            print("Client Reconnected")

async def main():
    await client.start(phone=phone_number)
    print("Client Created")
    asyncio.create_task(restart_client())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())