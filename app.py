# Веб-приложение должно менять цветовые карты изображения r, g, b в соответствии
# с заданным пользователем порядком, выдавать графики распределения цветов
# исходной картинки и графики среднего значения цвета по вертикали и горизонтали.
import cv2
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(12).hex()


class ColorForm(FlaskForm):
    img1 = FileField("Upload image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField("Submit", validators=[DataRequired()])
    choosing_colormaps = SelectField("Choosing_colormaps",
                                     choices=[("hot", "hot"), ("Blues", "Blues"), ("cool", "cool"), ("BuGn", "BuGn"),
                                              ("Dark2", "Dark2")],
                                     validators=[DataRequired()])

#меняет цветовую карту изображения
def color_pics(path, choosing_colormaps):
    image = Image.open(path)
    np_image = np.array(image)
    plt.imshow(np_image[:, :, 1], cmap=choosing_colormaps)
    plt.colorbar(orientation='vertical')
    plt.title('Color map:', text=choosing_colormaps)
    plt.savefig('./static/images/new_image.jpg')
    plt.close()


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
    viewer = fig.add_subplot(1, 1, 1)
    plt.plot(rgb[0], color='red', linestyle='solid', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=1)
    plt.plot(rgb[1], color='green', linestyle='solid', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=1)
    plt.plot(rgb[2], color='blue', linestyle='solid', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=1)
    # setting x and y axis range
    plt.ylim()
    plt.xlim()

    # именуем сторону x
    plt.xlabel('x - axis')
    # именуем сторону y
    plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title('График распределения цветов!')
    fig.savefig(f'./static/images/color_map.jpg')
    plt.close()
    return 0

###################
# Load image as BGR
def average_color_image(path):
    image_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    # Calculate the mean of each channel
    rgb = cv2.mean(image_bgr)

    # Swap blue and red values (making it RGB, not BGR)
    observation = np.array([(rgb[0], rgb[1], rgb[2])])
    # Show mean channel values
    observation
    # Show image
    plt.imshow(observation), plt.axis("off")
    plt.savefig(f'./static/images/average_color_image.jpg')
    plt.show()

##############
# Load image as BGR
def average_color_graph(path):
    image_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    # Calculate the mean of each channel
    rgb = cv2.mean(image_bgr)

    # Swap blue and red values (making it RGB, not BGR)
    np.array([(rgb[0], rgb[1], rgb[2])])
    # Show mean channel values
    print(rgb[1])
    plt.plot(rgb[0], color='red', linestyle='dotted', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=8)
    plt.plot(rgb[1], color='green', linestyle='dotted', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=8)
    plt.plot(rgb[2], color='blue', linestyle='dotted', linewidth=1,
             marker='o', markerfacecolor='blue', markersize=8)
    # setting x and y axis range
    plt.ylim()
    plt.xlim()

    plt.xlabel('horizontal')
    plt.ylabel('vertical')
    plt.title('График среднего значения цвета')
    plt.savefig(f'./static/images/average_color_graph.jpg')
    plt.show()
    plt.close()
##############
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
