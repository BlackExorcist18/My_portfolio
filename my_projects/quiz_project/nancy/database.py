"""Модуль для работы с базой данных PostgreSQL."""

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import List, Dict, Any

Base = declarative_base()

class Test(Base):
    """Модель теста."""
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с вопросами
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")

class Question(Base):
    """Модель вопроса."""
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    option1 = Column(Text, nullable=False)
    option2 = Column(Text, nullable=False)
    option3 = Column(Text)
    option4 = Column(Text)
    correct_answer = Column(Integer, nullable=False)  # 0-3
    
    # Связь с тестом
    test = relationship("Test", back_populates="questions")

class TestResult(Base):
    """Модель результата тестирования."""
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    user_name = Column(String(100), default="Аноним")
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с тестом
    test = relationship("Test")

class DatabaseManager:
    """Менеджер для работы с базой данных."""
    
    def __init__(self, database_url: str = None):
        """
        Инициализация менеджера базы данных.
        
        Args:
            database_url: URL подключения к PostgreSQL. Если None, используется из переменных окружения.
        """
        if database_url is None:
            database_url = os.getenv(
                'DATABASE_URL', 
                'postgresql://username:password@localhost:5432/quiz_system'
            )
        
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db(self) -> None:
        """Создание таблиц в базе данных."""
        Base.metadata.create_all(bind=self.engine)
        print("✅ Таблицы базы данных созданы")
    
    def get_session(self):
        """Получить сессию базы данных."""
        return self.SessionLocal()
    
    def add_test(self, test_data: Dict[str, Any]) -> bool:
        """Добавить тест в базу данных.
        
        Args:
            test_data: Данные теста в формате JSON.
            
        Returns:
            bool: True если успешно, False в случае ошибки.
        """
        try:
            session = self.get_session()
            
            # Проверяем, существует ли тест с таким именем
            existing_test = session.query(Test).filter(Test.name == test_data['name']).first()
            if existing_test:
                print(f"Тест с именем '{test_data['name']}' уже существует")
                return False
            
            # Создаем тест
            test = Test(
                name=test_data['name'],
                description=test_data.get('description', '')
            )
            session.add(test)
            session.flush()  # Получаем ID теста
            
            # Добавляем вопросы
            for question_data in test_data['questions']:
                question = Question(
                    test_id=test.id,
                    question_text=question_data['question'],
                    option1=question_data['options'][0],
                    option2=question_data['options'][1],
                    option3=question_data['options'][2] if len(question_data['options']) > 2 else None,
                    option4=question_data['options'][3] if len(question_data['options']) > 3 else None,
                    correct_answer=question_data['correct_answer']
                )
                session.add(question)
            
            session.commit()
            print(f"✅ Тест '{test_data['name']}' добавлен в базу данных")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при добавлении теста: {e}")
            return False
        finally:
            session.close()
    
    def get_all_tests(self) -> List[Dict[str, Any]]:
        """Получить все тесты из базы данных.
        
        Returns:
            List[Dict[str, Any]]: Список тестов.
        """
        try:
            session = self.get_session()
            tests = session.query(Test).all()
            
            result = []
            for test in tests:
                test_dict = {
                    'name': test.name,
                    'description': test.description,
                    'questions_count': len(test.questions),
                    'created_at': test.created_at
                }
                result.append(test_dict)
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка при получении тестов: {e}")
            return []
        finally:
            session.close()
    
    def get_test_by_name(self, test_name: str) -> Dict[str, Any]:
        """Получить тест по имени.
        
        Args:
            test_name: Название теста.
            
        Returns:
            Dict[str, Any]: Данные теста или пустой словарь если не найден.
        """
        try:
            session = self.get_session()
            test = session.query(Test).filter(Test.name == test_name).first()
            
            if not test:
                return {}
            
            questions = []
            for question in test.questions:
                options = [question.option1, question.option2]
                if question.option3:
                    options.append(question.option3)
                if question.option4:
                    options.append(question.option4)
                
                questions.append({
                    'question': question.question_text,
                    'options': options,
                    'correct_answer': question.correct_answer
                })
            
            return {
                'name': test.name,
                'description': test.description,
                'questions': questions
            }
            
        except Exception as e:
            print(f"❌ Ошибка при получении теста: {e}")
            return {}
        finally:
            session.close()
    
    def save_test_result(self, result_data: Dict[str, Any]) -> bool:
        """Сохранить результат тестирования.
        
        Args:
            result_data: Данные результата.
            
        Returns:
            bool: True если успешно, False в случае ошибки.
        """
        try:
            session = self.get_session()
            
            # Находим ID теста
            test = session.query(Test).filter(Test.name == result_data['test_name']).first()
            if not test:
                print(f"Тест '{result_data['test_name']}' не найден")
                return False
            
            # Сохраняем результат
            result = TestResult(
                test_id=test.id,
                user_name=result_data.get('user_name', 'Аноним'),
                score=result_data['score'],
                total_questions=result_data['total_questions'],
                percentage=result_data['percentage'],
                passed=result_data['passed']
            )
            
            session.add(result)
            session.commit()
            print("✅ Результат тестирования сохранен в базу данных")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при сохранении результата: {e}")
            return False
        finally:
            session.close()
    
    def get_test_results(self, test_name: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Получить результаты тестирования.
        
        Args:
            test_name: Фильтр по названию теста. Если None, возвращаются все результаты.
            limit: Максимальное количество результатов.
            
        Returns:
            List[Dict[str, Any]]: Список результатов.
        """
        try:
            session = self.get_session()
            
            query = session.query(TestResult).join(Test)
            if test_name:
                query = query.filter(Test.name == test_name)
            
            results = query.order_by(TestResult.completed_at.desc()).limit(limit).all()
            
            result_list = []
            for result in results:
                result_list.append({
                    'test_name': result.test.name,
                    'user_name': result.user_name,
                    'score': result.score,
                    'total_questions': result.total_questions,
                    'percentage': result.percentage,
                    'passed': result.passed,
                    'completed_at': result.completed_at
                })
            
            return result_list
            
        except Exception as e:
            print(f"❌ Ошибка при получении результатов: {e}")
            return []
        finally:
            session.close()