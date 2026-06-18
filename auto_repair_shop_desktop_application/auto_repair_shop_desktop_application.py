import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QTabWidget, QComboBox, QDateEdit, QTextEdit,
                             QInputDialog)
from PyQt5.QtCore import Qt, QDate
import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('autocenter.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Пользователи
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            is_admin INTEGER DEFAULT 0
        )
        ''')

        # Автомобили на заказ
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            color TEXT,
            engine_volume REAL,
            transmission TEXT,
            mileage INTEGER,
            price REAL,
            delivery_path TEXT,
            status TEXT DEFAULT 'ordered',
            order_date TEXT,
            delivery_date TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Автозапчасти
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            brand TEXT NOT NULL,
            car_model TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            supplier TEXT,
            description TEXT
        )
        ''')

        # Ремонты
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'in_progress',
            total_cost REAL,
            user_id INTEGER,
            FOREIGN KEY (car_id) REFERENCES cars (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Состав ремонта (используемые запчасти)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repair_id INTEGER,
            part_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (repair_id) REFERENCES repairs (id),
            FOREIGN KEY (part_id) REFERENCES parts (id)
        )
        ''')

        self.conn.commit()

    def add_user(self, username, password, full_name, is_admin=False, phone=None, email=None):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, phone, email, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, full_name, phone, email, 1 if is_admin else 0))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT id, username, is_admin FROM users WHERE username=? AND password=?', 
                           (username, hashed_password))
        return self.cursor.fetchone()

    def get_user_info(self, user_id):
        self.cursor.execute('SELECT username, full_name, phone, email, is_admin FROM users WHERE id=?', (user_id,))
        return self.cursor.fetchone()

    def add_car(self, client_name, client_phone, brand, model, year, color, engine_volume, 
                transmission, mileage, price, delivery_path, order_date, user_id):
        self.cursor.execute('''
        INSERT INTO cars (client_name, client_phone, brand, model, year, color, engine_volume, 
                          transmission, mileage, price, delivery_path, order_date, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (client_name, client_phone, brand, model, year, color, engine_volume, 
              transmission, mileage, price, delivery_path, order_date, user_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_part(self, name, code, brand, car_model, price, quantity, supplier=None, description=None):
        try:
            self.cursor.execute('''
            INSERT INTO parts (name, code, brand, car_model, price, quantity, supplier, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, code, brand, car_model, price, quantity, supplier, description))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_repair(self, car_id, client_name, client_phone, start_date, description, user_id, end_date=None, status='in_progress'):
        self.cursor.execute('''
        INSERT INTO repairs (car_id, client_name, client_phone, start_date, end_date, description, status, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (car_id, client_name, client_phone, start_date, end_date, description, status, user_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_cars(self):
        self.cursor.execute('SELECT * FROM cars')
        return self.cursor.fetchall()

    def get_all_parts(self):
        self.cursor.execute('SELECT * FROM parts')
        return self.cursor.fetchall()

    def get_all_repairs(self):
        self.cursor.execute('SELECT * FROM repairs')
        return self.cursor.fetchall()

    def get_all_users(self):
        self.cursor.execute('SELECT id, username, full_name, phone, email, is_admin FROM users')
        return self.cursor.fetchall()

    def update_car_status(self, car_id, status):
        self.cursor.execute('UPDATE cars SET status=? WHERE id=?', (status, car_id))
        self.conn.commit()

    def update_part_quantity(self, part_id, quantity):
        self.cursor.execute('UPDATE parts SET quantity=? WHERE id=?', (quantity, part_id))
        self.conn.commit()

    def update_repair_status(self, repair_id, status, end_date=None, total_cost=None):
        if end_date and total_cost:
            self.cursor.execute('UPDATE repairs SET status=?, end_date=?, total_cost=? WHERE id=?', 
                               (status, end_date, total_cost, repair_id))
        elif end_date:
            self.cursor.execute('UPDATE repairs SET status=?, end_date=? WHERE id=?', 
                               (status, end_date, repair_id))
        else:
            self.cursor.execute('UPDATE repairs SET status=? WHERE id=?', (status, repair_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
        self.conn.commit()

    def delete_car(self, car_id):
        self.cursor.execute('DELETE FROM cars WHERE id=?', (car_id,))
        self.conn.commit()

    def delete_part(self, part_id):
        self.cursor.execute('DELETE FROM parts WHERE id=?', (part_id,))
        self.conn.commit()

    def delete_repair(self, repair_id):
        self.cursor.execute('DELETE FROM repairs WHERE id=?', (repair_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle('Автоцентр - Авторизация')
        self.setFixedSize(400, 300)
        
        # Применяем стили
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#register {
                background-color: #2196F3;
            }
            QPushButton#register:hover {
                background-color: #0b7dda;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Авторизация')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #333333; margin-bottom: 20px;')
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(20, 10, 20, 10)
        
        self.username_label = QLabel('Логин:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите ваш логин')
        
        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите ваш пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        
        button_layout = QHBoxLayout()
        self.login_button = QPushButton('Войти')
        self.login_button.setObjectName('login')
        self.register_button = QPushButton('Регистрация')
        self.register_button.setObjectName('register')
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        
        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.setContentsMargins(30, 20, 30, 30)
        
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.show_register)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль')
            return
        
        user = self.db.check_user(username, password)
        if user:
            user_id, username, is_admin = user
            self.main_window = MainWindow(self.db, user_id, is_admin)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
    
    def show_register(self):
        self.register_window = RegisterWindow(self.db)
        self.register_window.show()

class RegisterWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle('Регистрация')
        self.setFixedSize(450, 500)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Регистрация нового пользователя')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #333333; margin-bottom: 20px;')
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(30, 10, 30, 10)
        
        fields = [
            ('Логин:', QLineEdit(), 'username'),
            ('Пароль:', QLineEdit(), 'password'),
            ('Подтвердите пароль:', QLineEdit(), 'confirm_password'),
            ('ФИО:', QLineEdit(), 'full_name'),
            ('Телефон:', QLineEdit(), 'phone'),
            ('Email:', QLineEdit(), 'email')
        ]
        
        for label_text, input_widget, object_name in fields:
            label = QLabel(label_text)
            input_widget.setObjectName(object_name)
            if 'password' in object_name:
                input_widget.setEchoMode(QLineEdit.Password)
            form_layout.addWidget(label)
            form_layout.addWidget(input_widget)
        
        self.register_button = QPushButton('Зарегистрироваться')
        form_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        
        self.username_input = self.findChild(QLineEdit, 'username')
        self.password_input = self.findChild(QLineEdit, 'password')
        self.confirm_password_input = self.findChild(QLineEdit, 'confirm_password')
        self.full_name_input = self.findChild(QLineEdit, 'full_name')
        self.phone_input = self.findChild(QLineEdit, 'phone')
        self.email_input = self.findChild(QLineEdit, 'email')
        
        self.register_button.clicked.connect(self.register)
        
        self.setLayout(layout)
        
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        full_name = self.full_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        
        if not username or not password or not confirm_password or not full_name:
            QMessageBox.warning(self, 'Ошибка', 'Заполните обязательные поля (логин, пароль, ФИО)')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают')
            return
        
        success = self.db.add_user(username, password, full_name, False, phone, email)
        if success:
            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким логином уже существует')

class MainWindow(QMainWindow):
    def __init__(self, db, user_id, is_admin):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.is_admin = is_admin
        
        self.setWindowTitle('Автоцентр - Главное меню')
        self.setMinimumSize(1000, 700)
        
        # Основные стили для приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #333333;
            }
            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                background: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #dcdcdc;
                padding: 8px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #555555;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #333333;
            }
            QTabBar::tab:hover {
                background: #f0f0f0;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                selection-background-color: #e3f2fd;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: none;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
                min-height: 25px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#delete {
                background-color: #f44336;
            }
            QPushButton#delete:hover {
                background-color: #d32f2f;
            }
            QPushButton#logout {
                background-color: #607d8b;
            }
            QPushButton#logout:hover {
                background-color: #455a64;
            }
        """)
        
        self.init_ui()
        self.load_user_info()
    
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Панель пользователя
        user_panel = QWidget()
        user_panel.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 4px;
            padding: 10px;
            border: 1px solid #dcdcdc;
        """)
        user_layout = QHBoxLayout(user_panel)
        
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet('font-size: 14px; color: #333333;')
        
        self.logout_button = QPushButton('Выйти')
        self.logout_button.setObjectName('logout')
        self.logout_button.clicked.connect(self.logout)
        
        user_layout.addWidget(self.user_info_label, 1)
        user_layout.addWidget(self.logout_button)
        
        self.layout.addWidget(user_panel)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                margin-top: 10px;
            }
        """)
        
        # Вкладка автомобилей
        self.car_tab = QWidget()
        self.init_car_tab()
        self.tabs.addTab(self.car_tab, 'Автомобили')
        
        # Вкладка запчастей
        self.parts_tab = QWidget()
        self.init_parts_tab()
        self.tabs.addTab(self.parts_tab, 'Запчасти')
        
        # Вкладка ремонтов
        self.repairs_tab = QWidget()
        self.init_repairs_tab()
        self.tabs.addTab(self.repairs_tab, 'Ремонты')
        
        # Вкладка пользователей (только для админа)
        if self.is_admin:
            self.users_tab = QWidget()
            self.init_users_tab()
            self.tabs.addTab(self.users_tab, 'Пользователи')
        
        self.layout.addWidget(self.tabs)
        
        # Кнопка выхода
        self.logout_button = QPushButton('Выйти')
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)
    
    def init_car_tab(self):
        layout = QVBoxLayout()
        
        # Форма добавления автомобиля
        self.car_form = QWidget()
        form_layout = QVBoxLayout()
        
        self.car_client_name = QLineEdit()
        self.car_client_phone = QLineEdit()
        self.car_brand = QLineEdit()
        self.car_model = QLineEdit()
        self.car_year = QLineEdit()
        self.car_color = QLineEdit()
        self.car_engine_volume = QLineEdit()
        self.car_transmission = QComboBox()
        self.car_transmission.addItems(['Автомат', 'Механика', 'Робот', 'Вариатор'])
        self.car_mileage = QLineEdit()
        self.car_price = QLineEdit()
        self.car_delivery_path = QLineEdit()
        self.car_order_date = QDateEdit(QDate.currentDate())
        
        form_layout.addWidget(QLabel('Имя клиента:'))
        form_layout.addWidget(self.car_client_name)
        form_layout.addWidget(QLabel('Телефон клиента:'))
        form_layout.addWidget(self.car_client_phone)
        form_layout.addWidget(QLabel('Марка:'))
        form_layout.addWidget(self.car_brand)
        form_layout.addWidget(QLabel('Модель:'))
        form_layout.addWidget(self.car_model)
        form_layout.addWidget(QLabel('Год:'))
        form_layout.addWidget(self.car_year)
        form_layout.addWidget(QLabel('Цвет:'))
        form_layout.addWidget(self.car_color)
        form_layout.addWidget(QLabel('Объем двигателя:'))
        form_layout.addWidget(self.car_engine_volume)
        form_layout.addWidget(QLabel('Коробка передач:'))
        form_layout.addWidget(self.car_transmission)
        form_layout.addWidget(QLabel('Пробег:'))
        form_layout.addWidget(self.car_mileage)
        form_layout.addWidget(QLabel('Цена:'))
        form_layout.addWidget(self.car_price)
        form_layout.addWidget(QLabel('Путь доставки:'))
        form_layout.addWidget(self.car_delivery_path)
        form_layout.addWidget(QLabel('Дата заказа:'))
        form_layout.addWidget(self.car_order_date)
        
        self.add_car_button = QPushButton('Добавить автомобиль')
        self.add_car_button.clicked.connect(self.add_car)
        form_layout.addWidget(self.add_car_button)
        
        self.car_form.setLayout(form_layout)
        layout.addWidget(self.car_form)
        
        # Таблица автомобилей
        self.cars_table = QTableWidget()
        self.cars_table.setColumnCount(13)
        self.cars_table.setHorizontalHeaderLabels([
            'ID', 'Клиент', 'Телефон', 'Марка', 'Модель', 'Год', 'Цена', 
            'Статус', 'Дата заказа', 'Дата доставки', 'КПП', 'Пробег', 'Двигатель'
        ])
        self.cars_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cars_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Кнопки управления для автомобилей
        self.car_buttons = QWidget()
        buttons_layout = QHBoxLayout()
        
        self.update_car_status_button = QPushButton('Обновить статус')
        self.update_car_status_button.clicked.connect(self.update_car_status)
        buttons_layout.addWidget(self.update_car_status_button)
        
        if self.is_admin:
            self.delete_car_button = QPushButton('Удалить')
            self.delete_car_button.clicked.connect(self.delete_car)
            buttons_layout.addWidget(self.delete_car_button)
        
        self.car_buttons.setLayout(buttons_layout)
        
        layout.addWidget(self.cars_table)
        layout.addWidget(self.car_buttons)
        
        self.car_tab.setLayout(layout)
        self.update_cars_table()
    
    def init_parts_tab(self):
        layout = QVBoxLayout()
        
        # Форма добавления запчасти
        self.part_form = QWidget()
        form_layout = QVBoxLayout()
        
        self.part_name = QLineEdit()
        self.part_code = QLineEdit()
        self.part_brand = QLineEdit()
        self.part_car_model = QLineEdit()
        self.part_price = QLineEdit()
        self.part_quantity = QLineEdit()
        self.part_supplier = QLineEdit()
        self.part_description = QTextEdit()
        
        form_layout.addWidget(QLabel('Название:'))
        form_layout.addWidget(self.part_name)
        form_layout.addWidget(QLabel('Код:'))
        form_layout.addWidget(self.part_code)
        form_layout.addWidget(QLabel('Бренд:'))
        form_layout.addWidget(self.part_brand)
        form_layout.addWidget(QLabel('Модель авто:'))
        form_layout.addWidget(self.part_car_model)
        form_layout.addWidget(QLabel('Цена:'))
        form_layout.addWidget(self.part_price)
        form_layout.addWidget(QLabel('Количество:'))
        form_layout.addWidget(self.part_quantity)
        form_layout.addWidget(QLabel('Поставщик:'))
        form_layout.addWidget(self.part_supplier)
        form_layout.addWidget(QLabel('Описание:'))
        form_layout.addWidget(self.part_description)
        
        self.add_part_button = QPushButton('Добавить запчасть')
        self.add_part_button.clicked.connect(self.add_part)
        form_layout.addWidget(self.add_part_button)
        
        self.part_form.setLayout(form_layout)
        layout.addWidget(self.part_form)
        
        # Таблица запчастей
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(8)
        self.parts_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Код', 'Бренд', 'Модель', 'Цена', 'Количество', 'Поставщик'
        ])
        self.parts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.parts_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Кнопки управления для запчастей
        self.part_buttons = QWidget()
        buttons_layout = QHBoxLayout()
        
        self.update_part_quantity_button = QPushButton('Изменить количество')
        self.update_part_quantity_button.clicked.connect(self.update_part_quantity)
        buttons_layout.addWidget(self.update_part_quantity_button)
        
        if self.is_admin:
            self.delete_part_button = QPushButton('Удалить')
            self.delete_part_button.clicked.connect(self.delete_part)
            buttons_layout.addWidget(self.delete_part_button)
        
        self.part_buttons.setLayout(buttons_layout)
        
        layout.addWidget(self.parts_table)
        layout.addWidget(self.part_buttons)
        
        self.parts_tab.setLayout(layout)
        self.update_parts_table()
    
    def init_repairs_tab(self):
        layout = QVBoxLayout()
        
        # Форма добавления ремонта
        self.repair_form = QWidget()
        form_layout = QVBoxLayout()
        
        self.repair_car_id = QComboBox()
        self.update_car_combo()
        self.repair_client_name = QLineEdit()
        self.repair_client_phone = QLineEdit()
        self.repair_start_date = QDateEdit(QDate.currentDate())
        self.repair_description = QTextEdit()
        
        form_layout.addWidget(QLabel('Автомобиль (ID):'))
        form_layout.addWidget(self.repair_car_id)
        form_layout.addWidget(QLabel('Имя клиента:'))
        form_layout.addWidget(self.repair_client_name)
        form_layout.addWidget(QLabel('Телефон клиента:'))
        form_layout.addWidget(self.repair_client_phone)
        form_layout.addWidget(QLabel('Дата начала:'))
        form_layout.addWidget(self.repair_start_date)
        form_layout.addWidget(QLabel('Описание работ:'))
        form_layout.addWidget(self.repair_description)
        
        self.add_repair_button = QPushButton('Добавить ремонт')
        self.add_repair_button.clicked.connect(self.add_repair)
        form_layout.addWidget(self.add_repair_button)
        
        self.repair_form.setLayout(form_layout)
        layout.addWidget(self.repair_form)
        
        # Таблица ремонтов
        self.repairs_table = QTableWidget()
        self.repairs_table.setColumnCount(8)
        self.repairs_table.setHorizontalHeaderLabels([
            'ID', 'Автомобиль', 'Клиент', 'Телефон', 'Дата начала', 'Дата окончания', 'Статус', 'Стоимость'
        ])
        self.repairs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.repairs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Кнопки управления для ремонтов
        self.repair_buttons = QWidget()
        buttons_layout = QHBoxLayout()
        
        self.update_repair_status_button = QPushButton('Обновить статус')
        self.update_repair_status_button.clicked.connect(self.update_repair_status)
        buttons_layout.addWidget(self.update_repair_status_button)
        
        if self.is_admin:
            self.delete_repair_button = QPushButton('Удалить')
            self.delete_repair_button.clicked.connect(self.delete_repair)
            buttons_layout.addWidget(self.delete_repair_button)
        
        self.repair_buttons.setLayout(buttons_layout)
        
        layout.addWidget(self.repairs_table)
        layout.addWidget(self.repair_buttons)
        
        self.repairs_tab.setLayout(layout)
        self.update_repairs_table()
    
    def init_users_tab(self):
        layout = QVBoxLayout()
        
        # Форма добавления пользователя (только для админа)
        self.user_form = QWidget()
        form_layout = QVBoxLayout()
        
        self.new_username = QLineEdit()
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_full_name = QLineEdit()
        self.new_phone = QLineEdit()
        self.new_email = QLineEdit()
        self.new_is_admin = QComboBox()
        self.new_is_admin.addItems(['Обычный пользователь', 'Администратор'])
        
        form_layout.addWidget(QLabel('Логин:'))
        form_layout.addWidget(self.new_username)
        form_layout.addWidget(QLabel('Пароль:'))
        form_layout.addWidget(self.new_password)
        form_layout.addWidget(QLabel('ФИО:'))
        form_layout.addWidget(self.new_full_name)
        form_layout.addWidget(QLabel('Телефон:'))
        form_layout.addWidget(self.new_phone)
        form_layout.addWidget(QLabel('Email:'))
        form_layout.addWidget(self.new_email)
        form_layout.addWidget(QLabel('Роль:'))
        form_layout.addWidget(self.new_is_admin)
        
        self.add_user_button = QPushButton('Добавить пользователя')
        self.add_user_button.clicked.connect(self.add_user)
        form_layout.addWidget(self.add_user_button)
        
        self.user_form.setLayout(form_layout)
        layout.addWidget(self.user_form)
        
        # Таблица пользователей
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            'ID', 'Логин', 'ФИО', 'Телефон', 'Email', 'Роль'
        ])
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Кнопка удаления пользователя
        self.delete_user_button = QPushButton('Удалить пользователя')
        self.delete_user_button.clicked.connect(self.delete_user)
        
        layout.addWidget(self.users_table)
        layout.addWidget(self.delete_user_button)
        
        self.users_tab.setLayout(layout)
        self.update_users_table()
    
    def load_user_info(self):
        user_info = self.db.get_user_info(self.user_id)
        if user_info:
            username, full_name, phone, email, is_admin = user_info
            role = "Администратор" if is_admin else "Пользователь"
            self.user_info_label.setText(
                f"Пользователь: {full_name} ({username}) | Роль: {role} | Телефон: {phone} | Email: {email}")
    
    def update_cars_table(self):
        cars = self.db.get_all_cars()
        self.cars_table.setRowCount(len(cars))
        
        for row, car in enumerate(cars):
            for col, value in enumerate(car):
                item = QTableWidgetItem(str(value) if value is not None else '')
                self.cars_table.setItem(row, col, item)
    
    def update_parts_table(self):
        parts = self.db.get_all_parts()
        self.parts_table.setRowCount(len(parts))
        
        for row, part in enumerate(parts):
            for col, value in enumerate(part):
                if col == 5:  # Форматирование цены
                    item = QTableWidgetItem(f"{value:.2f}")
                else:
                    item = QTableWidgetItem(str(value) if value is not None else '')
                self.parts_table.setItem(row, col, item)
    
    def update_repairs_table(self):
        repairs = self.db.get_all_repairs()
        self.repairs_table.setRowCount(len(repairs))
        
        for row, repair in enumerate(repairs):
            for col, value in enumerate(repair):
                if col == 7:  # Форматирование стоимости
                    item = QTableWidgetItem(f"{value:.2f}" if value is not None else '')
                else:
                    item = QTableWidgetItem(str(value) if value is not None else '')
                self.repairs_table.setItem(row, col, item)
    
    def update_users_table(self):
        users = self.db.get_all_users()
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, value in enumerate(user):
                if col == 5:  # Роль
                    item = QTableWidgetItem("Администратор" if value else "Пользователь")
                else:
                    item = QTableWidgetItem(str(value) if value is not None else '')
                self.users_table.setItem(row, col, item)
    
    def update_car_combo(self):
        cars = self.db.get_all_cars()
        self.repair_car_id.clear()
        self.repair_car_id.addItem('Не указан', None)
        for car in cars:
            self.repair_car_id.addItem(f"{car[0]} - {car[3]} {car[4]}", car[0])
    
    def add_car(self):
        try:
            car_id = self.db.add_car(
                client_name=self.car_client_name.text(),
                client_phone=self.car_client_phone.text(),
                brand=self.car_brand.text(),
                model=self.car_model.text(),
                year=int(self.car_year.text()),
                color=self.car_color.text(),
                engine_volume=float(self.car_engine_volume.text()),
                transmission=self.car_transmission.currentText(),
                mileage=int(self.car_mileage.text()),
                price=float(self.car_price.text()),
                delivery_path=self.car_delivery_path.text(),
                order_date=self.car_order_date.date().toString('yyyy-MM-dd'),
                user_id=self.user_id
            )
            
            QMessageBox.information(self, 'Успех', f'Автомобиль добавлен с ID: {car_id}')
            self.update_cars_table()
            self.update_car_combo()
            
            # Очистка полей
            self.car_client_name.clear()
            self.car_client_phone.clear()
            self.car_brand.clear()
            self.car_model.clear()
            self.car_year.clear()
            self.car_color.clear()
            self.car_engine_volume.clear()
            self.car_transmission.setCurrentIndex(0)
            self.car_mileage.clear()
            self.car_price.clear()
            self.car_delivery_path.clear()
            self.car_order_date.setDate(QDate.currentDate())
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка', 'Проверьте правильность введенных данных')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении автомобиля: {str(e)}')
    
    def add_part(self):
        try:
            success = self.db.add_part(
                name=self.part_name.text(),
                code=self.part_code.text(),
                brand=self.part_brand.text(),
                car_model=self.part_car_model.text(),
                price=float(self.part_price.text()),
                quantity=int(self.part_quantity.text()),
                supplier=self.part_supplier.text() or None,
                description=self.part_description.toPlainText() or None
            )
            
            if success:
                QMessageBox.information(self, 'Успех', 'Запчасть добавлена')
                self.update_parts_table()
                
                # Очистка полей
                self.part_name.clear()
                self.part_code.clear()
                self.part_brand.clear()
                self.part_car_model.clear()
                self.part_price.clear()
                self.part_quantity.clear()
                self.part_supplier.clear()
                self.part_description.clear()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Запчасть с таким кодом уже существует')
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка', 'Проверьте правильность введенных данных')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении запчасти: {str(e)}')
    
    def add_repair(self):
        try:
            car_id = self.repair_car_id.currentData()
            
            repair_id = self.db.add_repair(
                car_id=car_id,
                client_name=self.repair_client_name.text(),
                client_phone=self.repair_client_phone.text(),
                start_date=self.repair_start_date.date().toString('yyyy-MM-dd'),
                description=self.repair_description.toPlainText(),
                user_id=self.user_id
            )
            
            QMessageBox.information(self, 'Успех', f'Ремонт добавлен с ID: {repair_id}')
            self.update_repairs_table()
            
            # Очистка полей
            self.repair_client_name.clear()
            self.repair_client_phone.clear()
            self.repair_start_date.setDate(QDate.currentDate())
            self.repair_description.clear()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении ремонта: {str(e)}')
    
    def add_user(self):
        try:
            success = self.db.add_user(
                username=self.new_username.text(),
                password=self.new_password.text(),
                full_name=self.new_full_name.text(),
                is_admin=self.new_is_admin.currentIndex() == 1,
                phone=self.new_phone.text() or None,
                email=self.new_email.text() or None
            )
            
            if success:
                QMessageBox.information(self, 'Успех', 'Пользователь добавлен')
                self.update_users_table()
                
                # Очистка полей
                self.new_username.clear()
                self.new_password.clear()
                self.new_full_name.clear()
                self.new_phone.clear()
                self.new_email.clear()
                self.new_is_admin.setCurrentIndex(0)
            else:
                QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким логином уже существует')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении пользователя: {str(e)}')
    
    def update_car_status(self):
        selected = self.cars_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите автомобиль')
            return
        
        car_id = int(self.cars_table.item(selected[0].row(), 0).text())
        current_status = self.cars_table.item(selected[0].row(), 7).text()
        
        statuses = ['ordered', 'purchased', 'delivery', 'preparation', 'ready', 'sold', 'canceled']
        status_names = ['Заказан', 'Куплен', 'В доставке', 'На подготовке', 'Готов', 'Продан', 'Отменен']
        
        current_index = statuses.index(current_status) if current_status in statuses else 0
        
        status, ok = QInputDialog.getItem(
            self, 'Обновить статус', 'Выберите новый статус:',
            status_names, current_index, False
        )
        
        if ok and status:
            new_status = statuses[status_names.index(status)]
            self.db.update_car_status(car_id, new_status)
            self.update_cars_table()
    
    def update_part_quantity(self):
        selected = self.parts_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите запчасть')
            return
        
        part_id = int(self.parts_table.item(selected[0].row(), 0).text())
        current_quantity = int(self.parts_table.item(selected[0].row(), 6).text())
        
        quantity, ok = QInputDialog.getInt(
            self, 'Изменить количество', 'Введите новое количество:',
            current_quantity, 0, 10000, 1
        )
        
        if ok:
            self.db.update_part_quantity(part_id, quantity)
            self.update_parts_table()
    
    def update_repair_status(self):
        selected = self.repairs_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ремонт')
            return
        
        repair_id = int(self.repairs_table.item(selected[0].row(), 0).text())
        current_status = self.repairs_table.item(selected[0].row(), 6).text()
        
        statuses = ['in_progress', 'waiting_parts', 'completed', 'canceled']
        status_names = ['В работе', 'Ожидает запчасти', 'Завершен', 'Отменен']
        
        current_index = statuses.index(current_status) if current_status in statuses else 0
        
        status, ok = QInputDialog.getItem(
            self, 'Обновить статус', 'Выберите новый статус:',
            status_names, current_index, False
        )
        
        if ok and status:
            new_status = statuses[status_names.index(status)]
            
            if new_status == 'completed':
                cost, ok_cost = QInputDialog.getDouble(
                    self, 'Стоимость ремонта', 'Введите стоимость ремонта:',
                    0, 0, 1000000, 2
                )
                
                if ok_cost:
                    self.db.update_repair_status(
                        repair_id, new_status, 
                        end_date=QDate.currentDate().toString('yyyy-MM-dd'),
                        total_cost=cost
                    )
            else:
                self.db.update_repair_status(repair_id, new_status)
            
            self.update_repairs_table()
    
    def delete_car(self):
        selected = self.cars_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите автомобиль')
            return
        
        car_id = int(self.cars_table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этот автомобиль?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_car(car_id)
            self.update_cars_table()
            self.update_car_combo()
    
    def delete_part(self):
        selected = self.parts_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите запчасть')
            return
        
        part_id = int(self.parts_table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить эту запчасть?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_part(part_id)
            self.update_parts_table()
    
    def delete_repair(self):
        selected = self.repairs_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ремонт')
            return
        
        repair_id = int(self.repairs_table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этот ремонт?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_repair(repair_id)
            self.update_repairs_table()
    
    def delete_user(self):
        selected = self.users_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите пользователя')
            return
        
        user_id = int(self.users_table.item(selected[0].row(), 0).text())
        
        if user_id == self.user_id:
            QMessageBox.warning(self, 'Ошибка', 'Вы не можете удалить себя')
            return
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этого пользователя?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_user(user_id)
            self.update_users_table()
    
    def logout(self):
        self.login_window = LoginWindow(self.db)
        self.login_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Создаем базу данных и добавляем тестового админа, если его нет
    db = Database()
    
    # Проверяем, есть ли хотя бы один администратор
    db.cursor.execute('SELECT id FROM users WHERE is_admin=1')
    if not db.cursor.fetchone():
        db.add_user('admin', 'admin', 'Администратор', is_admin=True)
    
    login_window = LoginWindow(db)
    login_window.show()
    
    sys.exit(app.exec_())