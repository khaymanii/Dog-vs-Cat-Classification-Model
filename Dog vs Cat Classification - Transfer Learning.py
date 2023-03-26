# Extracting Dataset using Kaggle API

# In[ ]:


# installing the Kaggle library
get_ipython().system('pip install kaggle')


# In[ ]:


# configuring the path of Kaggle.json file
get_ipython().system('mkdir -p ~/.kaggle')
get_ipython().system('cp kaggle.json ~/.kaggle/')
get_ipython().system('chmod 600 ~/.kaggle/kaggle.json')


# Importing the Dog vs Cat Dataset from Kaggle

# In[ ]:


# Kaggle api 
get_ipython().system('kaggle competitions download -c dogs-vs-cats')


# In[ ]:


get_ipython().system('ls')


# In[ ]:


# extracting the compressed dataset
from zipfile import ZipFile

dataset = '/content/dogs-vs-cats.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('The dataset is extracted')


# In[ ]:


# extracting the compressed dataset
from zipfile import ZipFile

dataset = '/content/train.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('The dataset is extracted')


# In[ ]:


import os
# counting the number of files in train folder
path, dirs, files = next(os.walk('/content/train'))
file_count = len(files)
print('Number of images: ', file_count)


# Printing the name of images

# In[ ]:


file_names = os.listdir('/content/train/')
print(file_names)


# Importing the Dependencies

# In[ ]:


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from google.colab.patches import cv2_imshow 


# Displaying the images of dogs and cats

# In[ ]:


# display dog image
img = mpimg.imread('/content/train/dog.8298.jpg')
imgplt = plt.imshow(img)
plt.show()


# In[ ]:


# display cat image
img = mpimg.imread('/content/train/cat.4352.jpg')
imgplt = plt.imshow(img)
plt.show()


# In[ ]:


file_names = os.listdir('/content/train/')

for i in range(5):

  name = file_names[i] 
  print(name[0:3])



# In[ ]:


file_names = os.listdir('/content/train/')

dog_count = 0
cat_count = 0

for img_file in file_names:

  name = img_file[0:3]

  if name == 'dog':
    dog_count += 1

  else:
    cat_count += 1

print('Number of dog images =', dog_count)
print('Number of cat images =', cat_count)


# Resizing all the images

# In[ ]:


#creating a directory for resized images
os.mkdir('/content/image resized')


# In[ ]:


original_folder = '/content/train/'
resized_folder = '/content/image resized/'

for i in range(2000):

  filename = os.listdir(original_folder)[i]
  img_path = original_folder+filename

  img = Image.open(img_path)
  img = img.resize((224, 224))
  img = img.convert('RGB')

  newImgPath = resized_folder+filename
  img.save(newImgPath)


# In[ ]:


# display resized dog image
img = mpimg.imread('/content/image resized/dog.8298.jpg')
imgplt = plt.imshow(img)
plt.show()


# In[ ]:


# display resized cat image
img = mpimg.imread('/content/image resized/cat.4352.jpg')
imgplt = plt.imshow(img)
plt.show()


# **Creating labels for resized images of dogs and cats**

# Cat --> 0
# 
# Dog --> 1

# In[ ]:


# creaing a for loop to assign labels
filenames = os.listdir('/content/image resized/')


labels = []

for i in range(2000):

  file_name = filenames[i]
  label = file_name[0:3]

  if label == 'dog':
    labels.append(1)

  else:
    labels.append(0)


# In[ ]:


print(filenames[0:5])
print(len(filenames))


# In[ ]:


print(labels[0:5])
print(len(labels))


# In[ ]:


# counting the images of dogs and cats out of 2000 images
values, counts = np.unique(labels, return_counts=True)
print(values)
print(counts)


# Converting all the resized images to numpy arrays

# In[ ]:


import cv2
import glob


# In[ ]:


image_directory = '/content/image resized/'
image_extension = ['png', 'jpg']

files = []

[files.extend(glob.glob(image_directory + '*.' + e)) for e in image_extension]

dog_cat_images = np.asarray([cv2.imread(file) for file in files])


# In[ ]:


print(dog_cat_images)


# In[ ]:


type(dog_cat_images)


# In[ ]:


print(dog_cat_images.shape)


# In[ ]:


X = dog_cat_images
Y = np.asarray(labels)


# **Train Test Split**

# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)


# In[ ]:


print(X.shape, X_train.shape, X_test.shape)


# 1600 --> training images
# 
# 400 --> test images

# In[ ]:


# scaling the data
X_train_scaled = X_train/255

X_test_scaled = X_test/255


# In[ ]:


print(X_train_scaled)


# **Building the Neural Network**

# In[ ]:


import tensorflow as tf
import tensorflow_hub as hub


# In[ ]:


mobilenet_model = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4'

pretrained_model = hub.KerasLayer(mobilenet_model, input_shape=(224,224,3), trainable=False)


# In[ ]:


num_of_classes = 2

model = tf.keras.Sequential([
    
    pretrained_model,
    tf.keras.layers.Dense(num_of_classes)

])

model.summary()


# In[ ]:


model.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics = ['acc']
)


# In[ ]:


model.fit(X_train_scaled, Y_train, epochs=5)


# In[ ]:


score, acc = model.evaluate(X_test_scaled, Y_test)
print('Test Loss =', score)
print('Test Accuracy =', acc)


# **Predictive System**

# In[ ]:


input_image_path = input('Path of the image to be predicted: ')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (224,224))

input_image_scaled = input_image_resize/255

image_reshaped = np.reshape(input_image_scaled, [1,224,224,3])

input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 0:
  print('The image represents a Cat')

else:
  print('The image represents a Dog')


# In[ ]:


input_image_path = input('Path of the image to be predicted: ')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (224,224))

input_image_scaled = input_image_resize/255

image_reshaped = np.reshape(input_image_scaled, [1,224,224,3])

input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 0:
  print('The image represents a Cat')

else:
  print('The image represents a Dog')


# In[ ]:




