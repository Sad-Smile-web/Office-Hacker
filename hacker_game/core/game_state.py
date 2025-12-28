import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List
import random

from core.email_system import EmailSystem
from simple_translation import translation


def tr(key, default=None, **kwargs):
    """Вспомогательная функция для перевода с дефолтным значением"""
    if default is None:
        default = key
    return translation.t(key, default=default, **kwargs)


@dataclass
class GameState:
    """Состояние игры"""
    first_name: str = ""
    last_name: str = ""
    day: int = 1
    shift_started: bool = False
    tasks_completed: int = 0
    reputation: int = 0
    money: float = 500.0  # В рублях
    skills: Dict[str, int] = field(default_factory=dict)
    current_task: str = ""
    current_task_progress: int = 0
    task_difficulty: int = 1
    shift_time: int = 0  # В минутах от начала смены
    energy: int = 100
    stress: int = 0
    completed_tasks_list: List[str] = field(default_factory=list)
    
    # Игровое время
    game_time: Dict = field(default_factory=dict)
    
    # Система почты
    email_system: EmailSystem = None
    
    # Конфигурация специальных писем
    special_emails_config: Dict = field(default_factory=dict)
    
    # Время на паузе (для main_window.py)
    time_paused: bool = False
    
    def __post_init__(self):
        if not self.skills:
            self.skills = {
                tr("game_state.skill_hacking", "Взлом"): 1,
                tr("game_state.skill_social_engineering", "Социальная инженерия"): 1,
                tr("game_state.skill_programming", "Программирование"): 1,
                tr("game_state.skill_stealth", "Скрытность"): 1,
                tr("game_state.skill_analysis", "Анализ"): 1,
                tr("game_state.skill_network_security", "Сетевая безопасность"): 1
            }
        
        if not self.completed_tasks_list:
            self.completed_tasks_list = []
        
        # Инициализация игрового времени
        if not self.game_time:
            self.game_time = {
                'current_hour': 9,  # Начало рабочего дня в 9:00
                'current_minute': 0,
                'day': self.day,
                'month': 1,
                'year': 1984,
                'is_paused': False,
                'time_speed': 1.0,
                'workday_start': 9,
                'workday_end': 18
            }
        
        # Настройка конфигурации специальных писем
        if not self.special_emails_config:
            self.special_emails_config = {
                "error_message": {
                    "enabled": True,
                    "required_tasks": 1,
                    "required_time": 60,
                    "description": tr("game_state.special_email_config", "Письмо ERROR - отправляется после выполнения первой задачи через 60 минут")
                }
            }
        
        # Инициализируем систему почты, если её нет
        if self.email_system is None:
            self.email_system = EmailSystem(
                player_name=self.player_name,
                day=self.day,
                reputation=self.reputation,
                money=self.money
            )
    
    @property
    def player_name(self):
        """Полное имя сотрудника"""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return ""
    
    @player_name.setter
    def player_name(self, value):
        """Установка полного имени"""
        if value:
            parts = value.strip().split()
            self.first_name = parts[0] if len(parts) > 0 else ""
            self.last_name = parts[1] if len(parts) > 1 else ""
            # Обновляем имя в системе почты
            if self.email_system:
                self.email_system.player_name = self.player_name
        else:
            self.first_name = ""
            self.last_name = ""
    
    @property
    def unread_emails(self):
        """Количество непрочитанных писем (свойство для обратной совместимости)"""
        return self.email_system.get_unread_count() if self.email_system else 0
    
    @property
    def mvd_email_read(self):
        """Флаг прочтения письма от МВД (свойство для обратной совместимости)"""
        return self.email_system.mvd_email_read if self.email_system else False
    
    def start_new_shift(self):
        """Начать новую смену (для совместимости с main_window.py)"""
        return self.start_shift()
    
    def start_shift(self):
        """Начать смену"""
        self.shift_started = True
        self.current_task = tr("game_state.initial_task", "Проверьте почту и прочитайте срочное письмо от МВД")
        self.current_task_progress = 0
        self.task_difficulty = 1
        self.shift_time = 0
        self.energy = 100
        self.stress = 0
        
        # Сброс игрового времени на начало смены (9:00)
        self.game_time.update({
            'current_hour': 9,
            'current_minute': 0,
            'day': self.day,
            'is_paused': False
        })
        
        # Добавляем начальные письма, если их еще нет
        if not self.email_system.emails_received_today:
            self.email_system.add_initial_emails()
    
    def save(self, slot: int = 0):
        """Сохранить игру"""
        filename = f"saves/slot_{slot}.json"
        os.makedirs("saves", exist_ok=True)
        
        # Подготавливаем данные для сохранения
        data = asdict(self)
        
        if 'email_system' in data:
            email_system_data = data.pop('email_system')
        else:
            email_system_data = None
        
        # Обновляем данные email_system перед сохранением
        if self.email_system:
            self.email_system.player_name = self.player_name
            self.email_system.day = self.day
            self.email_system.reputation = self.reputation
            self.email_system.money = self.money
            email_system_data = self.email_system.to_dict()
        
        # Добавляем данные почтовой системы
        data["email_system"] = email_system_data
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(tr("game.save_success", "[СОХРАНЕНИЕ] Игра сохранена в {filename}").format(filename=filename))
    
    @classmethod
    def load(cls, slot: int = 0):
        """Загрузить игру"""
        filename = f"saves/slot_{slot}.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Обратная совместимость со старыми сохранениями
                    if 'player_name' in data and ('first_name' not in data or not data['first_name']):
                        if 'player_name' in data:
                            parts = data['player_name'].split()
                            data['first_name'] = parts[0] if len(parts) > 0 else ""
                            data['last_name'] = parts[1] if len(parts) > 1 else ""
                    
                    # Обновляем названия навыков
                    if 'skills' in data:
                        old_to_new = {
                            'hacking': tr("game_state.skill_hacking", "Взлом"),
                            'social_engineering': tr("game_state.skill_social_engineering", "Социальная инженерия"),
                            'programming': tr("game_state.skill_programming", "Программирование"),
                            'stealth': tr("game_state.skill_stealth", "Скрытность"),
                            'analysis': tr("game_state.skill_analysis", "Анализ"),
                            'network_security': tr("game_state.skill_network_security", "Сетевая безопасность")
                        }
                        new_skills = {}
                        for key, value in data['skills'].items():
                            new_key = old_to_new.get(key, key)
                            new_skills[new_key] = value
                        
                        # Добавляем недостающие навыки
                        required_skills = [
                            tr("game_state.skill_analysis", "Анализ"),
                            tr("game_state.skill_network_security", "Сетевая безопасность")
                        ]
                        for skill in required_skills:
                            if skill not in new_skills:
                                new_skills[skill] = 1
                        data['skills'] = new_skills
                    
                    # Обработка старого формата писем (для обратной совместимости)
                    email_system_data = data.get('email_system')
                    
                    if email_system_data is None and 'emails' in data:
                        # Конвертируем старый формат в новый
                        email_system_data = cls._convert_old_emails_format(data)
                        data['email_system'] = email_system_data
                        # Удаляем старые поля
                        for field in ['emails', 'unread_emails', 'emails_received_today', 
                                     'mvd_email_read', 'next_email_id']:
                            data.pop(field, None)
                    
                    # Загружаем систему почты, если есть данные
                    email_system = None
                    if email_system_data:
                        email_system = EmailSystem.from_dict(email_system_data)
                    
                    data['email_system'] = email_system
                    
                    # Загружаем игровое время или инициализируем новое
                    if 'game_time' not in data:
                        data['game_time'] = {
                            'current_hour': 9,
                            'current_minute': 0,
                            'day': data.get('day', 1),
                            'month': 1,
                            'year': 1984,
                            'is_paused': False,
                            'time_speed': 1.0,
                            'workday_start': 9,
                            'workday_end': 18
                        }
                    
                    # Загружаем конфигурацию специальных писем
                    if 'special_emails_config' not in data:
                        data['special_emails_config'] = {
                            "error_message": {
                                "enabled": True,
                                "required_tasks": 1,
                                "required_time": 60,
                                "description": tr("game_state.special_email_config", "Письмо ERROR - отправляется после выполнения первой задачи через 60 минут")
                            }
                        }
                    
                    # Добавляем недостающие поля для совместимости
                    default_fields = [
                        ('current_task_progress', 0),
                        ('task_difficulty', 1),
                        ('shift_time', 0),
                        ('energy', 100),
                        ('stress', 0),
                        ('completed_tasks_list', []),
                        ('time_paused', False),
                    ]
                    
                    for field_name, default_value in default_fields:
                        if field_name not in data:
                            data[field_name] = default_value
                    
                    # Создаем экземпляр GameState
                    return cls(**data)
                    
            except Exception as e:
                print(tr("game.load_error", "[ОШИБКА] Не удалось загрузить сохранение: {error}").format(error=e))
                return cls()
        else:
            print(tr("game.save_not_found", "[ИНФО] Сохранение не найдено: {filename}").format(filename=filename))
            return cls()
    
    @staticmethod
    def _convert_old_emails_format(data: dict) -> dict:
        """Конвертировать старый формат писем в новый"""
        emails = data.get('emails', [])
        
        # Создаем систему почты
        email_system = EmailSystem(
            player_name=data.get('player_name', ''),
            day=data.get('day', 1),
            reputation=data.get('reputation', 0),
            money=data.get('money', 0.0)
        )
        
        # Переносим старые письма
        for email_data in emails:
            email_system.add_email(
                sender=email_data.get('sender', ''),
                subject=email_data.get('subject', ''),
                content=email_data.get('content', ''),
                important=email_data.get('important', False)
            )
        
        # Помечаем письма как прочитанные/непрочитанные
        unread_emails = data.get('unread_emails', 0)
        emails_received_today = data.get('emails_received_today', False)
        mvd_email_read = data.get('mvd_email_read', False)
        
        # Обновляем флаги
        email_system.emails_received_today = emails_received_today
        email_system.mvd_email_read = mvd_email_read
        
        return email_system.to_dict()
    
    def generate_new_task(self):
        """Сгенерировать новое задание"""
        tasks = [
            tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД"),
            tr("game_state.task_scan_network", "Просканировать сеть на уязвимости"),
            tr("game_state.task_update_antivirus", "Обновить антивирусные базы"),
            tr("game_state.task_check_security_logs", "Проверить логи безопасности"),
            tr("game_state.task_configure_firewall", "Настроить межсетевой экран"),
            tr("game_state.task_analyze_traffic", "Проанализировать подозрительный трафик"),
            tr("game_state.task_install_updates", "Установить обновления безопасности"),
            tr("game_state.task_check_backups", "Проверить резервные копии"),
            tr("game_state.task_setup_vpn", "Настроить VPN подключение"),
            tr("game_state.task_audit_users", "Провести аудит пользователей"),
            tr("game_state.task_test_recovery", "Протестировать систему восстановления")
        ]
        
        difficulty_modifiers = [
            tr("game_state.difficulty_easy", "легкую"),
            tr("game_state.difficulty_medium", "стандартную"),
            tr("game_state.difficulty_hard", "сложную"),
            tr("game_state.difficulty_expert", "экспертную")
        ]
        
        # Если это первая задача дня и письмо МВД не прочитано
        if self.tasks_completed == 0 and not self.email_system.mvd_email_read:
            self.current_task = tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД")
        # Если это вторая задача дня (первая задача была выполнена)
        elif self.tasks_completed == 1:
            self.current_task = tr("game_state.task_familiarize", "Освойтесь с интерфейсом, пока ждете ваше первое задание")
            # Устанавливаем низкую сложность для этой ознакомительной задачи
            self.task_difficulty = 1
        else:
            # Исключаем задачу про почту из списка после ее выполнения
            email_task = tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД")
            available_tasks = [t for t in tasks if t != email_task]
            task = random.choice(available_tasks)
            self.current_task = tr("game_state.task_template", "Выполните {modifier} задачу: {task}").format(
                modifier=random.choice(difficulty_modifiers),
                task=task
            )
            # Сложность для обычных задач
            self.task_difficulty = random.randint(1, 4)
        
        # Сбрасываем прогресс для новой задачи
        self.current_task_progress = 0
    
    def update_time(self, minutes: int = 1):
        """Обновить игровое время на указанное количество минут"""
        if self.game_time.get('is_paused', False):
            return
        
        self.game_time['current_minute'] += minutes
        self.shift_time += minutes  # Обновляем время смены
        
        # Проверка переполнения минут
        if self.game_time['current_minute'] >= 60:
            self.game_time['current_minute'] = 0
            self.game_time['current_hour'] += 1
            
            # Проверка окончания рабочего дня
            if self.game_time['current_hour'] >= self.game_time.get('workday_end', 18):
                # Конец рабочего дня
                self.end_workday()
            
            # Смена дня
            if self.game_time['current_hour'] >= 24:
                self.game_time['current_hour'] = 0
                self.game_time['day'] += 1
                
                # Упрощенная логика месяцев
                if self.game_time['day'] > 30:
                    self.game_time['day'] = 1
                    self.game_time['month'] += 1
                    
                    if self.game_time['month'] > 12:
                        self.game_time['month'] = 1
                        self.game_time['year'] += 1
        
        # Проверка специальных писем после обновления времени
        self.check_special_emails()
    
    def get_formatted_time(self):
        """Получить отформатированное время"""
        hour = self.game_time.get('current_hour', 9)
        minute = self.game_time.get('current_minute', 0)
        return f"{hour:02d}:{minute:02d}"
    
    def get_formatted_date(self):
        """Получить отформатированную дату"""
        day = self.game_time.get('day', self.day)
        month = self.game_time.get('month', 1)
        year = self.game_time.get('year', 1984)
        return f"{day:02d}.{month:02d}.{year}"
    
    def get_workday_progress(self):
        """Получить прогресс рабочего дня в процентах"""
        workday_start = self.game_time.get('workday_start', 9)
        workday_end = self.game_time.get('workday_end', 18)
        
        current_hour = self.game_time.get('current_hour', 9)
        current_minute = self.game_time.get('current_minute', 0)
        
        # Если до начала рабочего дня или после конца
        if current_hour < workday_start:
            return 0
        elif current_hour >= workday_end:
            return 100
        
        # Общее количество минут рабочего дня
        total_minutes = (workday_end - workday_start) * 60
        
        # Сколько минут прошло с начала рабочего дня
        minutes_passed = (current_hour - workday_start) * 60 + current_minute
        
        # Прогресс в процентах
        progress = (minutes_passed / total_minutes) * 100 if total_minutes > 0 else 0
        
        # Ограничиваем от 0 до 100
        return min(100, max(0, progress))
    
    def make_task_progress(self, amount: int = 10):
        """Сделать прогресс в задании"""
        if not self.shift_started:
            return False
        
        # Если это задача с почты или ознакомительная задача, добавляем прогресс без времени
        email_task = tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД")
        familiarize_task = tr("game_state.task_familiarize", "Освойтесь с интерфейсом, пока ждете ваше первое задание")
        
        if (self.current_task == email_task or self.current_task == familiarize_task):
            self.current_task_progress = min(100, self.current_task_progress + amount)
            
            # Проверка завершения задачи
            if self.current_task_progress >= 100:
                return self.complete_task()
            
            return True
        else:
            # Для обычных задач добавляем время
            self.current_task_progress += amount
            
            # Обновляем время при прогрессе задачи
            time_per_progress = 5  # 5 игровых минут за 10% прогресса
            self.update_time(time_per_progress)
            
            # Расход энергии
            energy_cost = self.task_difficulty * 2
            self.energy = max(0, self.energy - energy_cost)
            
            # Накопление стресса
            stress_gain = random.randint(1, 3)
            self.stress = min(100, self.stress + stress_gain)
            
            # Проверка завершения задачи
            if self.current_task_progress >= 100:
                return self.complete_task()
            
            return True
    
    def add_mail_task_progress(self, amount: int):
        """Добавить прогресс для задачи с почты или ознакомительной задачи (без обновления времени)"""
        if not self.shift_started:
            return False
        
        email_task = tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД")
        familiarize_task = tr("game_state.task_familiarize", "Освойтесь с интерфейсом, пока ждете ваше первое задание")
        
        if (self.current_task == email_task or self.current_task == familiarize_task):
            self.current_task_progress = min(100, self.current_task_progress + amount)
            
            # Проверка завершения задачи
            if self.current_task_progress >= 100:
                return self.complete_task()
            
            return True
        return False
    
    def complete_task(self):
        """Завершить текущее задание"""
        self.tasks_completed += 1
        
        # Награда зависит от сложности
        base_reward = 50
        reward_multiplier = self.task_difficulty * 0.5
        
        money_earned = base_reward * reward_multiplier
        reputation_earned = 10 * self.task_difficulty
        
        self.money += money_earned
        self.reputation += reputation_earned
        
        # Прокачка навыков (случайный навык)
        skill_to_improve = random.choice(list(self.skills.keys()))
        current_level = self.skills[skill_to_improve]
        
        # Шанс улучшения зависит от сложности задачи
        improvement_chance = 0.3 + (self.task_difficulty * 0.1)
        if random.random() < improvement_chance and current_level < 10:
            self.skills[skill_to_improve] = current_level + 1
        
        # Восстановление энергии
        self.energy = min(100, self.energy + 20)
        
        # Уменьшение стресса
        self.stress = max(0, self.stress - 15)
        
        # Добавляем задачу в список выполненных
        self.completed_tasks_list.append(self.current_task)
        
        # Проверка условий для отправки специальных писем после выполнения задачи
        self.check_special_emails()
        
        # Генерируем новое задание
        self.generate_new_task()
        
        # Добавляем письмо о выполненном задании (иногда)
        if random.random() < 0.3:  # 30% шанс
            self.email_system.add_system_notification(
                tr("game_state.task_completed_notification", 
                   "Задание '{task}' выполнено успешно. Награда: {money:.2f} ₽").format(
                    task=self.current_task, money=money_earned)
            )
        
        return {
            "money": money_earned,
            "reputation": reputation_earned,
            "skill_improved": skill_to_improve if self.skills[skill_to_improve] > current_level else None
        }
    
    def check_special_emails(self):
        """Проверить условия для отправки специальных писем"""
        if not self.email_system:
            return
        
        # Проверяем каждое письмо в конфигурации
        for email_type, config in self.special_emails_config.items():
            if config.get("enabled", False):
                # Подготавливаем данные для проверки
                condition_data = {
                    "tasks_completed": self.tasks_completed,
                    "shift_time": self.shift_time,
                    "required_tasks": config.get("required_tasks", 0),
                    "required_time": config.get("required_time", 0)
                }
                
                # Проверяем и отправляем письмо
                was_sent = self.email_system.check_and_send_special_email(
                    email_type=email_type,
                    shift_time=self.shift_time,
                    condition_data=condition_data
                )
                
                if was_sent:
                    print(tr("game.special_email_sent", "[ИГРА] Отправлено специальное письмо: {type}").format(type=email_type))
    
    def add_special_email_config(self, email_type: str, config: dict):
        """Добавить конфигурацию для специального письма"""
        self.special_emails_config[email_type] = config
        print(tr("game.special_email_config_added", "[ИГРА] Добавлена конфигурация для письма: {type}").format(type=email_type))
    
    def enable_special_email(self, email_type: str, enabled: bool = True):
        """Включить/выключить отправку специального письма"""
        if email_type in self.special_emails_config:
            self.special_emails_config[email_type]["enabled"] = enabled
            print(tr("game.special_email_toggled", "[ИГРА] Письмо '{type}' {status}").format(
                type=email_type, 
                status=tr("game.enabled", "включено") if enabled else tr("game.disabled", "выключено")
            ))
    
    def mark_email_as_read(self, email_id: int):
        """Пометить письмо как прочитанное"""
        if self.email_system.mark_as_read(email_id):
            # Проверяем, является ли это письмо от МВД
            email = self.email_system.get_email_by_id(email_id)
            if email and email.sender == tr("templates.system_welcome.sender", "МВД"):
                # Если текущая задача - прочитать письмо МВД, добавляем прогресс
                email_task = tr("game_state.task_check_email", "Проверьте почту и прочитайте срочное письмо от МВД")
                if self.current_task == email_task:
                    # Если прогресс меньше 100, добавляем оставшийся прогресс
                    if self.current_task_progress < 100:
                        remaining_progress = 100 - self.current_task_progress
                        return self.add_mail_task_progress(remaining_progress)
            
            return True
        return False
    
    def add_new_email(self, sender: str, subject: str, content: str, important: bool = False):
        """Добавить новое письмо (метод для обратной совместимости)"""
        return self.email_system.add_email(sender, subject, content, important)
    
    def get_current_time(self):
        """Получить текущее игровое время (обратная совместимость)"""
        return self.get_formatted_time()
    
    def take_break(self):
        """Сделать перерыв"""
        if not self.shift_started:
            return False
        
        # Перерыв занимает время (15 минут)
        self.update_time(15)
        
        # Восстановление энергии
        energy_restored = random.randint(20, 40)
        self.energy = min(100, self.energy + energy_restored)
        
        # Уменьшение стресса
        stress_reduced = random.randint(10, 25)
        self.stress = max(0, self.stress - stress_reduced)
        
        # Проверка условий для специальных писем после перерыва
        self.check_special_emails()
        
        return True
    
    def get_money_display(self):
        """Получить отформатированную строку с деньгами"""
        return f"{self.money:,.2f} ₽".replace(',', ' ')
    
    def get_shift_time_display(self):
        """Получить отформатированное время смены (обратная совместимость)"""
        return self.get_formatted_time()
    
    def get_skill_level_name(self, skill_level: int) -> str:
        """Получить название уровня навыка"""
        if skill_level <= 2:
            return tr("game_state.skill_level_novice", "Новичок")
        elif skill_level <= 4:
            return tr("game_state.skill_level_apprentice", "Ученик")
        elif skill_level <= 6:
            return tr("game_state.skill_level_experienced", "Опытный")
        elif skill_level <= 8:
            return tr("game_state.skill_level_expert", "Эксперт")
        else:
            return tr("game_state.skill_level_master", "Мастер")
    
    def get_stress_level(self) -> str:
        """Получить уровень стресса"""
        if self.stress <= 30:
            return tr("game_state.stress_low", "Низкий")
        elif self.stress <= 60:
            return tr("game_state.stress_medium", "Средний")
        elif self.stress <= 80:
            return tr("game_state.stress_high", "Высокий")
        else:
            return tr("game_state.stress_critical", "Критический")
    
    def get_energy_level(self) -> str:
        """Получить уровень энергии"""
        if self.energy <= 30:
            return tr("game_state.energy_low", "Низкий")
        elif self.energy <= 60:
            return tr("game_state.energy_medium", "Средний")
        elif self.energy <= 80:
            return tr("game_state.energy_high", "Высокий")
        else:
            return tr("game_state.energy_full", "Полный")
    
    def can_work(self) -> bool:
        """Может ли сотрудник работать"""
        return self.energy > 20 and self.stress < 80
    
    def pause_game_time(self):
        """Поставить игровое время на паузу"""
        self.game_time['is_paused'] = True
        self.time_paused = True
    
    def resume_game_time(self):
        """Возобновить игровое время"""
        self.game_time['is_paused'] = False
        self.time_paused = False
    
    def end_workday(self):
        """Окончание рабочего дня (вызывается автоматически при достижении 18:00)"""
        if not self.shift_started:
            return
        
        # Итоговая оплата за смену
        shift_bonus = self.tasks_completed * 1000
        self.money += shift_bonus
        
        # Переход к следующему дню
        self.day += 1
        
        # Сброс состояния
        self.shift_started = False
        self.current_task = ""
        self.current_task_progress = 0
        self.shift_time = 0
        self.energy = 100
        self.stress = 0
        self.tasks_completed = 0
        
        # Обновляем день в игровом времени
        self.game_time['day'] = self.day
        
        # Очищаем старые письма для нового дня
        self.email_system.clear_old_emails()
        self.email_system.emails_received_today = False
        self.email_system.mvd_email_read = False
        
        # Обновляем день в системе почты
        self.email_system.day = self.day
        
        return shift_bonus
    
    def end_shift(self):
        """Закончить смену (вручную)"""
        if not self.shift_started:
            return
        
        # Устанавливаем время на конец рабочего дня
        self.game_time['current_hour'] = self.game_time.get('workday_end', 18)
        self.game_time['current_minute'] = 0
        
        # Вызываем автоматическое завершение дня
        return self.end_workday()
    
    def get_statistics(self) -> dict:
        """Получить статистику игрока"""
        return {
            tr("game.statistics.name", "Имя"): self.player_name,
            tr("game.statistics.day", "День"): self.day,
            tr("game.statistics.tasks_completed", "Выполнено заданий"): self.tasks_completed,
            tr("game.statistics.reputation", "Репутация"): self.reputation,
            tr("game.statistics.balance", "Баланс"): self.get_money_display(),
            tr("game.statistics.shift_time", "Время смены"): self.get_formatted_time(),
            tr("game.statistics.energy", "Энергия"): f"{self.energy}% ({self.get_energy_level()})",
            tr("game.statistics.stress", "Стресс"): f"{self.stress}% ({self.get_stress_level()})",
            tr("game.statistics.unread_emails", "Непрочитанных писем"): self.unread_emails,
            tr("game.statistics.game_date", "Игровая дата"): self.get_formatted_date(),
            tr("game.statistics.shift_progress", "Прогресс смены"): f"{self.get_workday_progress():.1f}%",
            tr("game.statistics.skills", "Навыки"): {skill: f"{level}/10 ({self.get_skill_level_name(level)})" 
                      for skill, level in self.skills.items()}
        }