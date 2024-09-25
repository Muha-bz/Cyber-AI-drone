
[![Typing SVG](https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&weight=600&size=25&duration=3000&pause=1000&color=1ACAAA&background=11167B00&multiline=true&width=465&height=65&lines=%F0%9F%91%8B+%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%2C+%D0%BC%D1%8B+%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0+Cyber+AI+drone;%D0%B8+%D0%BC%D1%8B+%D1%83%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA%D0%B8+Brics+2024)](https://git.io/typing-svg)
## О проекте "Мы найдем тебя"

### Цель и актуальность работы
Организация спасательной операции (миссии) с формированием полётного задания в пересеченной местности при помощи КБС (Комплексной беспилотной системы) с использованием нейросети: обнаружение, доставка груза (без сброса), передача координат. Задание расчитано на самостоятельный забор груза. На этот проект нас вдохновил добровольческий поисковый отряд " ЛизаАлерт", ставящий своей задачей оперативное реагирование и гражданское содействие в поиске пропавших

Использование технологий искусственного интеллекта позволяет не только улучшить точность идентификации объектов, но и способствует адаптации к изменениям окружающей среды и постоянному самосовершенствованию системы за счет обучения на собранных данных.
## Миссия 
**`Задание для коптера`**
* Взлететь с точки взлёта. Световая индикация **`Lime`**. 
* Облететь полигон. Световая индикация **`Crimson`**.
* При обнаружении Ровера цвет светодиодной ленты поменять на **`Yellow`** , при обнаружении камня(мяч) моргнуть **`Blue`** цветом,  при обнаружении дерева(цветка) моргнуть **`SaddleBrown`**, при обнаружении человека (**Манекена**) моргнуть **`Green`** . Определять объекты с помощью компьютерного зрения.
* В топике подписать **`Название всех объектов`**, обозначить их цвет и обвести контур всех обнаруженных объектов.
* **`Создать отчёт`**, в котором будет находится информация обо всех обнаруженных объектах, их место расположения и цвет.
* Посадка в точку взлёта. Световая индикация **`Purple`**


**`Задание для ровера`** 
* Выехать с зоны парковки. Вкл. фары.
* Начать алгоритм движения по траектории, избегая столкновений с элементами полигона
* Найти объект. Моргнуть трижды фарами. Передать груз
* Вернуться в зону парковки. Выкл. фары

## Порядок выполнения проверки
    
**https://1drv.ms/x/c/8e997581c10a3126/ETir6DfYjeVNn_z09sgygx0BI8vJJylXbXAf2D9sMxTCXQ?e=QzCvJ1**
    
## План работ
* Продумать алгоритм работы ​
* Создать нейронную сеть​
* Написать код распознавания объектов​
* Написать алгоритм движения ровера по данным полученным из неиросети

Подробнее вы можете ознакомиться с планом в приложении **https://1drv.ms/x/c/8e997581c10a3126/EZwav9RLN3lFmgS0CpPVzr8BZBBNfjNsvDEk8561q5dxOw?e=LDzxkx**
## Нейронная сеть
Она была создана при помощи **`yolov8`** и **`roboflow`**. При помощи **`roboflow`** мы создали dataset и загрузили его в **`ultralytics hub`**.

## Выполнение миссии
Для выполнения миссии нам понадобилась библиотека **`opencv`**. Мы использовали различные маски для детекции объектов для последующего использования, чтобы найти объекты. Был создан алгоритм для проследующего движения ровера к месту обнаружения пострадавшего.


## О команде
В нашей команде 4 человека:

**`Хамматов Булат​`**  тестировка и отладка оборудования

**`Иваненко Артём`**  создание и обучение нейронных сетей

**`Толкунов Иван`**:  алгоритм движения ровера

**`Мухина Кира`**:  программа для детекции объектов

**`Роли и обязоности приведены ниже `**

![Описание изображения](images/1.jpg)

![Описание изображения](images/2.jpg)

*https://1drv.ms/x/c/8e997581c10a3126/Ecr18pxTuWlFv4xwWPiLGBMBWcGFFrLzbj5pNkoTytCJAA?e=10Tqwt*


Хотим представить решение поставленной задачи в компетенции **`"Искусвенный интелект в комплексных беспилотных системах"`**.
## 📖 содержание
