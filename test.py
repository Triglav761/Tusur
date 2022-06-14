from PIL import Image
import numpy as np

# from skimage import io,data
#image = Image.open('1.jpg')
#image[:, :, 0]
#image.show()
import matplotlib.pyplot as plt


image = plt.imread('1.jpg') # читаем изображение
#plt.axis('off') # отключить рамку
cat_image= image[:, :, 0]

plt.imshow(cat_image, cmap='plasma')# добавить палитру цветов к лабораторке :) cmap

plt.savefig('static/savefig.jpg')
plt.show()
#for i in range(0, 200,1):
#    if i < 50:
#        val_list = [2] * 200
#    elif i < 100:
#        val_list = [5] * 200
#    elif i < 150:
#        val_list = [10] * 200
#    vals.append(val_list)
#
#plt.pcolormesh (vals, cmap=plt.get_cmap('jet', 11), alpha=0.5)
#plt.axis('off')
#plt.colorbar()
#

#np.random.seed(123)
#data = np.random.rand(5, 7)
#plt.pcolormesh(data, cmap='plasma', edgecolors="k", shading='flat')
#plt.show()

## Преобразование данных изображения в массив для сохранения
## img = np.asarray(Image.open('1.jpg').convert('RGB'))
#x = Image.open('1.jpg').convert('RGB')
#print(x.format)
#print(x.mode)
#print(x.size)
##x.show()
#x[56:112,:] = np.random.rand(3)[np.newaxis,np.newaxis,:]
#x.show()
# with Image.open('1.jpg') as im:
#  im_data = np.array(im) # Преобразовать данные изображения в массив
#  im_l = im.convert('L') # Серое изображение
#  im_l_data = np.array(im_l) # Преобразование изображения в оттенках серого в массив
#  im_l.save('11.jpg')
#  open('11.jpg')
# print("im_data.shape",im_data.shape) # Вывести форму массива цветных изображений, output (1920, 1080, 3)
# print("im_l_data.shape", im_l_data.shape) # Вывести форму массива изображений в градациях серого, output (1920, 1080)
##сохранять данные
# np.savez('a_array.npz', a_dat = im_data, a_l_dat = im_l_data) # Сохраняем данные изображения в сжатый файл
## Прочитать сохраненные данные
# data = np.load('a_array.npz') # Загрузить данные, доступ к возвращаемым данным осуществляется через имя ключа и устанавливается как имя сохраненного массива
# print(data.keys()) #Return ['a_dat', 'a_l_dat']
## Оценка того, совпадают ли считанные и сохраненные данные
# print(np.all(data[data.keys()[0]] == im_data), np.all(data[data.keys()[1]] == im_l_data)) #Output True True
#
