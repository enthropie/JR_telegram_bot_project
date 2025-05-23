
*Проект "Telegram/ChatGPT"*

Код Telegram-бота с подключением ChatGPT.

Функционал:

### 1. *"Рандомный факт"*
Телеграм-бот должен обрабатывать команду /random.
При обработке команды он отсылает заранее заготовленное изображение и делает запрос к ChatGPT с заранее заготовленным промптом.
Ответ ChatGPT нужно получить и передать пользователю. К сообщению должна быть прикреплена кнопка "Закончить", нажатие на которую работает так же, как команда /start.
И кнопка "Хочу ещё факт", нажатие на которую работает так же, как команда /random

![image](https://github.com/user-attachments/assets/a278290e-d29e-48af-83d8-915b6a807ef9)

### 2. *"ChatGPT интерфейс"*
Телеграм-бот должен обрабатывать команду /gpt. При обработке команды он отсылает заранее заготовленное изображение
и делает запрос к ChatGPT, передавая  текст полученного сообщения. Ответ ChatGPT нужно получить и передать пользователю текстовым сообщением

![image](https://github.com/user-attachments/assets/a6c4fa79-4ff5-4f22-bdd4-7734f4e31355)

### 3. *"Диалог с известной личностью"*
Телеграм-бот должен обрабатывать команду /talk.
При обработке команды бот отсылает заранее заготовленное изображение и предлагает выбор из нескольких известных личностей,
используя кнопки. По нажатию кнопки нужно установить промпт выбранной личности. Дальнейшие текстовые сообщения от пользователя нужно передавать ChatGPT и
возвращать его ответы пользователю. К ним должна быть прикреплена кнопка "Закончить", нажатие на которую работает так же, как команда /start

![image](https://github.com/user-attachments/assets/ab0ac088-c0bb-4ce9-8580-4f9d276f89c0)

### 4. *"Квиз"*
Телеграм-бот должен обрабатывать команду /quiz.
При обработке команды бот отсылает заранее заготовленное изображение и предлагает выбор из нескольких тем, используя кнопки.
После выбора темы, передать запрос ChatGPT и, получив вопрос квиза, передать его пользователю. Следующее текстовое сообщение пользователя считается ответом.
Его нужно передать ChatGPT и получить результат. Результат передать пользователю с возможностью задать ещё вопрос на ту же тему, сменить тему или закончить квиз, с помощью кнопок.
Бот также должен вести счёт правильных ответов и отображать вместе с очередным результатом

![image](https://github.com/user-attachments/assets/82a3b0fa-fb97-4879-8e1b-20510000cc72)

### 5. **Тема на выбор** **"Переводчик"**
Бот предлагает выбрать язык на который нужно перевести текст, используя кнопки.
После выбора языка пользователь отправляет текст, который нужно перевести. Бот использует ChatGPT для перевода текста и отправляет результат пользователю.
К сообщению должна быть прикреплена кнопка смены языка и кнопка "Закончить", нажатие на которую работает так же, как команда /start.

![image](https://github.com/user-attachments/assets/5966dfe8-460d-46f8-bcf3-ac709a990953)

### 6. **Тема на выбор** **"Распознавание изображений"**
Бот должен принимать от пользователя изображение и передавать его ChatGPT.
ChatGPT должен определить, что находится на изображении и описывать в текстовом виде.
Ответ передается пользователю в текстовом сообщении.

![image](https://github.com/user-attachments/assets/050fa15d-2af0-4113-a6c2-9e49c4278b08)


