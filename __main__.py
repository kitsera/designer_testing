from PyQt5 import uic, QtWidgets, QtCore, QtGui
import form
from Cryterion import *
import sys

class CryterionTableModel(QtCore.QAbstractTableModel):

    def __init__(self, table, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.table = table
        self.headers = ['Конкуренція\n на тому ж\n рівні', 'Конкуренція\n трішки\n посилилась', 'Конкуренція\n різко\n посилилась']
        self.v_headers = ['Продовжити роботу\n в звичайному режимі', "Активувати\n рекламну діяльність", "Активувати рекламу\n і знизити ціну"]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.table)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.table[0])

    def data(self, QModelIndex, int_role=None):
        row = QModelIndex.row()
        column = QModelIndex.column()
        if int_role == QtCore.Qt.DisplayRole:
            return self.table[row][column]
        if int_role == QtCore.Qt.EditRole:
            return  self.table[row][column]
        if column > 2:
            maximum = []
            for i in range(3):
                maximum.append(self.table[i][column])
            if int_role == QtCore.Qt.TextColorRole and self.table[row][column] == max(maximum):
                return QtGui.QColor('#ff5555')

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == QtCore.Qt.DisplayRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return self.headers[p_int]
            else:
                return self.v_headers[p_int]

    def flags(self, QModelIndex):
        if QModelIndex.column()<3:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return  QtCore.Qt.ItemIsSelectable

    def insertColumns(self, position, columns, QModelIndex_parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertColumns(QModelIndex_parent, position, position+columns-1)
        rowCount = len(self.table)

        for i in range(columns):
            for j in range(rowCount):
                self.table[j].insert(position, args[i].get('values')[j])
            self.headers.append(args[i].get('name'))

        self.endInsertColumns()


class MyWindow(QtWidgets.QMainWindow, form.Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.set_table()
        self.pushButton.clicked.connect(self.btn_clicked)
        self.setFixedSize(1200,250)

    def set_table(self):
        self.table = [[100, 80, 40],
                 [70, 90, 50],
                 [50, 70, 80]]
        self.table_model = CryterionTableModel(self.table)
        self.tableView.setModel(self.table_model)
        for i in range(3):
            self.tableView.setColumnWidth(i, 200)
            self.tableView.setRowHeight(i, 50)

    def btn_clicked(self):
        table = [[100, 80, 40],
                 [70, 90, 50],
                 [50, 70, 80]]
        vald = Vald(table)
        gulvic = Gulvic(table)
        laplas = Laplas(table)
        bayes_laplas = Bayes_Laplas(self.table)
        self.table_model.insertColumns(3, 4, QtCore.QModelIndex(), {'name': 'Критерій\n Вальда', 'values': vald.calc_result()}, {'name': 'Критерый\n Гульвіца', 'values': gulvic.calc_result()},
                 {'name': 'Критерій\n Лапласа', 'values': laplas.calc_result()}, {'name': 'Критерій\n Байеса-\nЛапласа', 'values': bayes_laplas.calc_result()})

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())