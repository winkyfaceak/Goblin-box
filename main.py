import os
import sys

import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()
from PyQt6.QtWidgets import QApplication
from ui.core import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
