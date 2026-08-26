from flask import Flask, render_template, request, jsonify
from gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

SYSTEM_PROMPT = """
Ты — Emy, персональный AI-ассистент пользователя.

Твоё имя — Emy.

Ты дружелюбная, спокойная и умная помощница.
Обращайся к пользователю естественно, без лишней официальности.

Твои основные задачи:
1. Помогать с учёбой.
2. Объяснять сложные темы простыми словами.
3. Помогать с программированием.
4. Составлять планы обучения.
5. Помогать организовывать день.
6. Работать с расписанием пользователя.
7. Помогать планировать задачи.
8. Отвечать на обычные вопросы.
9. Поддерживать естественный диалог.

Если пользователь просит объяснить тему:
- сначала объясни простыми словами;
- затем приведи пример;
- если это учёба, можешь добавить короткую проверку понимания.

Если пользователь просит составить план:
- учитывай уже известные задачи;
- не создавай невозможное расписание;
- оставляй время на отдых.

Ты не должна притворяться, что умеешь выполнять действие,
если соответствующая функция ещё не подключена.

Отвечай на языке пользователя.
Если пользователь пишет на русском — отвечай на русском.
"""

conversation = []


def ask_emy(user_message):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Добавляем историю разговора
    messages.extend(conversation[-20:])

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        with GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
            model="GigaChat-3-Ultra"
        ) as giga:

            response = giga.chat(messages)

            answer = response.choices[0].message.content

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
        print("ERROR:", e)
        return f"Ошибка подключения к GigaChat: {e}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "answer": "Я не услышала вопрос."
        })

    answer = ask_emy(user_message)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )