import asyncio
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import ChannelPrivateError
import re

# Настройки
api_id = '20909352'
api_hash = 'a3be2584a77447cfc0c7d1595076e9dc'
phone_number = '+923559486166'

# ID каналов
source_channel_id = -1002454039581  # ID исходного канала (1)
target_channel_id = -1002212238461  # ID целевого канала (1)
source_channel_id_2 = -1002335869892  # ID исходного канала (2)
target_channel_id_2 = -1002283473746  # ID целевого канала (2)
source_channel_id_3 = -1002485605769 # ID исходного канала (3) для NFT улучшений
target_channel_id_3 = -1002212238461  # ID целевого канала (3) для NFT улучшений

# Имя пользователя для отправки сообщений
username = '@asteroalex'

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)

# Функция для отправки периодических сообщений
async def periodic_messages():
    while True:
        try:
            await client.send_message(username, "Привет, работаю")
        except ValueError:
            print(f"Пользователь {username} недоступен. Проверьте, что он взаимодействовал с ботом.")
        await asyncio.sleep(1800)  # 900 секунд = 15 минут

# Функция для отправки сообщения при запуске
async def send_startup_message():
    try:
        await client.send_message(username, "Запущено успешно!")
    except ValueError:
        print(f"Пользователь {username} недоступен. Проверьте, что он взаимодействовал с ботом.")

# Функция для форматирования supply
def format_supply(supply):
    supply = int(supply)
    if supply >= 1000:
        return f"{supply // 1000}k"
    return str(supply)

# Обработка сообщений из первого исходного канала
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    message = event.message.message

    # Проверяем, содержит ли сообщение слово "LIMITED"
    if "LIMITED" in message:
        try:
            # Извлечение значений price и supply
            price_match = re.search(r"Price: (\d+)", message)
            supply_match = re.search(r"LIMITED \((\d+)\)", message)

            if price_match and supply_match:
                price = price_match.group(1)  # Извлекаем значение price
                supply = format_supply(supply_match.group(1))  # Извлекаем и форматируем supply

                # Формирование нового сообщения для лимитированных подарков
                new_message = (
                    f"⬆️ <b>New gift! Новый подарок!</b>\n\n"
                    f"Price: <code>{price}</code>★ (<b>limited:</b> {supply} gifts only)\n\n"
                    f"<b>🎁 <a href='https://t.me/AutoGiftRobot?start=_tgr_D7aIRUlmM2Yy'>@AutoGiftRobot</a> • @TGGiftsNews</b>\n"
                    f"<b>🌸 <a href='https://t.me/tonnel_network_bot/gifts?startapp=ref_1267171169'>Купить/продать подарки</a></b>"
                )

                # Отправка сообщения в целевой канал без предпросмотра ссылок
                await client.send_message(
                    target_channel_id,
                    new_message,
                    buttons=[[Button.inline("Copy Gift ID", data="N/A")]],
                    parse_mode='html',
                    link_preview=False  # Отключение предпросмотра ссылок
                )
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    # Проверяем на нелимитированные подарки (не содержит "LIMITED", но содержит "Price:")
    elif "Price:" in message and "LIMITED" not in message:
        try:
            # Извлечение значения price
            price_match = re.search(r"Price: (\d+)", message)

            if price_match:
                price = price_match.group(1)  # Извлекаем значение price

                # Формирование нового сообщения для нелимитированных подарков
                new_message = (
                    f"⬆️ <b>New gift! Новый подарок!</b>\n\n"
                    f"Price: <code>{price}</code>★\n\n"
                    f"<b>🎁 <a href='https://t.me/AutoGiftRobot?start=_tgr_D7aIRUlmM2Yy'>@AutoGiftRobot</a> • @TGGiftsNews</b>\n"
                    f"<b>🌸 <a href='https://t.me/tonnel_network_bot/gifts?startapp=ref_1267171169'>Купить/продать подарки</a></b>"
                )

                # Отправка сообщения в целевой канал без предпросмотра ссылок
                await client.send_message(
                    target_channel_id,
                    new_message,
                    buttons=[[Button.inline("Copy Gift ID", data="N/A")]],
                    parse_mode='html',
                    link_preview=False  # Отключение предпросмотра ссылок
                )
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

    # Проверка на наличие стикера или анимированного стикера в сообщении
    if event.message.sticker or (event.message.file and event.message.file.mime_type == "application/x-tgsticker"):
        try:
            await client.send_file(target_channel_id, event.message.media)
        except ChannelPrivateError:
            print("Failed to send sticker: Bot lacks permission to access the target channel.")

# Обработка сообщений из второго исходного канала
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

# Обработка сообщений из третьего исходного канала для NFT улучшений
@client.on(events.NewMessage(chats=source_channel_id_3))
async def handler_3(event):
    message = event.message.message

    # Проверка на наличие строки "NFT upgrade available"
    if "upgrade available" in message:
        try:
            # Формирование нового сообщения для NFT улучшений
            new_message = (
                f"🆕 <b>New NFT upgrades! Доступны новые улучшения!</b>\n\n"
                f"<code>Подарки которые получили NFT скины будут показаны здесь через пару секунд</code>\n\n"
                f"<b>🎁 <a href='https://t.me/AutoGiftRobot?start=_tgr_D7aIRUlmM2Yy'>@AutoGiftRobot</a> • @TGGiftsNews</b>\n"
                f"<b>🌸 <a href='https://t.me/tonnel_network_bot/gifts?startapp=ref_1267171169'>Купить/продать подарки</a></b>"
            )

            # Отправка сообщения в целевой канал без предпросмотра ссылок
            await client.send_message(
                target_channel_id_3,
                new_message,
                parse_mode='html',
                link_preview=False  # Отключение предпросмотра ссылок
            )
        except ChannelPrivateError:
            print("Failed to send message: Bot lacks permission to access the target channel.")

# Обработка кнопок
@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    await event.answer(f"Gift ID: {data}", alert=True)

# Основная функция
async def main():
    await client.start(phone=phone_number)
    print("Client Created")
    # Отправка сообщения при запуске
    await send_startup_message()
    # Запуск периодических сообщений
    asyncio.create_task(periodic_messages())
    # Ожидание завершения работы клиента
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())