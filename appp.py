from flask import Flask, render_template, request, jsonify
from gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

conversation = []

SYSTEM_PROMPT = """
Ты — Emy, дружелюбный персональный AI-ассистент.
Помогай пользователю с учёбой, программированием,
планированием, расписанием и обычными вопросами.
Отвечай на русском языке, если пользователь пишет по-русски.
"""

def ask_emy(user_message):

    print("1. Получен вопрос:", user_message)

    credentials = os.getenv("GIGACHAT_CREDENTIALS")

    print("2. API ключ найден:", bool(credentials))

    if not credentials:
        return "Ошибка: GIGACHAT_CREDENTIALS не найден в .env"

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(conversation[-20:])

    messages.append({
        "role": "user",
        "content": user_message
    })

    print("3. Подключаемся к GigaChat...")

    try:
        with GigaChat(
            credentials=credentials,
            scope=os.getenv(
                "GIGACHAT_SCOPE",
                "GIGACHAT_API_PERS"
            ),
            model="GigaChat-3-Ultra"
        ) as giga:

            print("4. Отправляем запрос...")

            response = giga.chat(messages)

            print("5. Ответ получен!")

            answer = response.choices[0].message.content

            print("6. Ответ:", answer)

            conversation.append({
                "role": "user",
                "content": user_message
            })

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

    except Exception as e:

        print("ОШИБКА GIGACHAT:")
        print(type(e).__name__)
        print(str(e))

        return "Ошибка GigaChat: " + str(e)


@app.route("/")
def index():
    print("Открыта главная страница")
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    print("\n========== НОВЫЙ ЗАПРОС ==========")

    print("Получен POST /ask")

    try:

        data = request.json

        print("Данные:", data)

        if not data:
            return jsonify({
                "answer": "Сервер не получил данные."
            })

        user_message = data.get("message", "").strip()

        print("Сообщение пользователя:", user_message)

        if not user_message:
            return jsonify({
                "answer": "Я не услышала вопрос."
            })

        answer = ask_emy(user_message)

        print("Возвращаем ответ браузеру:", answer)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ОШИБКА /ask:")
        print(type(e).__name__)
        print(str(e))

        return jsonify({
            "answer": "Ошибка сервера: " + str(e)
        })


if __name__ == "__main__":

    print("================================")
    print("EMy запущена")
    print("http://127.0.0.1:5000")
    print("================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )