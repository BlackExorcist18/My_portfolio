"""Модуль основной логики тестирования.

Содержит класс QuizEngine, который управляет процессом 
прохождения тестов, проверкой ответов и подсчетом результатов.
"""

import random
from typing import List, Dict, Any, Tuple, Optional


class QuizEngine:
    """Движок для управления процессом тестирования.
    
    Attributes:
        tests (List[Dict[str, Any]]): Список всех доступных тестов.
        current_test (Dict[str, Any]): Текущий выбранный тест.
        current_questions (List[Dict[str, Any]]): Вопросы текущего теста.
        score (int): Количество правильных ответов.
        total_questions (int): Общее количество вопросов в тесте.
        current_question_index (int): Индекс текущего вопроса.
    """
    
    def __init__(self, tests: List[Dict[str, Any]]):
        """Инициализирует движок тестирования.
        
        Args:
            tests (List[Dict[str, Any]]): Список тестов для инициализации.
        """
        self.tests = tests
        self.current_test = None
        self.current_questions = []
        self.score = 0
        self.total_questions = 0
        self.current_question_index = 0
    
    def list_tests(self) -> List[str]:
        """Получает список названий доступных тестов.
        
        Returns:
            List[str]: Список названий тестов.
        """
        return [test['name'] for test in self.tests]
    
    def select_test(self, test_name: str) -> bool:
        """Выбирает тест по имени для прохождения.
        
        Args:
            test_name (str): Название теста для выбора.
            
        Returns:
            bool: True если тест найден и выбран, False в противном случае.
        """
        for test in self.tests:
            if test['name'] == test_name:
                self.current_test = test
                self.current_questions = test['questions'].copy()
                return True
        return False
    
    def shuffle_questions(self, count: int = None) -> None:
        """Перемешивает вопросы и выбирает указанное количество.
        
        Args:
            count (int, optional): Количество вопросов для выбора. 
                                Если None, используются все вопросы.
        """
        random.shuffle(self.current_questions)
        if count and count < len(self.current_questions):
            self.current_questions = self.current_questions[:count]
    
    def start_quiz(self, shuffle: bool = True, question_count: int = None) -> None:
        """Начинает процесс тестирования.
        
        Args:
            shuffle (bool): Нужно ли перемешивать вопросы. По умолчанию True.
            question_count (int, optional): Количество вопросов для теста.
            
        Raises:
            ValueError: Если тест не был выбран перед началом.
        """
        if not self.current_test:
            raise ValueError("Тест не выбран")
        
        if shuffle:
            self.shuffle_questions(question_count)
        elif question_count:
            self.current_questions = self.current_questions[:question_count]
        
        self.score = 0
        self.total_questions = len(self.current_questions)
        self.current_question_index = 0
        
        print(f"\nНачинаем тест: {self.current_test['name']}")
        print(f"Количество вопросов: {self.total_questions}")
        print("=" * 50)
    
    def get_next_question(self) -> Optional[Tuple[str, List[str], int]]:
        """Получает следующий вопрос из текущего теста.
        
        Returns:
            Optional[Tuple[str, List[str], int]]: Кортеж (вопрос, варианты ответов, 
                                                индекс правильного ответа) 
                                                или None если вопросы закончились.
        """
        if self.current_question_index >= len(self.current_questions):
            return None
        
        question_data = self.current_questions[self.current_question_index]
        question = question_data['question']
        options = question_data['options']
        correct_answer = question_data['correct_answer']
        
        self.current_question_index += 1
        return question, options, correct_answer
    
    def check_answer(self, user_answer: int, correct_answer: int) -> bool:
        """Проверяет ответ пользователя.
        
        Args:
            user_answer (int): Индекс ответа, выбранного пользователем.
            correct_answer (int): Индекс правильного ответа.
            
        Returns:
            bool: True если ответ правильный, False в противном случае.
        """
        is_correct = user_answer == correct_answer
        if is_correct:
            self.score += 1
        return is_correct
    
    def get_progress(self) -> Tuple[int, int]:
        """Получает текущий прогресс прохождения теста.
        
        Returns:
            Tuple[int, int]: Текущий номер вопроса и общее количество вопросов.
        """
        return self.current_question_index, self.total_questions
    
    def get_results(self) -> Dict[str, Any]:
        """Подсчитывает и возвращает результаты тестирования.
        
        Returns:
            Dict[str, Any]: Словарь с результатами теста, содержащий:
                - test_name: название теста
                - score: количество правильных ответов
                - total_questions: общее количество вопросов
                - percentage: процент правильных ответов
                - passed: пройден ли тест (>= 70%)
        """
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        return {
            'test_name': self.current_test['name'],
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': percentage,
            'passed': percentage >= 70
        }