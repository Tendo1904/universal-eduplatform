import telebot
from telebot import types
import sqlite3
import numpy as np
import config_eduplatform

TOKEN = config_eduplatform.bot_token
bot = telebot.TeleBot(TOKEN)


def connect_db():
    """
    Connect to a SQLite database.
    
    Args:
        None
    
    Returns:
        SQLite connection object for the database.
    """
    return sqlite3.connect('test_bot.db')


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Summary:
        Display a start message with navigation buttons in a chat using the Telegram bot.
    
    Parameters:
        message: The incoming message object from the chat.
    
    Args:
        message: telegram.Message
            The incoming message object from the chat.
    
    Return:
        This method does not return any value.
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    register_button = types.KeyboardButton('Регистрация')
    login_button = types.KeyboardButton('Авторизация')
    markup.add(register_button, login_button)
    bot.send_message(chat_id, "Добро пожаловать! Используйте кнопки ниже для навигации.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Регистрация')
def register(message):
    """
    Registers a user by checking if the user is already registered based on the given message. If the user is not registered, prompts the user to enter a phone number for registration.
    
    Parameters:
    - message: the message object containing information about the chat
    
    Returns:
    None
    
    Args:
    - message: the message object containing information about the chat
    
    Return:
    None
    """
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (chat_id,))
    if cursor.fetchone():
        bot.send_message(chat_id, "Вы уже зарегистрированы!")
    else:
        msg = bot.send_message(chat_id, "Введите номер телефона:")
        bot.register_next_step_handler(msg, process_register_phone)


def process_register_phone(message):
    """
    Summary:
        Process registration of a phone number.
    
    Args:
        message: Represents the message object containing chat and phone information.
    
    Returns:
        None
    
    Args:
        message: Represents the message object containing chat and phone information.
    
    Returns:
        None
    """
    chat_id = message.chat.id
    phone = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    if cursor.fetchone():
        bot.send_message(chat_id, "Этот номер телефона уже зарегистрирован.")
        return
    msg = bot.send_message(chat_id, "Введите пароль:")
    bot.register_next_step_handler(msg, process_register_password, phone)


def process_register_password(message, phone):
    """
    Processes the registration password entered by the user and prompts for their first name.
    
    Parameters:
    - message: The message object containing the user input.
    - phone: The user's phone number used for registration.
    
    Args:
    - message: The message object containing the user input.
    - phone: The user's phone number used for registration.
    
    Returns:
    None
    """
    chat_id = message.chat.id
    password = message.text
    msg = bot.send_message(chat_id, "Введите ваше имя:")
    bot.register_next_step_handler(msg, process_register_first_name, phone, password)


def process_register_first_name(message, phone, password):
    """
    Processes the registration of a user's first name by sending a message to the chat for input.
    
    Parameters:
    - message: The message object containing user input.
    - phone: The phone number of the user.
    - password: The user's password for registration.
    
    Args:
    - message: The message object containing user input.
    - phone: The phone number of the user.
    - password: The user's password for registration.
    
    Returns:
    None
    """
    chat_id = message.chat.id
    first_name = message.text
    msg = bot.send_message(chat_id, "Введите вашу фамилию:")
    bot.register_next_step_handler(msg, process_register_last_name, phone, password, first_name)


def process_register_last_name(message, phone, password, first_name):
    """
    Processes the registration of a user's last name and stores it in the database.
        
        Parameters:
        - message: The message object containing chat information.
        - phone: The user's phone number.
        - password: The user's password.
        - first_name: The user's first name.
        
        Returns:
        - None
    """
    chat_id = message.chat.id
    last_name = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (id, phone, password, first_name, last_name, score) VALUES (?, ?, ?, ?, ?, ?)",
                   (chat_id, phone, password, first_name, last_name, 0))
    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    createtest_button = types.KeyboardButton('Создать тест')
    starttest_button = types.KeyboardButton('Пройти тест')
    viewrating_button = types.KeyboardButton('Посмотреть рейтинг')
    markup.add(createtest_button, starttest_button, viewrating_button)
    bot.send_message(chat_id, f"Регистрация завершена! Ваш логин: {phone}", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Авторизация')
def login(message):
    """
    Logs in a user by prompting them to enter their phone number.
    
    Args:
    - message: The message object containing information for the chat session.
    
    Returns:
    None
    """
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите номер телефона:")
    bot.register_next_step_handler(msg, process_login_phone)


def process_login_phone(message):
    """
    Process the login phone number provided by the user.
    
    Parameters:
    - message: The message object containing information about the incoming message.
    
    Args:
    - message (object): The message object containing information about the incoming message.
    
    Return:
    - None
    """
    chat_id = message.chat.id
    phone = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    user = cursor.fetchone()
    if user:
        msg = bot.send_message(chat_id, "Введите пароль:")
        bot.register_next_step_handler(msg, process_login_password, phone)
    else:
        bot.send_message(chat_id,
                         "Пользователь с таким номером телефона не найден. Пожалуйста, зарегистрируйтесь или введите номер телефона повторно.")
        login(message)


def process_login_password(message, phone):
    """
    Processes login and password for user authentication.
        
        Parameters:
        - message: Represents the message object containing user input data.
        - phone: Represents the user's phone number used for login.
        
        Returns:
        None
    """
    chat_id = message.chat.id
    password = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE phone = ? AND password = ?", (phone, password))
    user = cursor.fetchone()
    if user:
        # Пользователь успешно авторизован
        user_id = user[0]
        cursor.execute("UPDATE users SET id = ? WHERE phone = ?", (chat_id, phone))
        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        createtest_button = types.KeyboardButton('Создать тест')
        starttest_button = types.KeyboardButton('Пройти тест')
        viewrating_button = types.KeyboardButton('Посмотреть рейтинг')
        markup.add(createtest_button, starttest_button, viewrating_button)
        bot.send_message(chat_id, f"Авторизация успешна! Ваш логин: {phone}", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Неправильный пароль, попробуйте снова.")
        login(message)


@bot.message_handler(func=lambda message: message.text == 'Создать тест')
def createtest(message):
    """
    Creates a new test based on the message received from the user.
        
        Parameters:
        - message: The message object containing information about the chat and user.
        
        Returns:
        None
    """
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (chat_id,))
    user = cursor.fetchone()
    if user:
        msg = bot.send_message(chat_id, "Введите тему теста:")
        bot.register_next_step_handler(msg, process_create_topic)
    else:
        bot.send_message(chat_id,
                         "Пожалуйста, авторизуйтесь с помощью кнопки 'Авторизация' или зарегистрируйтесь с помощью кнопки 'Регистрация'.")


def process_create_topic(message):
    """
    Processes the creation of a new topic for user tests in a chat.
    
    Args:
    - message: The message object containing information about the chat and topic.
    
    Returns:
    - None
    """
    chat_id = message.chat.id
    topic = message.text
    user_tests[chat_id] = {'topic': topic, 'questions': []}
    msg = bot.send_message(chat_id, "Выберите уровень сложности (легкий, средний, сложный):")
    bot.register_next_step_handler(msg, process_create_difficulty)


def process_create_difficulty(message):
    """
    Processes the creation of a difficulty level for a user in a chat, based on the received message.
    
    Args:
    - message: The message object containing information about the chat and user input.
    
    Return:
    None
    """
    chat_id = message.chat.id
    difficulty = message.text.lower()
    if difficulty in ['легкий', 'средний', 'сложный']:
        user_tests[chat_id]['difficulty'] = difficulty
        msg = bot.send_message(chat_id, "Введите вопрос:")
        bot.register_next_step_handler(msg, process_create_question)
    else:
        bot.send_message(chat_id, "Некорректный уровень сложности. Попробуйте снова.")
        process_create_topic(message)


def process_create_question(message):
    """
    Processes the creation of a new question in the chat. Appends the new question to the user_tests dictionary under the specific chat_id with empty lists for answers and correct answers. Sets up a custom reply keyboard markup for interaction. Prompts for an answer input or completion confirmation.
    
    Args:
    - message: The message object containing the question text and chat information.
    
    Return:
    - None
    """
    chat_id = message.chat.id
    question = message.text
    user_tests[chat_id]['questions'].append({'question': question, 'answers': [], 'correct_answers': []})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_answer_button = types.KeyboardButton('Добавить ответ')
    done_button = types.KeyboardButton('Готово')
    markup.add(add_answer_button, done_button)
    bot.send_message(chat_id, "Введите вариант ответа или нажмите 'Готово' для завершения:", reply_markup=markup)
    bot.register_next_step_handler(message, process_create_answers)


def process_create_answers(message):
    """
    Process the creation of answers for a chat bot quiz question.
    
    Args:
        message: The message object containing user input for creating answers.
    
    Returns:
        None
    """
    chat_id = message.chat.id
    if message.text == 'Готово':
        msg = bot.send_message(chat_id, "Введите правильный ответ (если несколько, через запятую):")
        bot.register_next_step_handler(msg, process_create_correct_answer)
    else:
        answer = message.text
        user_tests[chat_id]['questions'][-1]['answers'].append(answer)
        msg = bot.send_message(chat_id, "Введите вариант ответа или нажмите 'Готово' для завершения:")
        bot.register_next_step_handler(msg, process_create_answers)


def process_create_correct_answer(message):
    """
    Process and store correct answers for a question in a chat session.
    
    Args:
    - message: the message object containing chat information and user input.
    
    Return:
    None
    """
    chat_id = message.chat.id
    correct_answers = message.text.split(',')
    user_tests[chat_id]['questions'][-1]['correct_answers'] = correct_answers
    msg = bot.send_message(chat_id, "Добавить еще один вопрос? (да/нет)")
    bot.register_next_step_handler(msg, process_add_more_questions)


def process_add_more_questions(message):
    """
    Processes adding more questions to a test based on user input.
    
    Args:
    - message: Represents the message object containing user input.
    
    Return:
    - None
    """
    chat_id = message.chat.id
    if message.text.lower() == 'да':
        msg = bot.send_message(chat_id, "Введите вопрос:")
        bot.register_next_step_handler(msg, process_create_question)
    else:
        test = user_tests.pop(chat_id)
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tests (topic_id, difficulty) VALUES (?, ?)", (test['topic'], test['difficulty']))
        test_id = cursor.lastrowid

        for question in test['questions']:
            cursor.execute("INSERT INTO questions (test_id, question) VALUES (?, ?)", (test_id, question['question']))
            question_id = cursor.lastrowid
            for answer in question['answers']:
                is_correct = 1 if answer in question['correct_answers'] else 0
                cursor.execute("INSERT INTO answers (question_id, answer, is_correct) VALUES (?, ?, ?)",
                               (question_id, answer, is_correct))

        conn.commit()
        conn.close()

        bot.send_message(chat_id, "Тест успешно создан!")


@bot.message_handler(func=lambda message: message.text == 'Пройти тест')
def starttest(message):
    '''
    Handles starting a test based on the user's message. If the user is authorized, prompts the user to enter the test ID; otherwise, prompts the user to authenticate or register.
    
    Args:
        message: The message object containing information about the chat.
    
    Returns:
        None
    '''
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (chat_id,))
    user = cursor.fetchone()
    if user:
        msg = bot.send_message(chat_id, "Введите ID теста, который хотите пройти:")
        bot.register_next_step_handler(msg, process_test_id)
    else:
        bot.send_message(chat_id,
                         "Пожалуйста, авторизуйтесь с помощью кнопки 'Авторизация' или зарегистрируйтесь с помощью кнопки 'Регистрация'.")


def process_test_id(message):
    """
    Summary:
        Process the test ID received in the message and handle based on the availability of the test.
    
    Description:
        - message: The message object containing information about the chat and text input.
        
    Args:
        message (object): The message object containing information about the chat and text input.
        
    Return:
        None
    """
    chat_id = message.chat.id
    test_id = int(message.text)
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tests WHERE id = ?", (test_id,))
    test = cursor.fetchone()
    if test:
        msg = bot.send_message(chat_id, "Выберите уровень сложности (легкий, средний, сложный):")
        bot.register_next_step_handler(msg, process_test_difficulty, test_id)
    else:
        bot.send_message(chat_id, "Тест с таким ID не найден. Попробуйте снова.")
        msg = bot.send_message(chat_id, "Введите ID теста, который хотите пройти:")
        bot.register_next_step_handler(msg, process_test_id)


def process_test_difficulty(message, test_id):
    """
    Processes the test difficulty based on the provided message and test ID.
    
    Parameters:
    - message: The message object containing information about the user input.
    - test_id: The ID of the test for which the difficulty needs to be processed.
    
    Args:
    - chat_id: The ID of the chat to send messages.
    - difficulty: The difficulty level of the test obtained from the user input.
    - conn: The database connection object.
    - cursor: The database cursor object.
    - test: The retrieved test information based on the test ID and difficulty level.
    
    Return:
    This method does not return any value.
    """
    chat_id = message.chat.id
    difficulty = message.text.lower()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tests WHERE id = ? AND difficulty = ?", (test_id, difficulty))
    test = cursor.fetchone()
    if test:
        send_question(chat_id, test_id, 0)
    else:
        bot.send_message(chat_id, "Тест с таким уровнем сложности не найден. Попробуйте снова.")
        msg = bot.send_message(chat_id, "Выберите уровень сложности (легкий, средний, сложный):")
        bot.register_next_step_handler(msg, process_test_difficulty, test_id)


def send_question(chat_id, test_id, question_index):
    """
    Sends a question to a chat, including its answers for selection.
    
    Parameters:
    - chat_id: The ID of the chat to send the question.
    - test_id: The ID of the test from which the question is selected.
    - question_index: The index of the question within the test.
    
    Args:
    - chat_id (int): The ID of the chat to send the question.
    - test_id (int): The ID of the test from which the question is selected.
    - question_index (int): The index of the question within the test.
    
    Returns:
    This method does not return any value.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions WHERE test_id = ? LIMIT 1 OFFSET ?", (test_id, question_index))
    question = cursor.fetchone()
    if question:
        cursor.execute("SELECT * FROM answers WHERE question_id = ?", (question[0],))
        answers = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=2)
        for answer in answers:
            markup.add(types.InlineKeyboardButton(answer[2], callback_data=f"{question[0]}_{answer[0]}"))
        markup.add(types.InlineKeyboardButton("Нет правильного ответа", callback_data=f"{question[0]}_None"))

        bot.send_message(chat_id, f"Вопрос: {question[2]}", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, process_test_answer, test_id, question_index)
    else:
        bot.send_message(chat_id, "Все вопросы теста завершены.")
        conn.close()


def process_test_answer(message, test_id, question_index):
    """
    Processes the user's submitted answers for a test question, validates them against the correct answers stored in the database, updates the user's score, and sends appropriate feedback messages based on the correctness of the answers.
    
    Args:
        message: The message object containing the user's input.
        test_id: The identifier of the ongoing test.
        question_index: The index of the current question being answered.
    
    Return:
        None
    """
    chat_id = message.chat.id
    selected_answers = message.data.split('_')
    question_id = int(selected_answers[0])
    answer_ids = selected_answers[1:]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM answers WHERE question_id = ? AND is_correct = 1", (question_id,))
    correct_answers = cursor.fetchall()
    correct_answer_ids = [answer[0] for answer in correct_answers]

    if all(answer_id in correct_answer_ids for answer_id in answer_ids):
        bot.send_message(chat_id, "Правильно!")
        cursor.execute("UPDATE users SET score = score + 1 WHERE id = ?", (chat_id,))
    else:
        correct_answers_text = ', '.join(
            [cursor.execute("SELECT answer FROM answers WHERE id = ?", (answer_id,)).fetchone()[0] for answer_id in
             correct_answer_ids])
        bot.send_message(chat_id, f"Неправильно! Правильные ответы: {correct_answers_text}")

    cursor.execute("INSERT INTO test_results (test_id, user_id, score) VALUES (?, ?, ?)",
                   (test_id, chat_id, 1 if all(answer_id in correct_answer_ids for answer_id in answer_ids) else 0))

    conn.commit()
    conn.close()

    send_question(chat_id, test_id, question_index + 1)


def calculate_mean_without_outliers(scores):
    """
    Calculate mean of scores without including outliers.
    
    Parameters:
    - scores: A list of numeric values representing individual scores.
    
    Returns:
    - float: The mean value of scores after removing outliers. If there are no scores within the range of (lower_bound, upper_bound),
      it returns 0.
      
    Args:
    - scores (list): A list of numeric values representing individual scores.
    
    Return:
    - float: The mean value of scores after removing outliers. If there are no scores within the range of (lower_bound, upper_bound),
      it returns 0.
    """
    q1 = np.percentile(scores, 25)
    q3 = np.percentile(scores, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_scores = [score for score in scores if lower_bound <= score <= upper_bound]
    if len(filtered_scores) == 0:
        return 0
    return np.mean(filtered_scores)


def calculate_median(scores):
    """
    Calculate the median value of the given scores.
    
    Args:
    - scores (list of int/float): A list of numerical values for which the median will be calculated.
    
    Returns:
    - float: The median value of the input scores.
    """
    return np.median(scores)


def calculate_creativity(question_scores):
    """
    Calculate creativity metric based on question scores.
    
    Args:
    - question_scores (list): A list of scores representing responses to creativity questions.
    
    Return:
    - float: The calculated creativity metric. This metric is derived by calculating the interquartile range divided by the median score. If the median score is 0, the result will be 0 as well.
    """
    iq_range = np.percentile(question_scores, 75) - np.percentile(question_scores, 25)
    median_score = np.median(question_scores)
    if median_score == 0:
        return 0
    return iq_range / median_score


@bot.message_handler(func=lambda message: message.text == 'Посмотреть рейтинг')
def request_topic_for_rating(message):
    """
    Requests a topic for rating based on the received message.
    
    Parameters:
    - message: The message object containing the chat information.
    
    Returns:
    None
    
    Args:
    - message (object): The message object containing chat information.
    
    Return:
    None
    """
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM topics")
    topics = cursor.fetchall()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics:
        markup.add(types.KeyboardButton(topic[0]))

    msg = bot.send_message(chat_id, "Выберите тему для просмотра рейтинга:", reply_markup=markup)
    bot.register_next_step_handler(msg, view_rating)


def view_rating(message):
    """
    Summary:
        View the rating of users based on test results for a specific topic.
    
    Parameters:
        message: Telegram message object containing information related to the chat and text message.
    
    Args:
        message (Telegram message object): Contains information related to the chat and text message.
    
    Return:
        None
    """
    chat_id = message.chat.id
    topic_name = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM topics WHERE name = ?", (topic_name,))
    topic_id = cursor.fetchone()[0]

    cursor.execute("SELECT user_id, score FROM test_results WHERE test_id IN (SELECT id FROM tests WHERE topic_id = ?)",
                   (topic_id,))
    user_scores = cursor.fetchall()

    users_scores_dict = {}
    for user_id, score in user_scores:
        if user_id not in users_scores_dict:
            users_scores_dict[user_id] = []
        users_scores_dict[user_id].append(score)

    ratings = []
    for user_id, scores in users_scores_dict.items():
        cursor.execute("SELECT first_name, last_name FROM users WHERE id = ?", (user_id,))
        first_name, last_name = cursor.fetchone()

        analytic_score = calculate_mean_without_outliers(scores)
        creativity_score = calculate_creativity(scores)

        ratings.append(f"{first_name} {last_name}: Аналитичность: {analytic_score}, Креативность: {creativity_score}")

    bot.send_message(chat_id, "Рейтинг пользователей по теме '{}':\n".format(topic_name) + "\n".join(ratings))


bot.polling()
