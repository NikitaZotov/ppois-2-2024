# Лабораторная работа №4

<span style="font-size: 25px;">__Цель:__</span><br>
• Изучить архитектурные приемы построения пользовательского интерфейса и принципы создания веб-приложений


<span style="font-size: 25px;">__Вариант 1. Структура киностудии</span><br>

<hr>

В моей программе реализованы функции:
- Создание, удаление, редактирование актеров;
- Создание, удаление, редактирование сценариев;
- Создание, удаление, редактирование режиссеров;
- Создание, удаление, редактирование Площадок;
- Создание, удаление, редактирование Студий;

Отображение страниц для создания сайта реализовано в html шаблонах и формах, которые упрощают реализацию представления визуального интерфейса страницы.

<div style="text-align: center;">
    <img src="https://sun9-5.userapi.com/impg/2WtM7LkNH_uZZ9FvyWJEcv8GHa648dDOHpHSkQ/EzySVaMRi1g.jpg?size=172x258&quality=96&sign=df2c4ce5a304552d8f20591f79a623d5&type=album" style="height: 300px;">
</div>

Пример кода platform_form.html:

<div style="text-align: center;">
    <img src="https://sun9-6.userapi.com/impg/pGd3FWv-LND7he2b4s1PT71rXi-tTaQQ51baHA/J-Dm3uopKxY.jpg?size=1003x654&quality=96&sign=8a4b82786b26629f3f5bf344121235b6&type=album" style="height: 300px;">
</div>

<hr>

В лабораторной работе подключена база данных movies.bd, которая включает как __данные__ так и __отношения между данными__.

Обработка данных из базы данных происходит с использованием моделей:

<div style="text-align: center;">
    <img src="https://sun9-67.userapi.com/impg/GRB2O75QxHJ0SYHlHtPy9WKiZuepF_iKS9ztGQ/9iv-_AhaWpo.jpg?size=788x578&quality=96&sign=475bcce2b5671a5f015251d2e815accb&type=album" style="height: 300px;">
</div>

```
Данное приложение разработано и использованием Flask и имеет HTTP протоколы/

Также в лабораторной использован бутстрап 5, который упрощает создание визуального интерфейса.
```

<hr>

Переход на различные страницы сайта и логика этих страниц пррописана в роутах app.py, который является контроллером.

_Пример кода в app.py:_ 

<div style="text-align: center;">
    <img src="https://sun9-77.userapi.com/impg/KMaChX1jjEliJjmuOJO8OzSsi9HzQQXzMxUelg/tqHsLVfFaSw.jpg?size=693x609&quality=96&sign=b1961c69e1fbe3dd13b6c63231bb9e18&type=album" style="height: 300px;">
</div>

<hr>

__Агент__

Создание агента подразумевает указание его имени.

Он имеет функции:

- Редактирование - изменение его имени.
- Удаление - удаление актера из базы данных.

<div style="text-align: center;">
    <img src="https://sun9-4.userapi.com/impg/SDuvs7Y40pkJ07lRjhob_io9tnXgMY7DgGkh-w/TsrBxdvYJN8.jpg?size=1859x918&quality=96&sign=580a8a0eafe8d686614b460a1e615987&type=album" style="height: 300px;">
</div>

<hr>

__Режиссер__

Создание режиссера подразумевает указание его имени.

Он имеет функции:

- Редактирование - изменение его имени.
- Удаление - удаление актера из базы данных.

<div style="text-align: center;">
    <img src="https://sun9-59.userapi.com/impg/tXLtSlgrvFnBbD5bIM1kWupnYT2gW_WspjUEug/5BoKVoQBBiM.jpg?size=1857x924&quality=96&sign=090bf9a1919828a5377876c76579a5f5&type=album" style="height: 300px;">
</div>

<hr>

__Сценарий__

Создание сценария подразумевает указание его имени, а также указание описания данного сценария.

Он имеет функции:

- Редактирование:
    - Изменение названия сценария;
    - Изменение описания сценария;
- Удаление сценария

<div style="text-align: center;">
    <img src="https://sun9-77.userapi.com/impg/toB96YHsubNFQzVyPTXMix6eYaLqm0sx-l03Fw/lXKIN0gujvg.jpg?size=1857x923&quality=96&sign=56fa47599890e583a169436cc696445c&type=album" style="height: 300px;">
</div>

<hr>

__Платформа__

Создание платформы подразумевает указание его типа.

Для создания платформы нужно:

- Указать хотя бы один сценарий.
- Указать хотя бы одного актера.
- Указать хотя бы одного режиссера.

Изменение площадки подразумевает изменение его типа.
Удаление площадки удаляет ее из базы данных.

<div style="text-align: center;">
    <img src="https://sun9-37.userapi.com/impg/CRND5NUI50gHHgc57OvzJ7YKeYCnzUowbqLx9A/wTUH6_ZHHuo.jpg?size=1858x920&quality=96&sign=bfde429d906df45e07640ea0d4f368cc&type=album" style="height: 300px;">
</div>

<hr>

__Студия__

Создание студии подразумевает указание его имени.

Создание студии возможно только при указании хотя бы одной площадки.

Функции:

- Редактирвоание - изменение названия студии.
- Удаление - удаление студии из базы данных.

<div style="text-align: center;">
    <img src="https://sun9-54.userapi.com/impg/WFdU1R4qbTUXWTSyZooHFyhq3z6DF_bzadiW6A/n98qFtsYZes.jpg?size=1857x916&quality=96&sign=125e9ba9e988810a238529fdfef06ca1&type=album" style="height: 300px;">
</div>

<hr>

- Редактирование каких-то элементов отображает их изенения во всех элементах, к которым они подключены.

- Удаление элементов возможно. Если они были удалены, то в тех элементах, с которыми они связаны, они просто удаляются.
