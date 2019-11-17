from PySide2.QtCore import Signal, Slot, Property, QTimer
from PySide2.QtGui import QImage
from PySide2.QtQuick import QQuickItem, QSGSimpleTextureNode
import cv2

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

    fpsChanged = Signal(float)

    @Property(float, notify=fpsChanged)
    def fps(self):
        self._fps

    @fps.setter
    def setFps(self, fps):
        if fps == self._fps:
            return
        self._fps = fps
        self.fpsChanged.emit(self.onFpsChanged)

    def onFpsChanged(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._capture)
        self._timer.start(1000 / self._fps)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = None
        self._video = None
        self._fps = None
        self._root_node = None
        self.sourceChanged.connect(self.onSourceChanged)
        self.fpsChanged.connect(self.onFpsChanged)

        self._image = QImage()
        self._texture = None
        self._x = 0
        self._y = 0
        self._width = 640
        self._height = 480
        self._fit_to_screen = False

        self.setFlag(QQuickItem.ItemHasContents, True)

    def geometryChanged(self, new_geometry, old_geometry):
        if self._image:
            self._calcAspectRatio(new_geometry)

    def updatePaintNode(self, old_node, node_data):
        if self._root_node is None:
            self._root_node = QSGSimpleTextureNode()

        if self._texture:
            self._texture.deleteLater()
        self._texture = self.window().createTextureFromImage(self._image)
        self._root_node.setTexture(self._texture)
        self._root_node.setRect(self._x, self._y, self._width, self._height)

        return self._root_node

    def _capture(self):
        ret, frame = self._video.read()
        if ret == False:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        stride = frame.strides[0]
        self._image = QImage(frame.data, w, h, stride, QImage.Format_RGB888)

        if not self._fit_to_screen:
            self._calcAspectRatio(self.window().geometry())
            self._fit_to_screen = True

        self.update()

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
