## ConfigParser

Разработан инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке json попадает в стандартный вывод.

**Функционал:**
Поддержка однострочных (REM) и многострочных (<{-...-}) комментариев.
Парсинг переменных вида def имя := значение;.
Имена: [_A-Z][_a-zA-Z0-9]*
Вычисление константы на этапе трансляции: [имя].
Поддержка словарей, определённых между table.
Результатом вычисления константного выражения является значение.

**Запуск:**
python main.py config.txt

**Пример работы:**

![Скриншот 1](https://github.com/kkikill/configdz3/blob/main/PNG1.png)
![Скриншот 2](https://github.com/kkikill/configdz3/blob/main/PNG2.png)
