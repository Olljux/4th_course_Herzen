from dataclasses import dataclass, field
from datetime import datetime, date, timedelta


# Пользователь приложения
@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str

    def register(self):
        print("Пользователь зарегистрирован")

    def login(self):
        print("Выполнен вход в приложение")


# Учебный материал грамматического урока
@dataclass
class LessonMaterial:
    id: int
    content: str
    topic: str

    def display_material(self):
        print(self.content)


# Вопрос теста
@dataclass
class Question:
    id: int
    text: str
    options: list
    correct_answer: str

    def check_answer(self, answer):
        return answer == self.correct_answer


# Тест по грамматическому уроку
@dataclass
class Test:
    id: int
    passing_score: float
    questions: list = field(default_factory=list)

    def start_test(self):
        print("Тест начат")

    def check_result(self, attempt):
        return attempt.calculate_score(self)


# Грамматический урок
@dataclass
class Lesson:
    id: int
    title: str
    order_number: int
    material: LessonMaterial
    test: Test

    def get_material(self):
        return self.material

    def get_test(self):
        return self.test


# Попытка прохождения теста
@dataclass
class TestAttempt:
    id: int
    date: datetime = field(default_factory=datetime.now)
    score: float = 0
    passed: bool = False
    answers: dict = field(default_factory=dict)

    def calculate_score(self, test):
        if not test.questions:
            self.score = 0
            self.passed = False
            return self.score

        correct_answers = 0

        for question in test.questions:
            answer = self.answers.get(question.id)

            if question.check_answer(answer):
                correct_answers += 1

        self.score = correct_answers / len(test.questions) * 100
        self.passed = self.score >= test.passing_score

        return self.score


# Прогресс пользователя по грамматическим урокам
@dataclass
class LessonProgress:
    id: int
    status: str = "locked"
    attempts_count: int = 0
    attempts: list = field(default_factory=list)

    def update_status(self, status):
        self.status = status

    def complete_lesson(self):
        self.status = "completed"


# Карточка немецкого слова
@dataclass
class VocabularyWord:
    id: int
    german_word: str
    translation: str
    example: str

    def display_card(self):
        print(self.german_word)
        print(self.translation)
        print(self.example)


# Статистика запоминания отдельного слова пользователем
@dataclass
class VocabularyProgress:
    id: int
    correct_answers: int = 0
    incorrect_answers: int = 0
    memory_rating: float = 0
    next_review_date: date = field(default_factory=date.today)

    def update_statistics(self, is_correct):
        if is_correct:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

        self.calculate_memory_rating()

    def calculate_memory_rating(self):
        total = self.correct_answers + self.incorrect_answers

        if total == 0:
            self.memory_rating = 0
        else:
            self.memory_rating = self.correct_answers / total * 100

        return self.memory_rating


# Управление изучением лексики
class VocabularyService:

    def check_answer(self, word, user_answer):
        return user_answer.strip().lower() == word.translation.lower()

    def record_answer(self, word, progress, user_answer):
        is_correct = self.check_answer(word, user_answer)
        progress.update_statistics(is_correct)

        if is_correct:
            progress.next_review_date = date.today() + timedelta(days=3)
        else:
            progress.next_review_date = date.today() + timedelta(days=1)

        return is_correct

    def select_words_for_review(self, words, progress_list):
        selected_words = []

        for word, progress in zip(words, progress_list):
            if progress.next_review_date <= date.today():
                selected_words.append(word)

        return selected_words


# Управление прохождением грамматических уроков
class LessonService:

    def check_passing_score(self, attempt, test):
        return attempt.calculate_score(test) >= test.passing_score

    def unlock_next_lesson(self, progress_list, current_lesson):
        next_order = current_lesson.order_number + 1

        for progress in progress_list:
            if progress.status == "locked":
                progress.update_status("available")
                break

    def repeat_lesson(self, progress):
        progress.update_status("in_progress")
        progress.attempts_count += 1