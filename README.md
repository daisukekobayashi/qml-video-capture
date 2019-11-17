# QML VideoCapture

This repository contains VideoCapture type to be usable from QML.
Capturing image using OpenCV VideoCapture class and rendering the image on Qt Quick Scene Graph.

You can change video source to specify source property as follows.

```js
VideoCapture {
    source: "0" // camera index. you have to specify index in string.
    //source: "/path/to/video.avi"
    //source: "img_%02d.jpg"
    //source: "http://localhost:8080/mjpeg"
}
```
