import telebot
from telebot import types
import sqlite3
import numpy as np
import config_eduplatform

TOKEN = config_eduplatform.bot_token
bot = telebot.TeleBot(TOKEN)


def connect_db():
    """
    Establishes a connection to the SQLite database.

        This method creates and returns a connection object to the
        'test_bot.db' SQLite database, allowing for database operations.

        Returns:
            A Connection object that can be used to interact with the database.
    """
    return sqlite3.connect("test_bot.db")


@bot.message_handler(commands=["start"])
def start_message(message):
    """
    Handles the start command from the user.

        This method is triggered when a user sends the '/start' command. It initializes the conversation by
        sending a welcome message to the user and provides buttons for registration and authorization.

        Args:
            message: The message object that contains information about the user's message, including chat ID.

        Returns:
            None: This method does not return a value; it sends a message to the user instead.
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    register_button = types.KeyboardButton("Регистрация")
    login_button = types.KeyboardButton("Авторизация")
    markup.add(register_button, login_button)
    bot.send_message(
        chat_id,
        "Добро пожаловать! Используйте кнопки ниже для навигации.",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Регистрация")
def register(message):
    """
    Registers a new user if they are not already registered.

        This method checks if a user is already registered by querying the database
        using the user's chat ID. If the user is not registered, it prompts them
        to enter their phone number, transitioning to the next step in the registration
        process.

        Parameters:
            None

        Returns:
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
    Processes the registration of a phone number.

        This method checks if the provided phone number is already registered in the database.
        If it is registered, a message is sent to the user indicating the phone number is already
        in use. If the phone number is not registered, the user is prompted to enter a password,
        which will be handled by a subsequent step.

        Args:
            phone: The phone number to register.
            chat_id: The chat ID of the user attempting to register.

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
    Processes the user's password registration step and initiates the next step
    to collect the user's first name.

    This method sends a message to the user asking for their first name after
    handling the password registration logic.

    Args:
        msg: The message object containing user input data.
        phone: The user's phone number in string format.
        password: The user's password in string format.

    Returns:
        None: This function does not return a value but initiates the next step
        in the registration process by sending a message to the user.
    """
    chat_id = message.chat.id
    password = message.text
    msg = bot.send_message(chat_id, "Введите ваше имя:")
    bot.register_next_step_handler(msg, process_register_first_name, phone, password)


def process_register_first_name(message, phone, password):
    """
    Processes the registration of the user's first name.

        This method is called to handle the user's input for their first name
        during the registration process. It registers the next step handler to
        capture the last name after the first name has been processed.

        Args:
            message: The message object containing the user's response.
            phone: The user's phone number as obtained earlier in the registration process.
            password: The password provided by the user for registration.
            first_name: The first name provided by the user during registration.

        Returns:
            None: This method does not return any value but continues the registration process.
    """
    chat_id = message.chat.id
    first_name = message.text
    msg = bot.send_message(chat_id, "Введите вашу фамилию:")
    bot.register_next_step_handler(
        msg, process_register_last_name, phone, password, first_name
    )


def process_register_last_name(message, phone, password, first_name):
    """
    Processes the registration of a user by storing their information and sending a confirmation message.

        This method inserts the user's details into the database and sends a confirmation message along with a
        keyboard for further actions after successful registration.

        Args:
            chat_id: The unique identifier for the chat where the user is interacting.
            phone: The phone number provided by the user for registration.
            password: The password chosen by the user for their account.
            first_name: The first name of the user.
            last_name: The last name of the user.

        Returns:
            None: The method does not return a value. It commits the registration to the database and sends a
            confirmation message to the user.
    """
    chat_id = message.chat.id
    last_name = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (id, phone, password, first_name, last_name, score) VALUES (?, ?, ?, ?, ?, ?)",
        (chat_id, phone, password, first_name, last_name, 0),
    )
    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    createtest_button = types.KeyboardButton("Создать тест")
    starttest_button = types.KeyboardButton("Пройти тест")
    viewrating_button = types.KeyboardButton("Посмотреть рейтинг")
    markup.add(createtest_button, starttest_button, viewrating_button)
    bot.send_message(
        chat_id, f"Регистрация завершена! Ваш логин: {phone}", reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Авторизация")
def login(message):
    """
    Handles user login based on a specific message trigger.

        This method is triggered by a message handler when a user sends a message with the text 'Авторизация'.
        It interacts with a database to verify user credentials and sends an appropriate response to the user.

        Parameters:
            None

        Returns:
            None
    """
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите номер телефона:")
    bot.register_next_step_handler(msg, process_login_phone)


def process_login_phone(message):
    """
    Processes the user's login attempt using their phone number.

        This method handles the user's login by verifying their phone number.
        If the provided phone number exists in the database, it prompts the user to
        enter their password. If the phone number is not found, it notifies the user
        and prompts for re-entry or registration.

        Args:
            message: The message object containing the user's chat information and phone number input.

        Returns:
            None: This method does not return any value.
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
        bot.send_message(
            chat_id,
            "Пользователь с таким номером телефона не найден. Пожалуйста, зарегистрируйтесь или введите номер телефона повторно.",
        )
        login(message)


def process_login_password(message, phone):
    """
    Processes the login and password input from the user.

        This method checks the provided password against the stored credentials for a user.
        If the password matches, it confirms successful authorization and provides the user
        with options for creating a test, taking a test, or viewing ratings. If the password
        is incorrect, it prompts the user to try again.

        Args:
            message: The message object containing the user's input and chat information.

        Returns:
            None: This method sends messages directly to the user and does not return a value.
    """
    chat_id = message.chat.id
    password = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE phone = ? AND password = ?", (phone, password)
    )
    user = cursor.fetchone()
    if user:
        # Пользователь успешно авторизован
        user_id = user[0]
        cursor.execute("UPDATE users SET id = ? WHERE phone = ?", (chat_id, phone))
        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        createtest_button = types.KeyboardButton("Создать тест")
        starttest_button = types.KeyboardButton("Пройти тест")
        viewrating_button = types.KeyboardButton("Посмотреть рейтинг")
        markup.add(createtest_button, starttest_button, viewrating_button)
        bot.send_message(
            chat_id, f"Авторизация успешна! Ваш логин: {phone}", reply_markup=markup
        )
    else:
        bot.send_message(chat_id, "Неправильный пароль, попробуйте снова.")
        login(message)


@bot.message_handler(func=lambda message: message.text == "Создать тест")
def createtest(message):
    """
    Starts the process of creating a test for the user.

        This method initiates a test creation process by prompting the user to specify a topic for the test. It stores the user's input
        and instructs them to choose a difficulty level before proceeding to the next step in the test creation workflow.

        Args:
            message: The message object containing information about the user's request, including the chat ID and the text of the message.

        Returns:
            None: This method does not return a value. Instead, it sends messages to the user and registers the next steps in the test creation process.
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
        bot.send_message(
            chat_id,
            "Пожалуйста, авторизуйтесь с помощью кнопки 'Авторизация' или зарегистрируйтесь с помощью кнопки 'Регистрация'.",
        )


def process_create_topic(message):
    """
    Processes the creation of a new topic based on a user message.

        This method handles user input for creating a new topic. If the input is
        invalid, it sends an error message and prompts the user to try again.

        Args:
            message: The message object containing user input, including the chat ID
                     and the text of the message.

        Returns:
            None: This method does not return a value.
    """
    chat_id = message.chat.id
    topic = message.text
    user_tests[chat_id] = {"topic": topic, "questions": []}
    msg = bot.send_message(
        chat_id, "Выберите уровень сложности (легкий, средний, сложный):"
    )
    bot.register_next_step_handler(msg, process_create_difficulty)


def process_create_difficulty(message):
    """
    Starts a process to create a difficulty level for a bot interaction.

        This method prompts the user to input a difficulty level by sending a message
        with options to add an answer or finish the process.

        Args:
            message: The message object containing information about the incoming message
                     from the user, including the chat ID and text.

        Returns:
            None: This method does not return any value. Instead, it sends messages
            directly to the user through the bot interface.
    """
    chat_id = message.chat.id
    difficulty = message.text.lower()
    if difficulty in ["легкий", "средний", "сложный"]:
        user_tests[chat_id]["difficulty"] = difficulty
        msg = bot.send_message(chat_id, "Введите вопрос:")
        bot.register_next_step_handler(msg, process_create_question)
    else:
        bot.send_message(chat_id, "Некорректный уровень сложности. Попробуйте снова.")
        process_create_topic(message)


def process_create_question(message):
    """
    Processes the creation of a new question for user tests.

        This function handles user input when creating a new question, allowing them to specify answer options
        and the correct answer. It prompts the user for various inputs and registers the next step handler to
        continue the process.

        Args:
            message: The incoming message from the user that contains the question and answers.

        Returns:
            None: The function does not return any value; it communicates with the user through
            bot messages and updates the user_tests dictionary.
    """
    chat_id = message.chat.id
    question = message.text
    user_tests[chat_id]["questions"].append(
        {"question": question, "answers": [], "correct_answers": []}
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_answer_button = types.KeyboardButton("Добавить ответ")
    done_button = types.KeyboardButton("Готово")
    markup.add(add_answer_button, done_button)
    bot.send_message(
        chat_id,
        "Введите вариант ответа или нажмите 'Готово' для завершения:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, process_create_answers)


def process_create_answers(message):
    """
    Handles the processing of user responses for creating answers.

        This method manages the user's input when creating answers for a
        specific question in a test. It determines whether the user wants
        to add more questions or finalize the test. Based on the user's input,
        it will either prompt for additional questions or save the test details
        to the database.

        Args:
            message: The incoming message containing the user's response
                     regarding test creation.

        Returns:
            None: This method does not return a value, but it performs database
            operations based on the user's input.
    """
    chat_id = message.chat.id
    if message.text == "Готово":
        msg = bot.send_message(
            chat_id, "Введите правильный ответ (если несколько, через запятую):"
        )
        bot.register_next_step_handler(msg, process_create_correct_answer)
    else:
        answer = message.text
        user_tests[chat_id]["questions"][-1]["answers"].append(answer)
        msg = bot.send_message(
            chat_id, "Введите вариант ответа или нажмите 'Готово' для завершения:"
        )
        bot.register_next_step_handler(msg, process_create_answers)


def process_create_correct_answer(message):
    """
    Processes and inserts a new question with its answers into the database.

        This method takes a test identifier and a question dictionary, extracts
        the relevant information, and inserts the question and its possible answers
        into the database. The method also marks the correct answers accordingly.

        Args:
            test_id: The identifier of the test to which the question belongs.
            question: A dictionary containing the 'question' text and a list of 'answers',
                      as well as a list of 'correct_answers' for marking correctness.

        Returns:
            The ID of the last inserted question in the database.
    """
    chat_id = message.chat.id
    correct_answers = message.text.split(",")
    user_tests[chat_id]["questions"][-1]["correct_answers"] = correct_answers
    msg = bot.send_message(chat_id, "Добавить еще один вопрос? (да/нет)")
    bot.register_next_step_handler(msg, process_add_more_questions)


def process_add_more_questions(message):
    """
    Process additional questions for a test and update the database.

        This method handles the addition of more questions to a specified test and commits the changes to the database.
        It also sends a confirmation message to the user indicating that the test has been successfully created.

        Parameters:
            None

        Returns:
            None
    """
    chat_id = message.chat.id
    if message.text.lower() == "да":
        msg = bot.send_message(chat_id, "Введите вопрос:")
        bot.register_next_step_handler(msg, process_create_question)
    else:
        test = user_tests.pop(chat_id)
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tests (topic_id, difficulty) VALUES (?, ?)",
            (test["topic"], test["difficulty"]),
        )
        test_id = cursor.lastrowid

        for question in test["questions"]:
            cursor.execute(
                "INSERT INTO questions (test_id, question) VALUES (?, ?)",
                (test_id, question["question"]),
            )
            question_id = cursor.lastrowid
            for answer in question["answers"]:
                is_correct = 1 if answer in question["correct_answers"] else 0
                cursor.execute(
                    "INSERT INTO answers (question_id, answer, is_correct) VALUES (?, ?, ?)",
                    (question_id, answer, is_correct),
                )

        conn.commit()
        conn.close()

        bot.send_message(chat_id, "Тест успешно создан!")


@bot.message_handler(func=lambda message: message.text == "Пройти тест")
def starttest(message):
    """
    Starts the test process for the user.

        This method initiates a conversation with the user by prompting them to enter the ID of the test they would like to take.
        It is triggered when the user sends a message that matches 'Пройти тест'. The user will receive a message asking for the test ID,
        and the next step in the conversation will be handled by the `process_test_id` function.

        Parameters:
            None

        Returns:
            None
    """
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (chat_id,))
    user = cursor.fetchone()
    if user:
        msg = bot.send_message(chat_id, "Введите ID теста, который хотите пройти:")
        bot.register_next_step_handler(msg, process_test_id)
    else:
        bot.send_message(
            chat_id,
            "Пожалуйста, авторизуйтесь с помощью кнопки 'Авторизация' или зарегистрируйтесь с помощью кнопки 'Регистрация'.",
        )


def process_test_id(message):
    """
    Processes the test ID by prompting the user to select a difficulty level.

        This method sends a message to the user asking them to choose a difficulty level
        for the test associated with the specified test ID. It then waits for the user to
        respond with their choice, which will be handled by a subsequent method.

        Args:
            chat_id: The unique identifier for the chat where the message will be sent.
            test_id: The unique identifier for the test that the user is being prompted about.

        Returns:
            None: This method does not return a value.
    """
    chat_id = message.chat.id
    test_id = int(message.text)
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tests WHERE id = ?", (test_id,))
    test = cursor.fetchone()
    if test:
        msg = bot.send_message(
            chat_id, "Выберите уровень сложности (легкий, средний, сложный):"
        )
        bot.register_next_step_handler(msg, process_test_difficulty, test_id)
    else:
        bot.send_message(chat_id, "Тест с таким ID не найден. Попробуйте снова.")
        msg = bot.send_message(chat_id, "Введите ID теста, который хотите пройти:")
        bot.register_next_step_handler(msg, process_test_id)


def process_test_difficulty(message, test_id):
    """
    Processes the difficulty level of a test by sending a question to the user.

        This method handles the display of a question to the user in a chat,
        and prepares for the next step where the user will provide their answer.
        If there are no remaining questions in the test, a message indicating the
        completion of the test is sent.

        Args:
            question: The current question to be sent to the user.
            chat_id: The unique identifier for the chat where the question is being sent.

        Returns:
            None: This method does not return any value.
    """
    chat_id = message.chat.id
    difficulty = message.text.lower()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tests WHERE id = ? AND difficulty = ?", (test_id, difficulty)
    )
    test = cursor.fetchone()
    if test:
        send_question(chat_id, test_id, 0)
    else:
        bot.send_message(
            chat_id, "Тест с таким уровнем сложности не найден. Попробуйте снова."
        )
        msg = bot.send_message(
            chat_id, "Выберите уровень сложности (легкий, средний, сложный):"
        )
        bot.register_next_step_handler(msg, process_test_difficulty, test_id)


def send_question(chat_id, test_id, question_index):
    """
    Send a question to the user and handle their answer.

        This method retrieves a question from the database based on the given test ID and question index.
        It checks the user's answers against the correct answers, sends feedback on whether the answers are correct,
        and updates the user's score accordingly.

        Args:
            chat_id: The ID of the user to whom the question is being sent.
            test_id: The ID of the test associated with the questions.
            question_index: The index of the specific question to be sent.

        Returns:
            None
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM questions WHERE test_id = ? LIMIT 1 OFFSET ?",
        (test_id, question_index),
    )
    question = cursor.fetchone()
    if question:
        cursor.execute("SELECT * FROM answers WHERE question_id = ?", (question[0],))
        answers = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=2)
        for answer in answers:
            markup.add(
                types.InlineKeyboardButton(
                    answer[2], callback_data=f"{question[0]}_{answer[0]}"
                )
            )
        markup.add(
            types.InlineKeyboardButton(
                "Нет правильного ответа", callback_data=f"{question[0]}_None"
            )
        )

        bot.send_message(chat_id, f"Вопрос: {question[2]}", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(
            chat_id, process_test_answer, test_id, question_index
        )
    else:
        bot.send_message(chat_id, "Все вопросы теста завершены.")
        conn.close()


def process_test_answer(message, test_id, question_index):
    """
    Processes a list of test scores to filter out outliers and calculate the mean.

        This method takes a list of numeric scores, identifies outliers using the interquartile range (IQR) method,
        filters these outliers, and computes the mean of the remaining scores. If all scores are considered outliers,
        it returns 0.

        Args:
            scores: A list of numeric scores representing the results of a test.

        Returns:
            The mean of the filtered scores, or 0 if no scores remain after filtering out outliers.
    """
    chat_id = message.chat.id
    selected_answers = message.data.split("_")
    question_id = int(selected_answers[0])
    answer_ids = selected_answers[1:]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM answers WHERE question_id = ? AND is_correct = 1",
        (question_id,),
    )
    correct_answers = cursor.fetchall()
    correct_answer_ids = [answer[0] for answer in correct_answers]

    if all(answer_id in correct_answer_ids for answer_id in answer_ids):
        bot.send_message(chat_id, "Правильно!")
        cursor.execute("UPDATE users SET score = score + 1 WHERE id = ?", (chat_id,))
    else:
        correct_answers_text = ", ".join(
            [
                cursor.execute(
                    "SELECT answer FROM answers WHERE id = ?", (answer_id,)
                ).fetchone()[0]
                for answer_id in correct_answer_ids
            ]
        )
        bot.send_message(
            chat_id, f"Неправильно! Правильные ответы: {correct_answers_text}"
        )

    cursor.execute(
        "INSERT INTO test_results (test_id, user_id, score) VALUES (?, ?, ?)",
        (
            test_id,
            chat_id,
            (
                1
                if all(answer_id in correct_answer_ids for answer_id in answer_ids)
                else 0
            ),
        ),
    )

    conn.commit()
    conn.close()

    send_question(chat_id, test_id, question_index + 1)


def calculate_mean_without_outliers(scores):
    """
    Calculates the mean score of users for a specific test topic, excluding any outlier scores.

    This method retrieves user scores from a database based on the given topic name,
    filters out outlier scores, and computes the mean of the remaining scores.

    Parameters:
        topic_name: The name of the topic for which the mean score is to be calculated.

    Returns:
        A float representing the mean score of users, excluding any outlier scores.
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
    Calculate the median score for a given user.

        This method retrieves the list of scores for the specified user and
        calculates the median value from that list. If the user has no scores,
        the method returns None.

        Args:
            user_id: The unique identifier of the user whose median score
                      is to be calculated.

        Returns:
            The median score of the user if scores are available, otherwise None.
    """
    return np.median(scores)


def calculate_creativity(question_scores):
    """
    Calculate and update the creativity score for a user.

        This method appends a new creativity score for the specified user,
        retrieves the user's name from the database, and prepares the data for further processing.

        Args:
            user_id: The unique identifier of the user whose creativity score is to be updated.
            score: The creativity score to be appended to the user's existing scores.

        Returns:
            A list containing the user's first and last names retrieved from the database.
    """
    iq_range = np.percentile(question_scores, 75) - np.percentile(question_scores, 25)
    median_score = np.median(question_scores)
    if median_score == 0:
        return 0
    return iq_range / median_score


@bot.message_handler(func=lambda message: message.text == "Посмотреть рейтинг")
def request_topic_for_rating(message):
    """
    Handles the request for viewing ratings of a specific topic.

        This method is triggered when a user sends a message that matches the predefined text
        'Посмотреть рейтинг'. It compiles user ratings based on their analytic and creativity scores
        associated with a given topic and sends the ratings back to the user.

        Parameters:
            None

        Returns:
            None: This method does not return any value. It sends a message to the user containing
            the ratings.
    """
    chat_id = message.chat.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM topics")
    topics = cursor.fetchall()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics:
        markup.add(types.KeyboardButton(topic[0]))

    msg = bot.send_message(
        chat_id, "Выберите тему для просмотра рейтинга:", reply_markup=markup
    )
    bot.register_next_step_handler(msg, view_rating)


def view_rating(message):
    """
    Retrieves and displays the current rating.

        This method fetches the current rating and presents it to the user.
        It is designed to provide quick access to the rating information.

        Parameters:
            None

        Returns:
            A string containing the current rating information.
    """
    chat_id = message.chat.id
    topic_name = message.text
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM topics WHERE name = ?", (topic_name,))
    topic_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT user_id, score FROM test_results WHERE test_id IN (SELECT id FROM tests WHERE topic_id = ?)",
        (topic_id,),
    )
    user_scores = cursor.fetchall()

    users_scores_dict = {}
    for user_id, score in user_scores:
        if user_id not in users_scores_dict:
            users_scores_dict[user_id] = []
        users_scores_dict[user_id].append(score)

    ratings = []
    for user_id, scores in users_scores_dict.items():
        cursor.execute(
            "SELECT first_name, last_name FROM users WHERE id = ?", (user_id,)
        )
        first_name, last_name = cursor.fetchone()

        analytic_score = calculate_mean_without_outliers(scores)
        creativity_score = calculate_creativity(scores)

        ratings.append(
            f"{first_name} {last_name}: Аналитичность: {analytic_score}, Креативность: {creativity_score}"
        )

    bot.send_message(
        chat_id,
        "Рейтинг пользователей по теме '{}':\n".format(topic_name) + "\n".join(ratings),
    )


bot.polling()
