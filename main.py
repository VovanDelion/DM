import os
import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QListWidget, QDialog, QDateEdit, QFormLayout, QListWidgetItem,
                             QFileDialog, QDoubleSpinBox, QSpinBox, QTextEdit)
from PyQt6.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt6.QtCore import Qt, QDate


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123123123",
    "database": "mebelorg_db"
}

STYLESHEET = """
QWidget {
    background-color: #FFFFFF;
    font-family: Calibri;
    font-size: 14px;
    color: #333333;
}
QPushButton {
    background-color: #00FFFF;
    color: black;
    border: 1px solid #00CCCC;
    padding: 6px 12px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #00E5E5;
}
QPushButton#ActionButton {
    background-color: #0000FF;
    color: white;
    font-weight: bold;
}
QPushButton#ActionButton:hover {
    background-color: #0000DD;
}
QPushButton#DeleteButton {
    background-color: #FF4D4D;
    color: white;
}
QLineEdit, QComboBox, QDateEdit, QTextEdit, QDoubleSpinBox, QSpinBox {
    border: 1px solid #CCCCCC;
    padding: 5px;
    border-radius: 4px;
    background-color: #FFFFFF;
}
QTableWidget, QListWidget {
    gridline-color: #E0E0E0;
    border: 1px solid #CCCCCC;
}
QHeaderView::section {
    background-color: #00FFFF;
    padding: 4px;
    border: 1px solid #CCCCCC;
    font-weight: bold;
}
"""


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ООО «МебельОрг» - Авторизация")
        self.resize(350, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Авторизация")
        title.setFont(QFont("Calibri", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)


        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин (Email)")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()

        self.guest_btn = QPushButton("Войти как Гость")
        self.guest_btn.clicked.connect(lambda: self.open_main_window("Гость"))
        btn_layout.addWidget(self.guest_btn)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setObjectName("ActionButton")
        self.login_btn.clicked.connect(self.authenticate)
        btn_layout.addWidget(self.login_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Внимание", "Заполните все поля!")
            return

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE Логин=%s AND Пароль=%s", (login, password))
            user = cursor.fetchone()
            db.close()

            if user:
                self.open_main_window(user['Роль_сотрудника'], user['ФИО'])
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось подключиться: {err}")

    def open_main_window(self, role, fio=""):
        self.main_win = ProductCatalogWindow(role, fio)
        self.main_win.show()
        self.close()


class ProductWidget(QWidget):
    """Кастомный виджет для отображения одного товара (Картинка | Текст | Скидка)"""

    def __init__(self, product_data):
        super().__init__()
        self.data = product_data
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(15)

        self.image_label = QLabel()
        self.image_label.setFixedSize(120, 120)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_name = self.data.get('Фото')
        photo_path = os.path.join("resources", photo_name) if photo_name else ""

        if photo_path and os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
        else:
            pixmap = QPixmap("picture.png")
            if pixmap.isNull():
                pixmap = QPixmap("resources/picture.png")

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(120, 120,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("Нет фото")
            self.image_label.setStyleSheet("border: 1px solid #CCCCCC; background-color: #EEEEEE; color: #000000;")

        main_layout.addWidget(self.image_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_lbl = QLabel(self.data['Наименование_товара'])
        name_font = QFont("Calibri", 13)
        name_font.setBold(True)
        name_lbl.setFont(name_font)
        name_lbl.setWordWrap(True)

        cat_lbl = QLabel(f"<b>Категория:</b> {self.data['Категория_товара']}")
        desc_lbl = QLabel(self.data['Описание_товара'])
        desc_lbl.setWordWrap(True)
        prod_lbl = QLabel(
            f"<b>Производитель:</b> {self.data['Производитель']} | <b>Поставщик:</b> {self.data['Поставщик']}")

        price = float(self.data['Цена'])
        discount = int(self.data['Действующая_скидка'] or 0)
        stock = int(self.data['Кол_во_на_складе'] or 0)
        unit = self.data['Единица_измерения']

        if discount > 0:
            new_price = price * (1 - discount / 100)
            price_text = (f"<b>Цена:</b> <font color='red'><s>{price:.2f}</s></font> "
                          f"<font color='black'><b>{new_price:.2f}</b> руб.</font> / {unit}")
        else:
            price_text = f"<b>Цена:</b> <font color='black'>{price:.2f} руб.</font> / {unit}"

        if stock == 0:
            stock_text = f"<font color='red'><b>0 (Нет на складе)</b></font>"
        else:
            stock_text = f"{stock}"

        stats_lbl = QLabel(f"{price_text} | <b>На складе:</b> {stock_text}")

        info_layout.addWidget(name_lbl)
        info_layout.addWidget(cat_lbl)
        info_layout.addWidget(desc_lbl)
        info_layout.addWidget(prod_lbl)
        info_layout.addWidget(stats_lbl)

        main_layout.addLayout(info_layout, stretch=1)

        discount_layout = QVBoxLayout()
        discount_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if discount > 0:
            discount_lbl = QLabel(f"Скидка\n{discount}%")
            discount_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            disc_font = QFont("Calibri", 12)
            disc_font.setBold(True)
            discount_lbl.setFont(disc_font)
            discount_lbl.setFixedSize(80, 50)

            if stock == 0:
                discount_lbl.setStyleSheet(
                    "background-color: #CCCCCC; color: #555555; border: 1px solid #999999; border-radius: 8px;")
            elif discount > 15:
                discount_lbl.setStyleSheet(
                    "background-color: transparent; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 8px;")
            else:
                discount_lbl.setStyleSheet(
                    "background-color: #00FFFF; color: #000000; border: 1px solid #0000FF; border-radius: 8px;")

            discount_layout.addWidget(discount_lbl)
        else:
            empty_spacer = QWidget()
            empty_spacer.setFixedWidth(80)
            discount_layout.addWidget(empty_spacer)

        main_layout.addLayout(discount_layout)
        self.setLayout(main_layout)

        self.setObjectName("ProductCard")

        if stock == 0:
            self.setStyleSheet("""
                #ProductCard { background-color: #E5E5E5; border-radius: 5px; }
                QLabel { background-color: transparent; color: #555555; }
            """)
            desc_lbl.setStyleSheet("background-color: transparent; color: #777777; font-style: italic;")
        elif discount > 15:
            self.setStyleSheet("""
                #ProductCard { background-color: #008080; border-radius: 5px; }
                QLabel { background-color: transparent; color: #FFFFFF; }
            """)
            desc_lbl.setStyleSheet("background-color: transparent; color: #E0E0E0; font-style: italic;")
        else:
            self.setStyleSheet("""
                #ProductCard { background-color: #FFFFFF; }
                QLabel { background-color: transparent; color: #000000; }
            """)
            desc_lbl.setStyleSheet("background-color: transparent; color: #555555; font-style: italic;")


class ProductCatalogWindow(QWidget):
    """Основное окно каталога товаров со всеми фильтрами, поиском и сортировкой"""

    def __init__(self, user_role="Гость", user_fio=""):
        super().__init__()
        self.role = user_role
        self.fio = user_fio
        self.setWindowTitle("ООО «МебельОрг» - Каталог товаров")
        self.resize(1100, 750)

        self.initUI()
        self.load_manufacturers()
        self.load_products()

    def initUI(self):
        layout = QVBoxLayout()

        # Верхняя панель
        top_panel = QHBoxLayout()
        self.logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join("resources", "icon.png"))
        if logo_pixmap.isNull():
            logo_pixmap = QPixmap("icon.png")

        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaledToHeight(50, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled_logo)
        else:
            self.logo_label.setText("[ Логотип ]")
            self.logo_label.setStyleSheet("color: #00CCCC; font-weight: bold;")

        top_panel.addWidget(self.logo_label)
        top_panel.addSpacing(10)

        user_info = f"Вы вошли как: <b>{self.role}</b>"
        if self.fio:
            user_info += f" ({self.fio})"

        user_lbl = QLabel(user_info)
        top_panel.addWidget(user_lbl)
        top_panel.addStretch()

        self.orders_btn = QPushButton("Заказы")
        self.orders_btn.setObjectName("MainButton")
        self.orders_btn.clicked.connect(self.open_orders)
        top_panel.addWidget(self.orders_btn)


        if self.role in ["Гость", "Авторизированный клиент"]:
            self.orders_btn.hide()

        logout_btn = QPushButton("Сменить пользователя")
        logout_btn.setObjectName("SecondaryButton")
        logout_btn.clicked.connect(self.logout)
        top_panel.addWidget(logout_btn)

        layout.addLayout(top_panel)

        # Панель фильтрации и поиска
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        search_lbl = QLabel("Поиск:")
        controls_layout.addWidget(search_lbl)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите название или описание для поиска...")
        self.search_input.textChanged.connect(self.load_products)
        controls_layout.addWidget(self.search_input, stretch=2)

        sort_lbl = QLabel("Сортировка:")
        controls_layout.addWidget(sort_lbl)
        self.sort_combobox = QComboBox()

        self.sort_combobox.addItems([
            "Без сортировки",
            "Цена (по возрастанию)",
            "Цена (по убыванию)",
            "Остаток на складе (по возрастанию)",
            "Остаток на складе (по убыванию)"
        ])
        self.sort_combobox.currentIndexChanged.connect(self.load_products)
        controls_layout.addWidget(self.sort_combobox, stretch=1)

        filter_lbl = QLabel("Производитель:")
        controls_layout.addWidget(filter_lbl)
        self.filter_combobox = QComboBox()
        self.filter_combobox.addItem("Все производители")
        self.filter_combobox.currentIndexChanged.connect(self.load_products)
        controls_layout.addWidget(self.filter_combobox, stretch=1)

        discount_lbl = QLabel("Скидка:")
        controls_layout.addWidget(discount_lbl)
        self.discount_combobox = QComboBox()
        self.discount_combobox.addItems([
            "Все диапазоны",
            "0-10.99%",
            "11-14.99%",
            "15% и более"
        ])
        self.discount_combobox.currentIndexChanged.connect(self.load_products)
        controls_layout.addWidget(self.discount_combobox, stretch=1)

        # Скрытие поиска и фильтрации для гостей и обычных пользователей
        if self.role in ["Менеджер", "Администратор"]:
            layout.addLayout(controls_layout)

        # Счетчик количества товаров
        self.count_lbl = QLabel("Выведено элементов: 0 из 0")
        self.count_lbl.setStyleSheet("font-weight: bold; color: #555555; margin-top: 5px; margin-bottom: 5px;")
        layout.addWidget(self.count_lbl)

        # Главный список товаров
        self.products_list = QListWidget()
        self.products_list.setStyleSheet("""
                    QListWidget::item { border-bottom: 1px solid #CCCCCC; padding: 0px; }
                    QListWidget::item:selected { background-color: #00FFFF; color: black; }
                """)
        layout.addWidget(self.products_list)

        # Если Администратор — подключаем переход к редактированию
        if self.role == "Администратор":
            self.products_list.itemClicked.connect(self.edit_product_from_list)

            admin_btn_layout = QHBoxLayout()
            self.add_product_btn = QPushButton("Добавить товар")
            self.add_product_btn.setObjectName("ActionButton")
            self.add_product_btn.clicked.connect(self.add_product)
            admin_btn_layout.addWidget(self.add_product_btn)

            layout.addLayout(admin_btn_layout)

        self.setLayout(layout)

    def load_manufacturers(self):
        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()
            cursor.execute(
                "SELECT DISTINCT Производитель FROM Products WHERE Производитель IS NOT NULL AND Производитель != ''")
            rows = cursor.fetchall()
            db.close()
            for row in rows:
                self.filter_combobox.addItem(str(row[0]))
        except Exception as e:
            print(f"Ошибка при заполнении списка производителей: {e}")

    def load_products(self):
        self.products_list.clear()
        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) as total FROM Products")
            total_count = cursor.fetchone()['total']

            base_query = """
                SELECT Артикул, Наименование_товара, Единица_измерения, Цена, 
                       Поставщик, Производитель, Категория_товара, 
                       Действующая_скидка, Кол_во_на_складе, Описание_товара, Фото 
                FROM Products WHERE 1=1
            """
            query_params = []

            if self.search_input.isVisible():
                search_text = self.search_input.text().strip()
                if search_text:
                    base_query += " AND (Наименование_товара LIKE %s OR Описание_товара LIKE %s)"
                    query_params.extend([f"%{search_text}%", f"%{search_text}%"])

            if self.filter_combobox.isVisible():
                selected_manuf = self.filter_combobox.currentText()
                if selected_manuf != "Все производители":
                    base_query += " AND Производитель = %s"
                    query_params.append(selected_manuf)


            if self.discount_combobox.isVisible():
                discount_index = self.discount_combobox.currentIndex()
                if discount_index == 1:  # 0-10.99%
                    base_query += " AND Действующая_скидка >= 0 AND Действующая_скидка <= 10.99"
                elif discount_index == 2:  # 11-14.99%
                    base_query += " AND Действующая_скидка >= 11 AND Действующая_скидка <= 14.99"
                elif discount_index == 3:  # 15% и более
                    base_query += " AND Действующая_скидка >= 15"

            sort_index = self.sort_combobox.currentIndex()
            if sort_index == 1:
                base_query += " ORDER BY Цена ASC"
            elif sort_index == 2:
                base_query += " ORDER BY Цена DESC"
            elif sort_index == 3:
                base_query += " ORDER BY Кол_во_на_складе ASC"
            elif sort_index == 4:
                base_query += " ORDER BY Кол_во_на_складе DESC"

            cursor.execute(base_query, query_params)
            products = cursor.fetchall()
            db.close()

            current_count = len(products)
            self.count_lbl.setText(f"Выведено элементов: {current_count} из {total_count}")

            for prod in products:
                item = QListWidgetItem(self.products_list)
                row_widget = ProductWidget(prod)
                item.setSizeHint(row_widget.sizeHint())
                self.products_list.addItem(item)
                self.products_list.setItemWidget(item, row_widget)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось обновить каталог: {err}")

    def add_product(self):
        dialog = ProductEditDialog(None, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()

    def edit_product_from_list(self, item):
        widget = self.products_list.itemWidget(item)
        if widget and hasattr(widget, 'data'):
            dialog = ProductEditDialog(widget.data, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_products()

    def open_orders(self):
        if self.role in ["Гость", "Пользователь"]:
            QMessageBox.warning(self, "Отказ в доступе", "Просмотр заказов недоступен для вашей роли.")
            return
        self.orders_window = OrdersWindow(self.role)
        self.orders_window.show()

    def logout(self):
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()


class ProductEditDialog(QDialog):
    """Окно для добавления и редактирования товара администратором"""

    def __init__(self, product_data=None, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setWindowTitle(
            "Добавление товара" if not product_data else f"Редактирование товара (Артикул: {product_data['Артикул']})")
        self.resize(450, 580)
        self.new_photo_path = None
        self.initUI()
        self.load_dropdown_data()

        if self.product_data:
            self.fill_fields()
        else:
            self.set_placeholder_image()

    def initUI(self):
        form = QFormLayout()
        form.setSpacing(10)

        if self.product_data:
            self.id_input = QLineEdit(str(self.product_data['Артикул']))
            self.id_input.setEnabled(False)
            form.addRow("Артикул (ID):", self.id_input)

        self.name_input = QLineEdit()
        form.addRow("Наименование товара *:", self.name_input)

        self.category_combobox = QComboBox()
        self.category_combobox.setEditable(True)
        form.addRow("Категория товара *:", self.category_combobox)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        form.addRow("Описание товара:", self.desc_input)

        self.manufacturer_combobox = QComboBox()
        self.manufacturer_combobox.setEditable(True)
        form.addRow("Производитель *:", self.manufacturer_combobox)

        self.supplier_combobox = QComboBox()
        self.supplier_combobox.setEditable(True)
        form.addRow("Поставщик *:", self.supplier_combobox)

        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.0, 9999999.99)
        self.price_spin.setDecimals(2)
        form.addRow("Цена (руб.) *:", self.price_spin)

        self.unit_input = QLineEdit()
        form.addRow("Единица измерения *:", self.unit_input)

        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 999999)
        form.addRow("Кол-во на складе *:", self.stock_spin)

        self.discount_spin = QSpinBox()
        self.discount_spin.setRange(0, 100)
        form.addRow("Действующая скидка (%):", self.discount_spin)

        photo_layout = QHBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 100)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px solid #CCCCCC; background-color: #FAFAFA;")

        self.choose_photo_btn = QPushButton("Выбрать фото")
        self.choose_photo_btn.clicked.connect(self.choose_photo)

        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.choose_photo_btn)
        form.addRow("Изображение товара:", photo_layout)

        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setObjectName("ActionButton")
        self.save_btn.clicked.connect(self.save_data)
        btn_layout.addWidget(self.save_btn)

        if self.product_data:
            self.delete_btn = QPushButton("Удалить товар")
            self.delete_btn.setObjectName("DeleteButton")
            self.delete_btn.clicked.connect(self.delete_data)
            btn_layout.addWidget(self.delete_btn)

        form.addRow(btn_layout)
        self.setLayout(form)

    def set_placeholder_image(self):
        pixmap = QPixmap("picture.png")
        if pixmap.isNull():
            pixmap = QPixmap("resources/picture.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.photo_label.setPixmap(scaled)
        else:
            self.photo_label.setText("Нет фото")

    def load_dropdown_data(self):
        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()

            cursor.execute("SELECT DISTINCT Категория_товара FROM Products WHERE Категория_товара IS NOT NULL")
            for r in cursor.fetchall():
                if r[0]: self.category_combobox.addItem(str(r[0]))

            cursor.execute("SELECT DISTINCT Производитель FROM Products WHERE Производитель IS NOT NULL")
            for r in cursor.fetchall():
                if r[0]: self.manufacturer_combobox.addItem(str(r[0]))

            cursor.execute("SELECT DISTINCT Поставщик FROM Products WHERE Поставщик IS NOT NULL")
            for r in cursor.fetchall():
                if r[0]: self.supplier_combobox.addItem(str(r[0]))

            db.close()
        except Exception as e:
            print(f"Ошибка загрузки справочников: {e}")

    def fill_fields(self):
        self.name_input.setText(self.product_data['Наименование_товара'])
        self.category_combobox.setCurrentText(self.product_data['Категория_товара'])
        self.desc_input.setText(self.product_data['Описание_товара'])
        self.manufacturer_combobox.setCurrentText(self.product_data['Производитель'])
        self.supplier_combobox.setCurrentText(self.product_data['Поставщик'])
        self.price_spin.setValue(float(self.product_data['Цена']))
        self.unit_input.setText(self.product_data['Единица_измерения'])
        self.stock_spin.setValue(int(self.product_data['Кол_во_на_складе'] or 0))
        self.discount_spin.setValue(int(self.product_data['Действующая_скидка'] or 0))

        photo_name = self.product_data.get('Фото')
        photo_path = os.path.join("resources", photo_name) if photo_name else ""
        if photo_path and os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                self.photo_label.setPixmap(scaled)
            else:
                self.set_placeholder_image()
        else:
            self.set_placeholder_image()

    def choose_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.new_photo_path = file_path
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                self.photo_label.setPixmap(scaled)

    def save_data(self):
        name = self.name_input.text().strip()
        category = self.category_combobox.currentText().strip()
        desc = self.desc_input.toPlainText().strip()
        manufacturer = self.manufacturer_combobox.currentText().strip()
        supplier = self.supplier_combobox.currentText().strip()
        price = self.price_spin.value()
        unit = self.unit_input.text().strip()
        stock = self.stock_spin.value()
        discount = self.discount_spin.value()

        if not name or not category or not manufacturer or not supplier or not unit:
            QMessageBox.warning(self, "Внимание", "Заполните все обязательные поля, отмеченные звездочкой (*)!")
            return

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()

            if not self.product_data:
                cursor.execute("SELECT Артикул FROM Products")
                rows = cursor.fetchall()
                max_id = 0
                for r in rows:
                    try:
                        val = int(r[0])
                        if val > max_id: max_id = val
                    except ValueError:
                        pass
                artikul = str(max_id + 1)
            else:
                artikul = self.product_data['Артикул']

            photo_filename = self.product_data['Фото'] if self.product_data else ""

            if self.new_photo_path:
                os.makedirs("resources", exist_ok=True)

                if self.product_data and self.product_data.get('Фото'):
                    old_path = os.path.join("resources", self.product_data['Фото'])
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except Exception as e:
                            print(f"Не удалось удалить старое фото: {e}")

                pixmap = QPixmap(self.new_photo_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                    ext = os.path.splitext(self.new_photo_path)[1] or ".png"
                    photo_filename = f"{artikul}{ext}"
                    target_path = os.path.join("resources", photo_filename)
                    scaled_pixmap.save(target_path)

            if not self.product_data:
                query = """
                    INSERT INTO Products (Артикул, Наименование_товара, Категория_товара, Описание_товара, 
                                         Производитель, Поставщик, Цена, Единица_измерения, 
                                         Кол_во_на_складе, Действующая_скидка, Фото)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    artikul, name, category, desc, manufacturer, supplier, price, unit, stock, discount,
                    photo_filename))
            else:
                query = """
                    UPDATE Products SET Наименование_товара=%s, Категория_товара=%s, Описание_товара=%s,
                                        Производитель=%s, Поставщик=%s, Цена=%s, Единица_измерения=%s,
                                        Кол_во_на_складе=%s, Действующая_скидка=%s, Фото=%s
                    WHERE Артикул=%s
                """
                cursor.execute(query, (
                    name, category, desc, manufacturer, supplier, price, unit, stock, discount, photo_filename,
                    artikul))

            db.commit()
            db.close()
            QMessageBox.information(self, "Успех", "Товар успешно сохранен!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", f"Ошибка БД: {e}")

    def delete_data(self):
        if not self.product_data:
            return

        artikul = str(self.product_data['Артикул']).strip()

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()

            cursor.execute("SELECT Артикул_заказа FROM Orders")
            rows = cursor.fetchall()

            in_order = False
            for row in rows:
                if row[0]:
                    order_articles = [a.strip() for a in str(row[0]).replace(',', ' ').split()]
                    if artikul in order_articles:
                        in_order = True
                        break

            if in_order:
                QMessageBox.warning(self, "Ошибка удаления", "Товар, который присутствует в заказе, удалить нельзя!")
                db.close()
                return

            confirm = QMessageBox.question(self, "Удаление",
                                           f"Вы уверены, что хотите удалить товар '{self.product_data['Наименование_товара']}'?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                if self.product_data.get('Фото'):
                    old_path = os.path.join("resources", self.product_data['Фото'])
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except Exception as e:
                            print(f"Не удалось удалить файл изображения: {e}")

                cursor.execute("DELETE FROM Products WHERE Артикул = %s", (artikul,))
                db.commit()
                QMessageBox.information(self, "Успех", "Товар успешно удален.")
                db.close()
                self.accept()
            else:
                db.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении товара: {e}")


class OrderWidget(QWidget):
    """Кастомный виджет отображения заказа"""

    def __init__(self, order_data):
        super().__init__()
        self.data = order_data
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        left_frame = QWidget()
        left_frame.setStyleSheet("border: 1px solid #777777; background-color: #FFFFFF; border-radius: 4px;")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(12, 10, 12, 10)
        left_layout.setSpacing(6)

        art_lbl = QLabel(f"<b>Артикул заказа:</b> {self.data['Артикул_заказа']}")
        art_lbl.setStyleSheet("border: none; font-size: 14px; color: #000000;")

        status_lbl = QLabel(f"Статус заказа: {self.data['Статус_заказа']}")
        status_lbl.setStyleSheet("border: none;")

        addr = self.data.get('Адрес') or 'Не указан'
        addr_lbl = QLabel(f"Адрес пункта выдачи: {addr}")
        addr_lbl.setWordWrap(True)
        addr_lbl.setStyleSheet("border: none;")

        date_o = str(self.data['Дата_заказа'])
        date_o_lbl = QLabel(f"Дата заказа: {date_o}")
        date_o_lbl.setStyleSheet("border: none;")

        left_layout.addWidget(art_lbl)
        left_layout.addWidget(status_lbl)
        left_layout.addWidget(addr_lbl)
        left_layout.addWidget(date_o_lbl)

        main_layout.addWidget(left_frame, stretch=1)

        right_frame = QWidget()
        right_frame.setFixedSize(140, 105)
        right_frame.setStyleSheet("border: 2px solid #000000; background-color: #FAFAFA; border-radius: 4px;")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_d = str(self.data['Дата_доставки'])
        delivery_lbl = QLabel(f"Дата доставки:\n{date_d}")
        delivery_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delivery_lbl.setStyleSheet("border: none; font-size: 13px; color: #000000;")

        right_layout.addWidget(delivery_lbl)
        main_layout.addWidget(right_frame)

        self.setLayout(main_layout)
        self.setObjectName("OrderCard")
        self.setStyleSheet("#OrderCard { border: 1px solid #333333; border-radius: 6px; background-color: #FFFFFF; }")


class OrdersWindow(QWidget):
    """Окно управления заказами, переведенное на структуру списка по макету"""

    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle("Управление заказами - ООО «МебельОрг»")
        self.resize(950, 650)
        self.initUI()
        self.load_orders()

    def initUI(self):
        layout = QVBoxLayout()

        self.orders_list = QListWidget()
        self.orders_list.setStyleSheet("""
            QListWidget::item { border: none; padding: 4px; }
            QListWidget::item:selected { background-color: #00FFFF; }
        """)
        layout.addWidget(self.orders_list)

        btn_layout = QHBoxLayout()

        if self.role == "Администратор":
            self.add_btn = QPushButton("Добавить заказ")
            self.add_btn.setObjectName("ActionButton")
            self.add_btn.clicked.connect(lambda: self.open_order_dialog())

            self.edit_btn = QPushButton("Редактировать заказ")
            self.edit_btn.clicked.connect(self.edit_selected_order)

            self.del_btn = QPushButton("Удалить заказ")
            self.del_btn.setObjectName("DeleteButton")
            self.del_btn.clicked.connect(self.delete_order)

            btn_layout.addWidget(self.add_btn)
            btn_layout.addWidget(self.edit_btn)
            btn_layout.addWidget(self.del_btn)
        else:
            lbl = QLabel("Примечание: Редактирование заказов доступно только Администратору.")
            btn_layout.addWidget(lbl)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_orders(self):
        self.orders_list.clear()
        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT o.*, p.Адрес FROM Orders o
                LEFT JOIN PickupPoints p ON o.Пункт_выдачи_id = p.id
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            db.close()

            for order in orders:
                item = QListWidgetItem(self.orders_list)
                row_widget = OrderWidget(order)
                item.setSizeHint(row_widget.sizeHint())
                self.orders_list.addItem(item)
                self.orders_list.setItemWidget(item, row_widget)

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы: {err}")

    def open_order_dialog(self, order_data=None):
        dialog = OrderEditDialog(order_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_orders()

    def edit_selected_order(self):
        selected_item = self.orders_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Внимание", "Выберите заказ из списка для редактирования!")
            return

        widget = self.orders_list.itemWidget(selected_item)
        if widget and hasattr(widget, 'data'):
            order_id = widget.data['Номер_заказа']

            try:
                db = mysql.connector.connect(**DB_CONFIG)
                cursor = db.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Orders WHERE Номер_заказа = %s", (order_id,))
                order_data = cursor.fetchone()
                db.close()

                if order_data:
                    self.open_order_dialog(order_data)
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Ошибка", f"Ошибка получения данных: {err}")

    def delete_order(self):
        selected_item = self.orders_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Внимание", "Выберите заказ для удаления!")
            return

        widget = self.orders_list.itemWidget(selected_item)
        if widget and hasattr(widget, 'data'):
            order_id = widget.data['Номер_заказа']

            confirm = QMessageBox.question(self, "Удаление", f"Вы уверены, что хотите удалить заказ №{order_id}?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    db = mysql.connector.connect(**DB_CONFIG)
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM Orders WHERE Номер_заказа = %s", (order_id,))
                    db.commit()
                    db.close()
                    self.load_orders()
                    QMessageBox.information(self, "Успех", "Заказ успешно удален.")
                except mysql.connector.Error as err:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {err}")


class OrderEditDialog(QDialog):
    def __init__(self, order_data=None):
        super().__init__()
        self.order_data = order_data
        self.setWindowTitle(
            "Добавление заказа" if not order_data else f"Редактирование заказа №{order_data['Номер_заказа']}")
        self.resize(400, 350)
        self.pickup_points = {}
        self.initUI()
        self.load_pickup_points()

        if self.order_data:
            self.fill_fields()

    def initUI(self):
        form = QFormLayout()

        self.id_input = QLineEdit()
        if self.order_data:
            self.id_input.setEnabled(False)
        form.addRow("Номер заказа:", self.id_input)

        self.article_input = QLineEdit()
        form.addRow("Артикул(ы) заказа:", self.article_input)

        self.status_combobox = QComboBox()
        self.status_combobox.addItems(["Новый", "Завершен", "В пути", "Ожидает получения"])
        form.addRow("Статус заказа:", self.status_combobox)

        self.pickup_combobox = QComboBox()
        form.addRow("Пункт выдачи:", self.pickup_combobox)

        self.date_order = QDateEdit(QDate.currentDate())
        self.date_order.setCalendarPopup(True)
        form.addRow("Дата заказа:", self.date_order)

        self.date_delivery = QDateEdit(QDate.currentDate().addDays(3))
        self.date_delivery.setCalendarPopup(True)
        form.addRow("Дата доставки:", self.date_delivery)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setObjectName("ActionButton")
        self.save_btn.clicked.connect(self.save_data)
        form.addRow(self.save_btn)

        self.setLayout(form)

    def load_pickup_points(self):
        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT id, Адрес FROM PickupPoints")
            rows = cursor.fetchall()
            db.close()

            for row in rows:
                self.pickup_combobox.addItem(row['Адрес'])
                self.pickup_points[row['Адрес']] = row['id']
        except mysql.connector.Error as err:
            print(f"Ошибка загрузки пунктов выдачи: {err}")

    def fill_fields(self):
        self.id_input.setText(str(self.order_data['Номер_заказа']))
        self.article_input.setText(self.order_data['Артикул_заказа'])
        self.status_combobox.setCurrentText(self.order_data['Статус_заказа'])

        if self.order_data['Дата_заказа']:
            self.date_order.setDate(QDate.fromString(str(self.order_data['Дата_заказа']), "yyyy-MM-dd"))
        if self.order_data['Дата_доставки']:
            self.date_delivery.setDate(QDate.fromString(str(self.order_data['Дата_доставки']), "yyyy-MM-dd"))

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()
            cursor.execute("SELECT Адрес FROM PickupPoints WHERE id = %s", (self.order_data['Пункт_выдачи_id'],))
            addr = cursor.fetchone()
            db.close()
            if addr:
                self.pickup_combobox.setCurrentText(addr[0])
        except:
            pass

    def save_data(self):
        order_id = self.id_input.text().strip()
        articles = self.article_input.text().strip()
        status = self.status_combobox.currentText()
        pickup_address = self.pickup_combobox.currentText()
        pickup_id = self.pickup_points.get(pickup_address)
        d_order = self.date_order.date().toString("yyyy-MM-dd")
        d_delivery = self.date_delivery.date().toString("yyyy-MM-dd")

        if not order_id or not articles:
            QMessageBox.warning(self, "Внимание", "Заполните номер и артикул заказа!")
            return

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()

            if not self.order_data:
                query = """
                    INSERT INTO Orders (Номер_заказа, Артикул_заказа, Статус_заказа, Пункт_выдачи_id, Дата_заказа, Дата_доставки)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (order_id, articles, status, pickup_id, d_order, d_delivery))
            else:
                query = """
                    UPDATE Orders SET Артикул_заказа=%s, Статус_заказа=%s, Пункт_выдачи_id=%s, Дата_заказа=%s, Дата_доставки=%s
                    WHERE Номер_заказа=%s
                """
                cursor.execute(query, (articles, status, pickup_id, d_order, d_delivery, order_id))

            db.commit()
            db.close()
            QMessageBox.information(self, "Успех", "Данные сохранены успешно!")
            self.accept()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка сохранения", f"Ошибка базы данных: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    icon_target = os.path.join("resources", "icon.png")
    if not os.path.exists(icon_target):
        icon_target = os.path.join("resources", "icon.png")

    if os.path.exists(icon_target):
        app.setWindowIcon(QIcon(icon_target))
    elif os.path.exists("icon.png"):
        app.setWindowIcon(QIcon("icon.png"))

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

#
# pyinstaller --noconfirm --windowed --onefile --name MebelOrgApp --icon resources\icon.png --add-data "resources;resources" --collect-all mysql.connector main.py
#