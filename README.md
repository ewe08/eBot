# eBot
### Инструкция по запуску:


1. Убедитесь, что на компьютере установлен git и python(https://git-scm.com, https://www.python.org)
2. Заходим в коммандную строку (терминал)
3. Пишем: </br> ```git clone https://github.com/ewe08/eBot.git``` </br>
(Может не работать из-за двухфакторной аутентификации) 
4. ```python -m venv venv```
5. ```venv\Scripts\activate``` (для линукс ```venv\bin\activate```)
6. ```pip install -r requirements.txt```
7. Создаём файл .env и вписываем туда полученные данные:
    ```
   TOKEN=<...>
   ADMIN_ID=<...>
   ADMIN_CHAT_ID=<...>
   WORK_CHAT_ID=<...>
   USER=<...>
   PASSWORD=<...>
   DATABASE=<...>
   HOST=<...>
   PORT=<...>
   TIMEOUT=<...>
   ```
8. Запускаем main.py

На линукс меняем python -> python3, pip -> pip3