import asyncio
from telethon import TelegramClient, events

# Настройки
api_id = '20909352'
api_hash = 'a3be2584a77447cfc0c7d1595076e9dc'
phone_number = '+923559486166'

# ID каналов
source_channel_id = -1002452764624
target_channel_id = -1002212238461
source_channel_id_2 = -1002335869892
target_channel_id_2 = -1002283473746

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    message = event.message.message
    if "A new limited gift has appeared" in message or "A new gift has appeared" in message:
        await client.send_message(target_channel_id, message)

@client.on(events.NewMessage(chats=source_channel_id_2))
async def handler_2(event):
    message = event.message.message
    if "Roxman @borz bought" in message:
        parts = message.split()
        number_of_stars = parts[3]  # Количество звезд идет после слова "bought"
        amount_ton = parts[6]  # Сумма TON идет перед словом "TON"
        # Извлечение даты после символа "—"
        date_time_str = message.split('— ')[1]
        new_message = f"Roxman купил {number_of_stars}⭐ за {amount_ton} TON — {date_time_str}"
        await client.send_message(target_channel_id_2, new_message)

async def restart_client():
    while True:
        await asyncio.sleep(1200000000000)  # 10 минут
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