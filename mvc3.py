import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Model(QAbstractItemModel):
    headers = 'トッピング', 'うどん/そば', '温/冷'
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = [
            ['たぬき','そば','温'],
            ['きつね','うどん','温'],
            ['月見','うどん','冷'],
            ['天ぷら','そば','温'],
            ]

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.items[index.row()][index.column()]
            except:
                return
        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]

    def addRow(self, topping, menkind, hotcold):
        self.beginInsertRows(QModelIndex(), len(self.items), 1)
        self.items.append([topping, menkind, hotcold])
        self.endInsertRows()

    def removeRows(self, rowIndexes):
        for row in sorted(rowIndexes, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row + 1)
            del self.items[row]
            self.endRemoveRows()


class View(QTreeView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setItemsExpandable(False)
        self.setIndentation(0)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def drawBranches(self, painter, rect, index):
        return


class InputWidget(QWidget):
    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)
        layout = QVBoxLayout()

        toppings = ('きつね', 'たぬき', 'てんぷら', '月見', '肉', 'カレー')
        self.toppingInput = QComboBox()
        for topping in toppings:
            self.toppingInput.addItem(topping)
        layout.addWidget(self.toppingInput)

        self.bgrp = QGroupBox()
        udon = QRadioButton('うどん')
        udon.setChecked(True)
        soba = QRadioButton('そば')
        btnlayout = QHBoxLayout()
        btnlayout.addWidget(udon)
        btnlayout.addWidget(soba)
        self.bgrp.setLayout(btnlayout)
        layout.addWidget(self.bgrp)
        self.udonsoba = udon, soba

        self.bgrp_temp = QGroupBox()
        hot = QRadioButton('温')
        hot.setChecked(True)
        cold = QRadioButton('冷')
        btnlayout_temp = QHBoxLayout()
        btnlayout_temp.addWidget(hot)
        btnlayout_temp.addWidget(cold)
        self.bgrp_temp.setLayout(btnlayout_temp)
        layout.addWidget(self.bgrp_temp)
        self.hotcold = hot, cold

        self.addButton = QPushButton('確定')
        layout.addWidget(self.addButton)

        layout.addStretch()

        self.setLayout(layout)

    def values(self):
        topping = self.toppingInput.currentText()

        udonsoba = '?'
        for btn in self.udonsoba:
            if btn.isChecked():
                udonsoba = btn.text()
                break

        hotcold = '?'
        for btn in self.hotcold:
            if btn.isChecked():
                hotcold = btn.text()
                break

        return topping, udonsoba, hotcold


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.view = View(self)
        self.model = Model(self)
        self.view.setModel(self.model)
        self.setCentralWidget(self.view)

        self.inputWidget = InputWidget()
        self.inputWidget.addButton.clicked.connect(self.addItem)
        self.addDock = QDockWidget('追加入力', self)
        self.addDock.setWidget(self.inputWidget)
        self.addDock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.RightDockWidgetArea, self.addDock)
        self.addDock.hide()

        toolBar = QToolBar()
        self.addToolBar(toolBar)

        delButton = QPushButton('削除')
        delButton.clicked.connect(self.removeItems)
        toolBar.addWidget(delButton)

        self.addButton = QPushButton('追加')
        self.addButton.clicked.connect(self.addDock.show)
        toolBar.addWidget(self.addButton)

    def addItem(self):
        self.model.addRow(*self.inputWidget.values())

    def selectedRows(self):
        rows = []
        for index in self.view.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def removeItems(self):
        self.model.removeRows(self.selectedRows())


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()
