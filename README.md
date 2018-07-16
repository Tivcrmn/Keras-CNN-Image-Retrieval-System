# Keras CNN Image Retrieval System

It is my capstone project for my bachelor degree. It uses the most popular machine learning algorithm CNN and tech stacks Keras to build a image retrieval system. For better user experience, I integrate the system with a web application with Vue and the server side with Django and MongoDB. And it also implements the [bianry hash code paper](https://github.com/Tivcrmn/Keras-CNN-Image-Retrieval-System/blob/master/Lin_Deep_Learning_of_2015_CVPR_paper.pdf) thanks to the code of [arpit512512](https://github.com/arpit512512/Deep-Learning-of-Binary-Hash-Codes-for-Faster-Image-Retrieval/blob/master/notebook.ipynb).

### Prerequisits

1. Install all the stacks. The front end needs npm to install all the dependencies. And I recommend use conda (you can install it by installing anaconda) to install packages for the server and the core system.

2. The datasets are [Caltech101](http://www.vision.caltech.edu/Image_Datasets/Caltech101/). You need to download it and push all the images in server/database. As you can see. I have put some in it, and all the image are classfied into different directories named with the category.

3. Generate all the h5 file And put all the data in MongoDB locally.
![](./assets/h5.jpg)
All the 6 files can be generated using the model jupyter notebook in this repo. For better understanding of the  [bianry hash code paper](https://github.com/Tivcrmn/Keras-CNN-Image-Retrieval-System/blob/master/Lin_Deep_Learning_of_2015_CVPR_paper.pdf) algorithm, you should better see the model first, because it is the core of this project. And the 2 index h5 file is for storing the Caltech101 images features and you need to using save.py to put all the info in database. And other 4 model file should be placed in server/h5File and are used for extracting new pictures uploaded from the front end.

### How to run it ?

1. For the server, run

```python
python manage.py runserver
```

2. For the client, run

```js
npm run dev
```

### Examples

Overview

![](./assets/web.png)

1. Query in database

![](./assets/query-1.png)

![](./assets/query-2.png)

2. Upload Query

![](./assets/upload-1.png)

![](./assets/upload-2.png)

### Result

![](./assets/result-map.png)

![](./assets/result-time.png)

### Finally

It might be the only period of time for me to do something with ML and DL. But it is fun. Hope this project is helpful to you. And I put my capstone thesis in the repo, even though it is chinese, but you might find it helpful in some aspects. If you have any questions, feel free to contact me!
