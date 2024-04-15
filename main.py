import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem

from ui_query_student import Ui_MainWindow


import DatabaseConnect


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        # 读取功能
        self.query_button.clicked.connect(self.query)

    # 查询学生信息
    def query(self):
        # 根据可视化中输入的条件构造 sql 语句并执行
        conn = DatabaseConnect.getConn()
        cur = conn.cursor()
        try:
            # 有输入的条件
            selected = ""
            # 是否有输入条件，如果没有，直接返回所有数据
            has_input = False
            # 是否是第一个条件
            is_first = True

            # 判断各个查询条件是否使用，若使用，则获取输入的值，并加入到 sql 语句中
            if self.id.isChecked():
                id = self.id_line.text()
                has_input = True
                if is_first:
                    selected += "s.id = '" + id + "'"
                    is_first = False
                else:
                    selected += " and s.id = '" + id + "'"
            if self.name.isChecked():
                name = self.name_line.text()
                has_input = True
                if is_first:
                    selected += "name = '" + name + "'"
                    is_first = False
                else:
                    selected += " and name = '" + name + "'"
            if self.age.isChecked():
                age_from = self.age_line_from.text()
                age_to = self.age_line_to.text()
                has_input = True
                if is_first:
                    selected += "age >= " + age_from + " and age <= " + age_to
                    is_first = False
                else:
                    selected += " and age >= " + age_from + " and age <= " + age_to
            if self.sex.isChecked():
                sex = self.sex_combo.currentText()
                has_input = True
                if is_first:
                    selected += "sex = '" + sex + "'"
                    is_first = False
                else:
                    selected += " and sex = '" + sex + "'"
            if self.Sclass.isChecked():
                Sclass = self.class_line.text()
                has_input = True
                if is_first:
                    selected += "class = '" + Sclass + "'"
                    is_first = False
                else:
                    selected += " and class = '" + Sclass + "'"
            if self.major.isChecked():
                major = self.major_line.text()
                has_input = True
                if is_first:
                    selected += "major = '" + major + "'"
                    is_first = False
                else:
                    selected += " and major = '" + major + "'"
            if self.address.isChecked():
                addr = self.address_line.text()
                has_input = True
                if is_first:
                    selected += "addr = '" + addr + "'"
                    is_first = False
                else:
                    selected += " and addr = '" + addr + "'"

            # 构造 sql 语句
            if has_input:
                sql = "select * from student s where " + selected + ";"
                print(sql)
            else:
                sql = "select * from student;"

            # 执行 sql 语句并获取结果
            cur.execute(sql)
            data = cur.fetchall()

            # 显示 sql 语句
            model = QStringListModel()
            model.setStringList([sql])
            self.sql.setModel(model)

            # 将执行结果显示在表格中
            self.result.setRowCount(len(data))
            self.result.setColumnCount(len(data[0]))
            self.result.setHorizontalHeaderLabels(['id', 'name', 'age', 'sex', 'class', 'major', 'addr'])
            for i, row in enumerate(data):
                for j, cell in enumerate(row):
                    item = QTableWidgetItem(str(cell))
                    self.result.setItem(i, j, item)
            # 自适应列宽
            self.result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Exception as e:
            print(e)

        finally:
            cur.close()
            conn.close()



if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec())
