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
#  Создаем форму. В случае успешной валидации, переходим на страницу с результатом
image = Image.open('./static/images/1.jpg')
# трансформируем изображение в numpy массив
np_image = np.array(image)
# транспонируем, чтобы получить доступ к значениям RGB
image_transposed = np_image.transpose()
rgb = [[]] * 3
for i in range(3):
    rgb[i], bin = np.histogram(image_transposed[i], bins=256)
# x axis values
#x = [1, 2, 3, 4, 5, 6]
## corresponding y axis values
#y = [2, 4, 1, 5, 2, 6]

# plotting the points
plt.plot(rgb[0], color='red', linestyle='solid', linewidth=1,
         marker='o', markerfacecolor='blue', markersize=1)
plt.plot(rgb[1], color='green', linestyle='solid', linewidth=1,
         marker='o', markerfacecolor='blue', markersize=1)
plt.plot(rgb[2], color='blue', linestyle='solid', linewidth=1,
         marker='o', markerfacecolor='blue', markersize=1)
# setting x and y axis range
plt.ylim()
plt.xlim()

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('Some cool customizations!')

# function to show the plot
plt.show()