This is an educational project

---
# Word counter
Утилита командной строки, позволяющая собbрать статистику по частоте использования слов в программах на языке Python.

## Описание
Утилита анализирует тексты программ в указанных директориях, выделяет слова английского языка в именах идентификаторов и для каждого слова подсчитывает, сколько раз это слово употреблялось. Через параметры командной строки можно указать слова каких частей речи будут анализироваться и из каких типов идентификаторов Python слова будут извлекаться.

По окончании работы создается отчет, который либо экспортируется в указанный файл, либо выводится на консоль. Для отчета vожно указать максимальное количество выводимых слов.

Отдельным аргументом командной строки можно указать, следует ли анализировать идентификаторы с магическими именами (типа `__get__, __name__` и т.д.)

Модульная структура программы позволяет легко ее модифицировать как для работы с другими языками програмирования, так и для других видов лексического анализа.

## Использование
```
words_count.py [-h] [-d DIR] [-p PROJECTS [PROJECTS ...]]
                      [-l PROJECTS_LIST] [-s {verb,noun} [{verb,noun} ...]]
                      [-i {func,local_var} [{func,local_var} ...]]
                      [-m MAX_WORDS] [-r REPORT] [--no_magic]
```
Аргументы командной строки:
```
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     path to directory with projects
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
                        projects list to check
  -l PROJECTS_LIST, --projects_list PROJECTS_LIST
                        file with projects list to check
  -s {verb,noun} [{verb,noun} ...], --part_of_speech {verb,noun} [{verb,noun} ...]
                        part of speech to extract
  -i {func,local_var} [{func,local_var} ...], --identifier {func,local_var} [{func,local_var} ...]
                        identifiers to extract
  -m MAX_WORDS, --max_words MAX_WORDS
                        number of words to print
  -r REPORT, --report REPORT
                        report file
  --no_magic            don't count words in magic names
```

## Требования
Python 3.6 или выше
Пакеты Python согласно `requirements.txt`

## Тесты
Для программы разработано тестовое окружение (директория `./tests`)
