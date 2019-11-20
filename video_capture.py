import logging
import queue
import threading
import time

import cv2

from PySide2.QtCore import Signal, Slot, Property, QTimer
from PySide2.QtGui import QImage
from PySide2.QtQuick import QQuickItem, QSGSimpleTextureNode

logging.basicConfig(level=logging.INFO)

class VideoCapture(QQuickItem):

    sourceChanged = Signal(str)

    @Property(str, notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def setSource(self, source):
        if source == self._source:
            return
        self._source = source
        self.sourceChanged.emit(self._source)

    def onSourceChanged(self):
        self._video = self._createVideoCapture(self._source)

    processFinished = Signal()

    def onProcessFinished(self):
        self.update()

    @Slot()
    def start(self):
        if self._capture_thread is None:
            self._capture_thread = threading.Thread(target=self._capture)
            self._capture_thread.setDaemon(True)
            self._capture_thread.start()
        if self._process_thread is None:
            self._process_thread = threading.Thread(target=self._process)
            self._process_thread.setDaemon(True)
            self._process_thread.start()

    @Slot()
    def stop(self):
        if self._process_thread is not None:
            self._process_thread.do_run = False
            self._process_thread.join()
            self._process_thread = None
        if self._capture_thread is not None:
            self._capture_thread.do_run = False
            self._capture_thread.join()
            self._capture_thread = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = None
        self._video = None
        self._root_node = None
        self.sourceChanged.connect(self.onSourceChanged)
        self.processFinished.connect(self.onProcessFinished)

        self._image = None
        self._texture = None
        self._x = 0
        self._y = 0
        self._width = 640
        self._height = 480
        self._fit_to_screen = False

        self.setFlag(QQuickItem.ItemHasContents, True)
        self._frame_queue = queue.Queue(3)
        self._qimage_queue = queue.Queue(3)
        self._capture_thread = None
        self._process_thread = None

    def geometryChanged(self, new_geometry, old_geometry):
        if self._image:
            self._calcAspectRatio(new_geometry)

    def updatePaintNode(self, old_node, node_data):
        if self._root_node is None:
            self._root_node = QSGSimpleTextureNode()

        if self._qimage_queue.empty():
            return old_node

        if self._texture:
            self._texture.deleteLater()
            self._texture = None

        self._image = self._qimage_queue.get()
        self._texture = self.window().createTextureFromImage(self._image)
        self._root_node.setTexture(self._texture)

        if not self._fit_to_screen:
            self._calcAspectRatio(self.window().geometry())
            self._fit_to_screen = True

        self._root_node.setRect(self._x, self._y, self._width, self._height)

        return self._root_node

    def _capture(self):
        t = threading.currentThread()
        while getattr(t, 'do_run', True):
            ret, frame = self._video.read()
            if ret == False:
                continue
            if self._frame_queue.full():
                self._frame_queue.get()

            self._frame_queue.put(frame)
            time.sleep(0.001)

    def _process(self):
        t = threading.currentThread()
        while getattr(t, 'do_run', True):
            frame = self._frame_queue.get()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w = frame.shape[:2]
            stride = frame.strides[0]
            image = QImage(frame.data, w, h, stride, QImage.Format_RGB888)
            if self._qimage_queue.full():
                self._qimage_queue.get()

            self._qimage_queue.put(image)
            self.processFinished.emit()
            time.sleep(0.001)

    def _calcAspectRatio(self, geometry):
        x, y = geometry.x(), geometry.y()
        width, height = geometry.width(), geometry.height()

        image_aspect = self._image.width() / float(self._image.height())
        display_aspect = width / float(height)

        if int(display_aspect * 1000) == int(image_aspect * 1000):
            self._width = width
            self._height = height
        elif height * image_aspect > width:
            self._width = width
            self._height = width / image_aspect
        else:
            self._width = height * image_aspect
            self._height = height

        self._x = (width - self._width) / 2.0
        self._y = (height - self._height) / 2.0

    def _createVideoCapture(self, source):
        if self._source.isdecimal():
            video = cv2.VideoCapture(int(self._source))
        else:
            video = cv2.VideoCapture(self._source)
        return video
