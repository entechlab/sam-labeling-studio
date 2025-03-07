# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customwidget.ui'
#
# Created by: PyQt6 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class CustomListItemWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomListItemWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ObjectListItem")

        # Set size policy to expand horizontally
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)  # Add some margins
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.object_label = QtWidgets.QLabel(self)
        self.object_label.setObjectName("object_label")
        self.verticalLayout.addWidget(self.object_label)

        self.shape_label = QtWidgets.QLabel(self)
        self.shape_label.setObjectName("shape_label")
        self.verticalLayout.addWidget(self.shape_label)

        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addStretch(1)  # Add stretch to push widgets to left

        self.label_combo_box = QtWidgets.QComboBox(self)
        self.label_combo_box.setObjectName("label_combo_box")
        self.label_combo_box.addItem("RTU")
        self.label_combo_box.addItem("Air-Cooled Chiller")
        self.label_combo_box.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,  # This is the key change
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.horizontalLayout.addWidget(self.label_combo_box, 3)

        self.lock_button = QtWidgets.QToolButton(self)
        self.lock_button.setObjectName("lock_button")
        self.lock_button.setText("🔒")
        self.horizontalLayout.addWidget(self.lock_button)

        self.pin_button = QtWidgets.QToolButton(self)
        self.pin_button.setObjectName("pin_button")
        self.pin_button.setText("📌")
        self.horizontalLayout.addWidget(self.pin_button)

        self.object_label.setText("Object")
        self.shape_label.setText("Polygon")

        # Setting stretch factor for the widgets
        self.horizontalLayout.setStretch(0, 20)  # Labels get 20%
        self.horizontalLayout.setStretch(1, 5)  # Stretch gets 5%
        self.horizontalLayout.setStretch(2, 60)  # Combo box gets 60%
        self.horizontalLayout.setStretch(3, 8)  # Lock button gets 7.5%
        self.horizontalLayout.setStretch(4, 7)  # Pin button gets 7.5%


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    object_list_item = CustomListItemWidget()
    # ui = Ui_CustomListItemWidget()
    # ui.setupUi(object_list_item)
    object_list_item.show()
    sys.exit(app.exec())
