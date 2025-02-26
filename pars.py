import PyPDF2
import re
import telebot
import time
import sys
import random

# Установите кодировку консоли на UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Initialize the bot with your token
bot_token = 'TOKEN'  # Замените на токен вашего бота
bot = telebot.TeleBot(bot_token)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    print(f"Opening PDF file: {pdf_path}")  # Debug print
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    print("Extracted text from PDF")  # Debug print
    return text

# Function to extract questions and answers
def extract_questions_answers(text):
    print("Extracting questions and answers")  # Debug print
    qa_pattern = re.compile(r'\d+\.\s+\[T\d+\]\s+(.*?)\s+А\)\s+(.*?)\s+Б\)\s+(.*?)\s+В\)\s+(.*?)\s+Г\)\s+(.*?)\s', re.DOTALL)
    matches = qa_pattern.findall(text)
    print(f"Found matches: {matches}")  # Debug print
    return matches

# Function to send questions and answers to Telegram as a quiz
def send_quiz_to_telegram(chat_id, questions_answers):
    print(f"Sending messages to chat_id: {chat_id}")  # Debug print
    for question, a, b, c, d in questions_answers:
        options = [a, b, c, d]
        random.shuffle(options)
        correct_option_id = options.index(a)  # Найти индекс правильного ответа после перемешивания
        options = [option[:100] for option in options]  # Обрезать варианты ответов до 100 символов
        message = f"Q: {question}"
        print(f"Sending quiz: {message}")  # Debug print
        print(f"Options: {options}")  # Debug print
        bot.send_poll(chat_id, question, options, type='quiz', correct_option_id=correct_option_id, explanation=f"Правильный ответ: {a}")
        time.sleep(3)  # Interval between sending messages
    print("All messages sent")  # Debug print

# Main function
def main():
    pdf_path = r'ПУТЬ_К_ФАЙЛУ.pdf'  # Замените на путь к вашему PDF-файлу
    chat_id = '@'  # Замените на идентификатор вашего канала
    
    print("Starting main function")  # Debug print
    text = extract_text_from_pdf(pdf_path)
    print("Extracted text")  # Debug print
    questions_answers = extract_questions_answers(text)
    print("Extracted questions and answers:", questions_answers)  # Debug print
    send_quiz_to_telegram(chat_id, questions_answers)
    print("Main function completed")  # Debug print

if __name__ == "__main__":
    main()