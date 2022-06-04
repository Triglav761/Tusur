# Веб-приложение должно менять цветовые карты изображения r, g, b в соответствии
# с заданным пользователем порядком, выдавать графики распределения цветов
# исходной картинки и графики среднего значения цвета по вертикали и горизонтали.

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileRequired, FileAllowed
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(12).hex()


class CollageForm(FlaskForm):
    img1 = FileField("Upload image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    color_red = IntegerRangeField("Red", default=0, validators=[NumberRange(min=0, max=255)])
    color_green = IntegerRangeField("Green", default=0, validators=[NumberRange(min=0, max=255)])
    color_blue = IntegerRangeField("Blue", default=0, validators=[NumberRange(min=0, max=255)])
    submit = SubmitField("Submit", validators=[DataRequired()])


# Веб-приложение должно менять цветовые карты изображения r, g, b в соответствии
# с заданным пользователем порядком
def color_change(img1, color_red, color_green, color_blue):
    # fig, axes = plt.subplots(nrows=1, ncols=3)  # функция, которая возвращает кортеж, содержащий объект фигуры и осей

    #  Данные в image доступны только для чтения
    # image_1 = img1.copy()
    # image_2 = img1.copy()
    # image_3 = img1.copy()
    # image_1[:, :, 0] = 0
    # axes[0].imshow(image_1)

    # image_2[:, :, 1] = 0
    # axes[1].imshow(image_2)

    # image_3[:, :, 2] = 0
    # axes[2].imshow(image_3)

    # for ax in axes:
    #    ax.set_xticks([])
    #    ax.set_yticks([])
    img_color_change = Image.new('RGB', (color_red, color_green, color_blue))
    img_color_change.paste(img1, (color_red, color_green, color_blue))
    # fig.set_figwidth(12)
    # fig.set_figheight(6)
    return None


# выдавать графики распределения цветов исходной картинки и графики среднего значения цвета по вертикали и горизонтали.
# Доделать выдачу средних значений.!!
def get_color_chart(path, filename):
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
    viewer.plot(rgb[0], color='r')
    viewer.plot(rgb[1], color='g')
    viewer.plot(rgb[2], color='b')
    fig.savefig(f'./static/{filename}.png')
    return 0


#collage_path = './static/collage.jpg'


# главная страница приложения
@app.route("/", methods=["GET", "POST"])
def index():
    # очищаем папку static от файлов, загруженных в прошлой сессии
    files = os.listdir("./static")
    if len(files) > 1:
        for file_path in files:
            if file_path != 'style.css':
                os.remove('./static/' + file_path)
    #  Создаем форму. В случае успешной валидации, переходим на страницу с результатом
    form = CollageForm()  # Класс

    if form.validate_on_submit():  # возвращает True, когда форма была отправлена и данные были приняты всеми валидаторами полей
        filename1 = os.path.join('./static', secure_filename(form.img1.data.filename))
        form.img1.data.save(filename1)
        color_red = form.color_red.data
        color_green = form.color_green.data
        color_blue = form.color_blue.data
        # открываем изображение
        image1 = Image.open(filename1)
        # комбинируем изображения и сохраняем файл
        #collage = color_change(image1, image2, color_red, color_green, color_blue)
        #collage.save(collage_path)
        get_color_chart(filename1, 'hist1')
        # get_color_chart(filename2, 'hist2')
        #get_color_chart(collage_path, 'hist3')
        return redirect(url_for("result", image1=filename1))

    return render_template("index.html", form=form)


@app.route("/result", methods=["GET"])
def result():
    # получаем названия файла и нужную форму коллажа из параметров функции redirect
    image1_path = request.args.get('image1')
    # image2_path = request.args.get('image2')

    return render_template("result.html", image1=image1_path)
