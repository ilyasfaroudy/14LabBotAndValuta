import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
    from reportlab.pdfgen import canvas

    class CurrencyConverter(QWidget):
        def init(self):
            super().init()
            self.init_ui()
        def init_ui(self):
            self.layout = QVBoxLayout()

            self.label_usd = QLabel("Enter amount in USD:")
            self.layout.addWidget(self.label_usd)

            self.input_usd = QLineEdit()
            self.layout.addWidget(self.input_usd)

            self.label_currency = QLabel("Select currency to convert to:")
            self.layout.addWidget(self.label_currency)

            self.currency_combobox = QComboBox()
            self.currency_combobox.addItems(["Euro", "GBP", "JPY"])
            self.layout.addWidget(self.currency_combobox)

            self.button_convert = QPushButton("Convert")
            self.button_convert.clicked.connect(self.convert_currency)
            self.layout.addWidget(self.button_convert)

            self.setLayout(self.layout)
            self.setWindowTitle("Currency Converter")
        def convert_currency(self):
            try:
                usd_amount = float(self.input_usd.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter a valid number.")
                return
            selected_currency = self.currency_combobox.currentText()
            if selected_currency == "Euro":
                converted_amount = usd_amount * 0.85
            elif selected_currency == "GBP":
                converted_amount = usd_amount * 12
            elif selected_currency == "JPY":
                converted_amount = usd_amount * 110.17

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Conversion Result")
            msg_box.setText(f"USD: {usd_amount}\n{selected_currency}: {converted_amount}")
            msg_box.setStyleSheet("QLabel{min-width: 200px;}")
            msg_box.exec_()
            c = canvas.Canvas("converted_currency.pdf")
            c.drawString(100, 800, f"USD: {usd_amount}")
            c.drawString(100, 780, f"{selected_currency}: {converted_amount}")
            c.save()
    if name == 'main':
        app = QApplication(sys.argv)
        converter = CurrencyConverter()
        converter.show()
        sys.exit(app.exec_())
