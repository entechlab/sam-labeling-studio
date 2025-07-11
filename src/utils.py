from enum import Enum
import logging
from typing import Optional
import os
from dataclasses import dataclass

from PyQt6.QtGui import QImage, QColor, QStyleHints, QIcon, QPixmap, QPainter
from PyQt6.QtCore import QRectF, Qt, QSize, QRect, QPoint
from PIL import Image, ImageQt
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle

from PyQt6.QtSvg import QSvgRenderer

import numpy as np


# Custom Logger formater
# from https://github.com/openai/preparedness/blob/main/project/paperbench/paperbench/utils.py
class CustomFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = record.getMessage()

        level_colors = {
            "DEBUG": "\033[38;5;39m",
            "INFO": "\033[38;5;15m",
            "WARNING": "\033[38;5;214m",
            "ERROR": "\033[38;5;203m",
            "CRITICAL": "\033[1;38;5;231;48;5;197m",
        }

        level_color = level_colors.get(levelname, "\033[0m")
        record.levelname = f"{level_color}{levelname:<8}\033[0m"
        record.asctime = f"\033[38;5;240m{self.formatTime(record, self.datefmt)}\033[0m"
        record.custom_location = (
            f"\033[38;5;240m{record.name}.{record.funcName}:{record.lineno}\033[0m"
        )
        record.msg = f"{level_color}{message}\033[0m"

        return super().format(record)


class DataSource(Enum):
    URL_REQUEST = 0
    LOCAL = 1


class ControlItem(Enum):
    NORMAL = 0
    BOX = 1
    POLYGON = 2
    ZOOM_IN = 3
    ZOOM_OUT = 4
    ROI = 5
    STAR = 6


class ModelPrompts(Enum):
    BOX = 0
    POINT = 1
    TEXT = 2


@dataclass
class MaskData(object):
    """
    Mask information data class(poly or box)
    mask_id: int
        Unique id for the mask()
    points: list[list[int]]
        List of [x,y] coordinates
    label: int
        label id
    center: (x,y)
    """

    def __init__(self, mask_id: int, points: list, label, center):
        self.id = mask_id
        self.points = points
        self.label = label
        self.center = center


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


# from https://github.com/openai/preparedness/blob/main/project/paperbench/paperbench/utils.py
def get_logger(name: Optional[str] = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.propagate = False
    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        fmt = "%(asctime)s | %(levelname)s | %(custom_location)s - %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S.%f"
        formatter = CustomFormatter(fmt=fmt, datefmt=datefmt)

        if os.environ.get("DISABLE_COLORED_LOGGING") == "1":
            formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def pil_to_qimage(pil_image):
    """Convert a PIL Image to a QImage."""
    qt_image = ImageQt.ImageQt(pil_image)
    return qt_image


def gray_out_icon(icon):
    """Convert an icon to a grayed-out version."""
    pixmap = icon.pixmap(48, 48, QIcon.Mode.Disabled)
    return QIcon(pixmap)


def read_colors(text_file):
    color_dict = {}
    with open(os.environ["HOME"] + "/" + text_file, "r") as f:
        for line in f:
            line_cols = line.strip().split(" ")
            color_dict[" ".join(line_cols[3:])] = (
                int(line_cols[0]),
                int(line_cols[1]),
                int(line_cols[2]),
            )
    return color_dict


def svg_to_icon(svg_string, size):
    """Convert an SVG string to a QIcon."""
    renderer = QSvgRenderer(bytearray(svg_string.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


def is_inside_rect(rect: QRectF, point: QPoint):
    rect_coords = rect.getCoords()
    x, y = point.x(), point.y()
    if (
        (x < rect_coords[0])
        or (x > rect_coords[2])
        or (y < rect_coords[1])
        or (y > rect_coords[3])
    ):
        return False
    return True


def get_convex_hull(pred_img: np.ndarray, bg_value: int = 0, k=6) -> np.ndarray:

    pred_cumsum = pred_img[pred_img.any(1)].cumsum(axis=1)
    start_y = pred_img[pred_img.any(1)].argmax(axis=1)
    end_y = pred_cumsum.argmax(axis=1)
    xs = np.where(pred_img.any(1, keepdims=False))[0]
    # xs, ys = np.apply_along_axis(get_first_last_occurrence, 1, pred_img)
    # xs, ys = np.where(pred_img != bg_value)
    indices = list(zip(np.concatenate((xs, xs)), np.concatenate((start_y, end_y))))
    # from scipy.spatial import ConvexHull
    import smallest_kgon as s_kgon

    # hull_indices = ConvexHull(np.array(indices)).vertices
    # convex_hull = np.array([indices[i] for i in hull_indices])
    hull_points = s_kgon.smallest_kgon(np.array(indices).astype(np.float32), k=k)
    return hull_points


def get_convex_hull_v2(pred_img: np.ndarray, bg_value: int = 0, k=6) -> np.ndarray:
    # from scipy.spatial import ConvexHull
    import smallest_kgon as s_kgon

    xs, ys = np.where(pred_img != bg_value)
    indices = list(zip(xs, ys))
    hull_points = s_kgon.smallest_kgon(np.array(indices).astype(np.float32), k=k)
    return hull_points
