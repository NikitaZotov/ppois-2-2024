# Лабораторная работа №4

<span style="font-size: 25px;">__Цель:__</span><br>
• Изучить архитектурные приемы построения пользовательского интерфейса и принципы создания веб-приложений


<span style="font-size: 25px;">__Вариант 1. Структура киностудии</span><br>

<hr>

В моей программе реализованы функции:
- Взаимодействие со студией;
- Взаимодействие с площадкой;
- Взаимодействие со сценарием;
- Взаимодействие с режиссером;
- Взаимодействие с актерами;
- Взаимодействие с камерой;
- Отображение информации о киностудии;

Отображение страниц для создания сайта реализовано в html шаблонах:

<div style="text-align: center;">
    <img src="https://sun9-11.userapi.com/impg/nHdPzRU3Iqlpy5oL_e4vgqN7OttJ9YQkPqdMVQ/kH7fAMef2bg.jpg?size=190x288&quality=96&sign=a20e117b027532c34e147599b676d298&type=album" style="height: 300px;">
</div>

<hr>

В лабораторной работе используется старый код, который включает в себя __модели 1-й лабораторной работы__ и __функции логики 1-й лабораторной работы__

В лабораторной работе подключена база данных movies.bd, которая включает как __данные__ так и __отношения между данными__.

Пример модели камеры, использованной из 1-й лабораторной работы:

<div style="text-align: center;">
    <img src="https://sun9-68.userapi.com/impg/K1fAhPF39R7uSj7qDcwf9J2_KVPhAl9r2KqOPA/zGnB9Oq-9UA.jpg?size=565x619&quality=96&sign=803e9fbc57ffce0f7199387aa332d747&type=album" style="height: 300px;">
</div>

```
Данное приложение разработано и использованием Flask и имеет HTTP протоколы

Также в лабораторной использован бутстрап 5, который упрощает создание визуального интерфейса.
```

<hr>

Переход на различные страницы сайта и логика этих страниц пррописана в роутах app.py, который является контроллером.

_Пример кода в app.py:_ 

<div style="text-align: center;">
    <img src="https://sun9-74.userapi.com/impg/ss99fVrG9uBECAhnM3cRxhxAy9V-WIz4mZh_8A/vjeamFD2y3g.jpg?size=995x446&quality=96&sign=ce653078ac89764fee57689f491923b7&type=album" style="height: 300px;">
</div>

<hr>

__Актер__

Создание актера подразумевает:
- Указание его имени;
- Указание возраста актера;

Актеры создаются до того момента, пока места в студии не закончатся;

<div style="text-align: center;">
    <img src="https://sun9-57.userapi.com/impg/9Vv9jdqZpxlN4vGG06T2SzHkKA6-xp1Tt276tg/WigJCznFNEQ.jpg?size=1857x925&quality=96&sign=e47a519dca35904c22b8c9508e2811ef&type=album" style="height: 300px;">
</div>

<hr>

__Режиссер__

Создание режиссера подразумевает:
- Указание его имени;
- Указание его опыта;

Опыт режиссера должен совпадать с опытом для сценария;


<div style="text-align: center;">
    <img src="https://sun9-27.userapi.com/impg/lyJ9PTSwUmo_iMmlkoSfqtyaxLbgHFc0rhcCqQ/ZJv9hw3xEiI.jpg?size=1852x923&quality=96&sign=85ca403d5f0b3a755d06ce0511423b17&type=album" style="height: 300px;">
</div>

<hr>

__Сценарий__

Создание сценария подразумевает:
- Указаниие его названия;
- Указание типа сценария;
- Указание общего кол-ва актеров;
- Указание описания;
- Указание опыта режиссера;

Кол-во актеров должно совпадать с кол-вом актеров студии;

Тип сценария должен совпадать с типом площадки;

<div style="text-align: center;">
    <img src="https://sun9-77.userapi.com/impg/toB96YHsubNFQzVyPTXMix6eYaLqm0sx-l03Fw/lXKIN0gujvg.jpg?size=1857x923&quality=96&sign=56fa47599890e583a169436cc696445c&type=album" style="height: 300px;">
</div>

<hr>

__Площадка__

Создание площадки подразумевает указание ее типа.

<div style="text-align: center;">
    <img src="https://sun9-69.userapi.com/impg/_mCeooNoXbTD4Qe9783xF3jgHleNXuKUqC3TSg/bxPot3r6CpY.jpg?size=1861x919&quality=96&sign=3cd7b554ec71ffe1fd985ff27bf785d1&type=album" style="height: 300px;">
</div>

<hr>

__Студия__

Создание студии подразумевает:
- Указание названия;
- Указаниие кол-ва всех актеров;
- Указание кол-ва моложых актеров;
- Указание кол-ва взрослых актеров;

<div style="text-align: center;">
    <img src="https://sun9-13.userapi.com/impg/uB-2HVJNmBR1Rb_3aiIlz3A_wkdFNojXwFeWAg/7BefoknuS8s.jpg?size=1858x928&quality=96&sign=446c2ae84b22fb62c8065c39fb8ad9f2&type=album" style="height: 300px;">
</div>

<hr>

__Камера__

Камера позволяет менять расположение:
- Вправо;
- Влево;
- Вниз;
- Вверх;


<div style="text-align: center;">
    <img src="https://sun9-6.userapi.com/impg/BUT1IhhSsZxWL_1FgH-3TqSrK6SMO0J3d0RMPg/4HBxW8ENJOc.jpg?size=1861x926&quality=96&sign=f1913e2a8933ea6d5d826bc563e0345a&type=album" style="height: 300px;">
</div>

<hr>

__Изменение актеров__

Можно менять кол-во актеров.

- Если новое кол-во актеров меньше, то лишние актеры удаляются;
- Если новое кол-во актеров больше, то вас отправляет на поле создания актеров;

<div style="text-align: center;">
    <img src="https://sun9-65.userapi.com/impg/S3LG8Y5LxmUuo2jKUwzkP03a7CSDdDiSY6kIUA/AjdVENZHgak.jpg?size=1859x919&quality=96&sign=d5e67bd5cc32e37d9470396f1e4eaa70&type=album" style="height: 300px;">
</div>

<hr>

__Постпродакшн__

- Вы можете удалять ненужные кадры;
- Вы можете изменять позицию кадра, указав его старую позицию и новую;

<div style="text-align: center;">
    <img src="https://sun9-72.userapi.com/impg/NRX_XSdU9SBgUrIZAlnQZlIlRj4DBOu6exTxrg/fdvkmnn1W4c.jpg?size=1280x633&quality=96&sign=b2fe36829e57a15715893e4bf73ca523&type=album" style="height: 300px;">
</div>

<hr>

__Реализация__

Реализация отображает основную информацию киностудии.

https://sun9-59.userapi.com/impg/_EnangoFehD7RAu_7Z5ZiWMI6jmJLFismRqopA/Bv0nR30WOYU.jpg?size=1862x922&quality=96&sign=8095e14aedd961a2f21f0e3a7e2d97ad&type=album

<div style="text-align: center;">
    <img src="https://sun9-59.userapi.com/impg/_EnangoFehD7RAu_7Z5ZiWMI6jmJLFismRqopA/Bv0nR30WOYU.jpg?size=1862x922&quality=96&sign=8095e14aedd961a2f21f0e3a7e2d97ad&type=album" style="height: 300px;">
</div>
