from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout
)


class ShopTable(QMainWindow):
    def __init__(
            self,
            trade_data: list[dict],
            shop_data: list[dict],
            product_data: list[dict]
    ):
        super().__init__()

        self.trade_data = trade_data
        self.shop_data = shop_data
        self.product_data = product_data

        self.setWindowTitle('Shop table')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.table_widget = QTableWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.table_widget)

        self.table_widget.setRowCount(len(self.trade_data))
        self.table_widget.setColumnCount(len(self.trade_data[0]))

        headers = list(self.trade_data[0].keys())
        self.table_widget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(self.trade_data):
            for col_idx, key in enumerate(headers):
                item = QTableWidgetItem(str(row_data[key]))
                self.table_widget.setItem(row_idx, col_idx, item)

        self.table_widget.resizeColumnsToContents()

        self.button = QPushButton('Calculate', self)
        self.label = QLabel('Result will be shown here...', self)

        self.button.clicked.connect(self.perform_action)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button)
        button_layout.addWidget(self.label)

        self.central_layout.addLayout(button_layout)

    def perform_action(self) -> None:
        product_coffe_ids = [
            product.get('Артикул', 0)
            for product in self.product_data
            if 'Кофе' in product.get('Наименование товара', '')
        ]
        october_shop_ids = [
            shop.get('ID магазина')
            for shop in self.shop_data
            if 'Октябрьский' in shop.get('Район', '')
        ]

        trade_total_revenue = [
            trade.get('Количество упаковок шт', 0) * trade.get('Цена руб за шт', 0)
            for trade in self.trade_data
            if (
                    trade.get('ID магазина', -1) in october_shop_ids and
                    trade.get('Артикул', -1) in product_coffe_ids and
                    trade.get('Тип операции', '') == 'Продажа'
            )
        ]

        result = f"Total revenue from October district shops for the sale of coffee: {sum(trade_total_revenue)} rub."

        self.label.setText(result)
