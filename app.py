from flask import Flask,request,jsonify,render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    """ Главная страниуа - отдаёт веб_интерфейс """
    return render_template('index.html')

@app.route('/ask',methods=['POST'])
def ask_ai():
    """Обрабатывает вопросы и возвращает ответ от ии"""
    #получаем вопрос из json запроса
    user_question = request.json['question']

    #отправляем запрос к openai api
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"sistem",
        "content":"Ты - полезный персональный ассистент студента .Отвечай чётко и кратко.Для академических тем обьясняй концепции пошагово.Если не знаешь ответа ,скажи об этом честно."
            },
            {"role":"user",
             "content": user_question
             }
    ],
        max_tokens=500,
        temperature=0.7
    )

    #извлекаем текст ответа
    assistent_response = response.choices[0].message.content

    #Возвращаем JSON с ответом
    return jsonify({"response": assistent_response})

    if __name__ == "__main__":
     app.run(debug=True, port=5001)