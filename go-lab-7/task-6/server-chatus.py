import asyncio
import websockets

connected_clients = set()

async def chat_server(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Получено: {message}")
            # Создаём задачи для отправки сообщений клиентам
            tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
            await asyncio.gather(*tasks)  # Ждём завершения всех задач
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(chat_server, "localhost", 8080):
        print("Сервер веб-сокетов запущен на ws://localhost:8080")
        await asyncio.Future()  # Блокируем выполнение, чтобы сервер продолжал работать

if __name__ == "__main__":
    asyncio.run(main())