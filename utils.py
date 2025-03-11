from PyQt6.QtGui import QImage, QColor, QStyleHints
from PyQt6.QtCore import Qt, QSize, QRect
from PIL import Image, ImageQt
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle


class ShapeDelegate(QStyledItemDelegate):
    """Custom delegate to center icons in QListWidget items."""

    def paint(self, painter, option, index):
        """Draw the icon centered in the item."""
        painter.save()

        rect = QRect(option.rect.x(), option.rect.y(), 50, option.rect.height())
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, QColor("#1c358a"))
        # Get the icon from the item data
        icon = index.data(Qt.ItemDataRole.DecorationRole)  # QIcon
        if icon:
            # Calculate the centered rectangle for the icon
            icon_size = QSize(24, 24)  # Match icon size
            icon_rect = QRect(0, 0, icon_size.width(), icon_size.height())
            icon_rect.moveCenter(rect.center())  # Center the icon in the item

            # Paint the icon centered
            icon.paint(painter, icon_rect, Qt.AlignmentFlag.AlignHCenter)

        painter.restore()

    def sizeHint(self, option, index):
        """Define the size of each item."""
        return QSize(50, 56)


def pil_to_qimage(pil_image):
    """Convert a PIL Image to a QImage."""
    qt_image = ImageQt.ImageQt(pil_image)
    return qt_image
