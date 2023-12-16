import sys

from PyQt6.QtWidgets import QApplication

from db.db_worker import DBWorker
from qt.shop_table import ShopTable
from config import config


# Simple db connections
trade_db = DBWorker(config.TRADE_CSV_PATH)
shop_db = DBWorker(config.SHOP_CSV_PATH)
product_db = DBWorker(config.PRODUCT_CSV_PATH)


def main():
    app = QApplication(sys.argv)

    window = ShopTable(
        trade_data=trade_db.get_data(),
        shop_data=shop_db.get_data(),
        product_data=product_db.get_data(),
    )

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
