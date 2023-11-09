from DB import examples


from PyQt5.QtWidgets import QApplication
from views import MainWindow
import sys

if __name__ == '__main__':
    examples.run()

    app = QApplication(sys.argv)
    main_view = MainWindow.MainWindow()

    sys.exit(app.exec_())

