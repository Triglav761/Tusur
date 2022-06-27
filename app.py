import app as app
import cv2
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm, RecaptchaField
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

app.debug = True
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

# Ключи для капчи
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfIwZ8gAAAAABE_Ch_6xbTMkOvt1tfjox-IPVw7'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfIwZ8gAAAAAJQaBoy92WOBg0pOMy0XHj3ouHrm'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}


class ColorForm(FlaskForm):
    img1 = FileField("Upload image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField("Submit", validators=[DataRequired()])
    choosing_colormaps = SelectField("Choosing_colormaps",
                                     choices=[("hot", "hot"), ("Blues", "Blues"), ("cool", "cool"), ("BuGn", "BuGn"),
                                              ("Dark2", "Dark2")],
                                     validators=[DataRequired()])
    recaptcha = RecaptchaField()


# меняет цветовую карту изображения
def color_pics(path, choosing_colormaps):
    image = Image.open(path)  # открываем изображение
    np_image = np.array(image)  # трансформируем в numpy массив
    plt.imshow(np_image[:, :, 1], cmap=choosing_colormaps)  # преобразуем изображение в 2D массив.
    plt.colorbar(orientation='vertical')  # цветовая шкала
    plt.title('', text=choosing_colormaps)  # название использованной цветовой карты
    plt.axis("off")  # убираем ось
    plt.savefig('./static/images/color_pics.jpg')  # сохраняем рисунок
    plt.close()  # закрываем, иначе при дальнейшем работе кода рисунок будет накладываться на другие.


def color_map(path):
    #  Создаем форму. В случае успешной валидации, переходим на страницу с результатом
    image = Image.open(path)
    # трансформируем изображение в numpy массив
    np_image = np.array(image)
    # транспонируем, чтобы получить доступ к значениям RGB
    image_transposed = np_image.transpose()
    # создаем массивы и записываем в них количество значений для каждой величины R, G и B
    rgb = [[]] * 3
    for i in range(3):
        rgb[i], bin = np.histogram(image_transposed[i], bins=256)
    # создаем график по получившимся данным и сохраняем его в виде изображения
    fig = plt.figure(figsize=(4, 4))
    # Separate Graph for each color
    plt.plot(rgb[0], color='red', linestyle='solid',
             marker='o', markerfacecolor='red', markersize=1)
    plt.plot(rgb[1], color='green', linestyle='solid', linewidth=1,
             marker='o', markerfacecolor='green', markersize=1)
    plt.plot(rgb[2], color='blue', linestyle='solid', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=1)
    # именуем сторону x
    plt.xlabel('x - axis')
    # именуем сторону y
    plt.ylabel('y - axis')
    plt.axis('tight')
    # даём название графику
    plt.title('График распределения цветов!')
    fig.savefig(f'./static/images/color_map.jpg', bbox_inches='tight')
    plt.close()
    return 0


def average_color_image(path):
    image_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    # Вычисляем среднее значение каждого канала BGR
    rgb = cv2.mean(image_bgr)
    # Вычисляем среднее значение каждого канала RGB
    observation = np.array([(rgb[0], rgb[1], rgb[2])])
    # Показать среднее значение канала
    observation
    # Показать изображение
    plt.imshow(observation), plt.axis("off")
    # даём название графику
    plt.title('Average color image')
    plt.savefig(f'./static/images/average_color_image.jpg')
    plt.show()


def average_color_graph(path):
    # Вычисляем среднее значение каждого канала
    image_rgb = cv2.imread(path, cv2.IMREAD_COLOR)
    rgb = cv2.mean(image_rgb)
    np.array([(rgb[0], rgb[1], rgb[2])])
    # Выводим значения для каждого цвета R G B
    plt.plot(rgb[0], color='red', marker='o', markersize=8)
    plt.plot(rgb[1], color='green', marker='o', markersize=8)
    plt.plot(rgb[2], color='blue', marker='o', markersize=8)
    # подписи
    plt.xlabel('horizontal')
    plt.ylabel('vertical')
    # название изображения
    plt.title('Average color graph')
    plt.savefig(f'./static/images/average_color_graph.jpg')
    plt.show()
    plt.close()


# главная страница приложения
@app.route("/", methods=["GET", "POST"])
def index():
    # очищаем папку static от файлов, загруженных в прошлой сессии
    files = os.listdir("./static/images/")
    if len(files) > 1:
        for file_path in files:
            if file_path != 'style.css':
                os.remove('./static/images/' + file_path)
    #  Создаем форму. В случае успешной валидации, переходим на страницу с результатом
    form = ColorForm()

    if form.validate_on_submit():
        choosing_colormaps = form.choosing_colormaps.data

    if form.validate_on_submit():  # возвращает True, когда форма была отправлена и данные были приняты всеми валидаторами полей

        filename = os.path.join('./static/images', secure_filename(form.img1.data.filename))
        form.img1.data.save(filename)
        color_map(filename)
        average_color_graph(filename)
        average_color_image(filename)
        color_pics(filename, choosing_colormaps)
        return redirect(url_for("result", image1=filename))

    return render_template("index.html", form=form)


@app.route("/result", methods=["GET"])
def result():
    # получаем названия файла и нужную форму из параметров функции redirect
    image1_path = request.args.get('image1')
    return render_template("result.html", image1=image1_path)
