# Веб-приложение должно менять цветовые карты изображения r, g, b в соответствии
# с заданным пользователем порядком, выдавать графики распределения цветов
# исходной картинки и графики среднего значения цвета по вертикали и горизонтали.
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
    shape = SelectField("Collage shape", choices=[("Accent", "Accent"),("Blues", "Blues"), ("cool", "cool"),("BuGn", "BuGn"), ("Dark2", "Dark2")],
                        validators=[DataRequired()])


# выдавать графики распределения цветов исходной картинки и графики среднего значения цвета по вертикали и горизонтали.
# Доделать выдачу средних значений.!!
def color_map(path, filename): # график
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


collage_path = './static/collage.jpg'
#############
def color_pics(path, shape):
    image=Image.open(path)
    np_image = np.array(image)
    print(shape)
    plt.imshow(np_image[:, :, 1], cmap=shape)
    plt.savefig('./static/new_image.jpg')

    ############

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
    form = ColorForm()

    if form.validate_on_submit():
        shape=form.shape.data
        print(form.shape.data)
    if form.validate_on_submit():  # возвращает True, когда форма была отправлена и данные были приняты всеми валидаторами полей
        filename1 = os.path.join('./static', secure_filename(form.img1.data.filename))
        form.img1.data.save(filename1)
        # открываем изображение
        #Открывает и идентифицирует данный файл изображения.
        #Это ленивая операция; эта функция идентифицирует файл, но файл остается открытым,
        # и фактические данные изображения не считываются из файла, пока вы не попытаетесь обработать данные (или вызвать load()метод).
        image1 = Image.open(filename1)
        color_pics(filename1, shape)
        color_map(filename1, 'hist1')

        #get_color_chart(collage_path, 'hist2')
        # get_color_chart(collage_path, 'hist2')
        return redirect(url_for("result", image1=filename1))

    return render_template("index.html", form=form)


@app.route("/result", methods=["GET"])
def result():
    # получаем названия файла и нужную форму коллажа из параметров функции redirect
    image1_path = request.args.get('image1')
    # image2_path = request.args.get('image2')

    return render_template("result.html", image1=image1_path)
