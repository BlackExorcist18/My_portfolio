# catalog/data.py
# Данные об авторах
AUTHORS = [
    {
        'id': 1,
        'name': 'Иван Петров',
        'specialization': 'Python разработка',
        'experience': '8 лет',
        'email': 'ivan.petrov@example.com',
        'bio': 'Опытный разработчик и преподаватель. Специализируется на backend-разработке на Python и Django.'
    },
    {
        'id': 2,
        'name': 'Мария Иванова',
        'specialization': 'Веб-дизайн',
        'experience': '6 лет',
        'email': 'maria.ivanova@example.com',
        'bio': 'Профессиональный веб-дизайнер. Преподает курсы по HTML/CSS, JavaScript и UI/UX дизайну.'
    },
    {
        'id': 3,
        'name': 'Алексей Смирнов',
        'specialization': 'Data Science',
        'experience': '10 лет',
        'email': 'alexey.smirnov@example.com',
        'bio': 'Специалист в области анализа данных и машинного обучения. Кандидат технических наук.'
    },
]

# Данные о курсах
COURSES = [
    {
        'id': 1,
        'name': 'Django для начинающих',
        'description': 'Полный курс по веб-разработке на Django. Изучите создание веб-приложений с нуля.',
        'author_id': 1,
        'level': 'Начальный',
        'duration': '6 недель',
        'students_count': 1245,
        'rating': 4.8,
        'topics': ['Введение в Django', 'Модели и базы данных', 'View и шаблоны', 'Формы', 'Аутентификация', 'Деплой']
    },
    {
        'id': 2,
        'name': 'Продвинутый Django',
        'description': 'Углубленный курс по Django REST Framework, оптимизации и масштабированию проектов.',
        'author_id': 1,
        'level': 'Продвинутый',
        'duration': '8 недель',
        'students_count': 567,
        'rating': 4.9,
        'topics': ['Django REST Framework', 'Оптимизация запросов', 'Кэширование', 'WebSockets', 'Тестирование', 'Docker']
    },
    {
        'id': 3,
        'name': 'Современный HTML/CSS',
        'description': 'Изучите современные подходы к верстке веб-страниц. Flexbox, Grid, анимации и адаптивный дизайн.',
        'author_id': 2,
        'level': 'Начальный',
        'duration': '4 недели',
        'students_count': 2134,
        'rating': 4.7,
        'topics': ['HTML5 семантика', 'CSS3', 'Flexbox', 'Grid Layout', 'Анимации', 'Адаптивная верстка']
    },
    {
        'id': 4,
        'name': 'JavaScript для веб-разработчиков',
        'description': 'Полный курс по JavaScript: от основ до современного ES6+ и асинхронного программирования.',
        'author_id': 2,
        'level': 'Средний',
        'duration': '8 недель',
        'students_count': 1876,
        'rating': 4.8,
        'topics': ['Основы JS', 'DOM манипуляции', 'События', 'ES6+', 'Асинхронность', 'API работа']
    },
    {
        'id': 5,
        'name': 'Введение в Data Science',
        'description': 'Основы анализа данных, Pandas, NumPy и визуализация данных.',
        'author_id': 3,
        'level': 'Начальный',
        'duration': '10 недель',
        'students_count': 892,
        'rating': 4.6,
        'topics': ['Python для анализа', 'NumPy', 'Pandas', 'Визуализация', 'Статистика', 'Машинное обучение основы']
    },
    {
        'id': 6,
        'name': 'Машинное обучение',
        'description': 'Практический курс по машинному обучению. Scikit-learn, нейронные сети и работа с реальными данными.',
        'author_id': 3,
        'level': 'Продвинутый',
        'duration': '12 недель',
        'students_count': 445,
        'rating': 4.9,
        'topics': ['Scikit-learn', 'Регрессия', 'Классификация', 'Кластеризация', 'Нейронные сети', 'Feature engineering']
    },
]