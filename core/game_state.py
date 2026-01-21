# core/game_state.py

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple
import random
import time

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
    reputation: int = 0
    money: float = 500.0
    skills: Dict[str, int] = field(default_factory=dict)
    
    # Игровое время
    game_time: Dict = field(default_factory=dict)
    
    # Система почты
    email_system: EmailSystem = None
    
    # Конфигурация специальных писем
    special_emails_config: Dict = field(default_factory=dict)
    
    # Время на паузе
    time_paused: bool = False
    
    # Флаги отправки писем
    error_email_sent: bool = False
    mvd_mission_email_sent: bool = False
    welcome_email_sent: bool = False
    
    # Флаг показа кат-сцены
    cutscene_shown: bool = False
    
    # Слот сохранения
    save_slot: int = 0
    
    # ДЛЯ ПОЧАСОВОГО СПАМА
    last_hour_checked: int = 9
    spam_cooldown: Dict[str, int] = field(default_factory=dict)
    spam_types_sent_today: set = field(default_factory=set)
    
    # СТАТИСТИКА
    shift_time: int = 0
    energy: int = 100
    stress: int = 0
    
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
        
        # Инициализация игрового времени
        if not self.game_time:
            self.game_time = {
                'current_hour': 9,
                'current_minute': 0,
                'day': self.day,
                'month': 1,
                'year': 2140,
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
                    "required_time": 30,
                    "description": tr("game_state.special_email_config", "Письмо ERROR - отправляется через 30 минут игрового времени после выполнения первой задачи")
                },
                "mvd_mission_1_intro": {
                    "enabled": True,
                    "required_tasks": 1,
                    "required_time": 30,
                    "description": tr("game_state.special_email_config", "Первое задание МВД - отправляется через 30 минут игрового времени после выполнения первой задачи")
                }
            }
        
        # Инициализация save_slot если его нет
        if not hasattr(self, 'save_slot'):
            self.save_slot = 0
        
        # Инициализация полей для почасового спама
        if not hasattr(self, 'last_hour_checked'):
            self.last_hour_checked = 9
        
        if not hasattr(self, 'spam_cooldown'):
            self.spam_cooldown = {}
        
        if not hasattr(self, 'spam_types_sent_today'):
            self.spam_types_sent_today = set()
        
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
        """Количество непрочитанных писем"""
        return self.email_system.get_unread_count() if self.email_system else 0
    
    @property
    def mvd_email_read(self):
        """Флаг прочтения письма от МВД"""
        return self.email_system.mvd_email_read if self.email_system else False
    
    def start_new_shift(self):
        """Начать новую смену"""
        return self.start_shift()
    
    def start_shift(self):
        """Начать смену"""
        self.shift_started = True
        self.shift_time = 0
        self.energy = 100
        self.stress = 0
        self.error_email_sent = False
        self.mvd_mission_email_sent = False
        self.welcome_email_sent = False
        
        # Сбрасываем статистику спама для нового дня
        self.spam_types_sent_today = set()
        
        # Сброс игрового времени на начало смены (9:00)
        self.game_time.update({
            'current_hour': 9,
            'current_minute': 0,
            'day': self.day,
            'is_paused': False,
            'year': 2140
        })
        
        # Отправляем приветственное письмо сразу
        if not self.welcome_email_sent and self.email_system:
            self.email_system.add_template_email("system_welcome")
            self.welcome_email_sent = True
            print("[ИГРА] Отправлено приветственное письмо")
    
    def save(self, slot: int = None):
        """Сохранить игру"""
        # Если слот не указан, используем текущий save_slot
        if slot is None:
            slot = self.save_slot
            
        filename = f"saves/slot_{slot}.json"
        os.makedirs("saves", exist_ok=True)
        
        # Обновляем слот сохранения
        self.save_slot = slot
        
        # Создаем словарь для сохранения
        data = {}
        
        # Сохраняем основные поля
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['day'] = self.day
        data['shift_started'] = self.shift_started
        data['reputation'] = self.reputation
        data['money'] = self.money
        data['skills'] = self.skills
        data['game_time'] = self.game_time
        data['time_paused'] = self.time_paused
        data['error_email_sent'] = self.error_email_sent
        data['mvd_mission_email_sent'] = self.mvd_mission_email_sent
        data['welcome_email_sent'] = self.welcome_email_sent
        data['cutscene_shown'] = self.cutscene_shown
        data['save_slot'] = self.save_slot
        data['last_hour_checked'] = self.last_hour_checked
        data['spam_cooldown'] = self.spam_cooldown
        data['spam_types_sent_today'] = list(self.spam_types_sent_today)
        data['special_emails_config'] = self.special_emails_config
        data['shift_time'] = self.shift_time
        data['energy'] = self.energy
        data['stress'] = self.stress
        
        # Сохраняем систему почты
        if self.email_system:
            data["email_system"] = self.email_system.to_dict()
        
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
                    
                    # Преобразуем spam_types_sent_today из list обратно в set
                    if 'spam_types_sent_today' in data and isinstance(data['spam_types_sent_today'], list):
                        data['spam_types_sent_today'] = set(data['spam_types_sent_today'])
                    
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
                    
                    # Обработка системы почты
                    email_system_data = data.get('email_system')
                    email_system = None
                    if email_system_data:
                        email_system = EmailSystem.from_dict(email_system_data)
                    data['email_system'] = email_system
                    
                    # Добавляем недостающие поля для совместимости
                    default_fields = [
                        ('shift_time', 0),
                        ('energy', 100),
                        ('stress', 0),
                        ('time_paused', False),
                        ('error_email_sent', False),
                        ('mvd_mission_email_sent', False),
                        ('welcome_email_sent', False),
                        ('save_slot', slot),
                        ('last_hour_checked', 9),
                        ('spam_cooldown', {}),
                        ('spam_types_sent_today', set()),
                        ('cutscene_shown', False),
                        ('special_emails_config', {
                            "error_message": {
                                "enabled": True,
                                "required_tasks": 1,
                                "required_time": 30,
                                "description": tr("game_state.special_email_config", "Письмо ERROR - отправляется через 30 минут игрового времени после выполнения первой задачи")
                            },
                            "mvd_mission_1_intro": {
                                "enabled": True,
                                "required_tasks": 1,
                                "required_time": 30,
                                "description": tr("game_state.special_email_config", "Первое задание МВД - отправляется через 30 минут игрового времени после выполнения первой задачи")
                            }
                        })
                    ]
                    
                    for field_name, default_value in default_fields:
                        if field_name not in data:
                            data[field_name] = default_value
                    
                    # Загружаем игровое время
                    if 'game_time' not in data:
                        data['game_time'] = {
                            'current_hour': 9,
                            'current_minute': 0,
                            'day': data.get('day', 1),
                            'month': 1,
                            'year': 2140,
                            'is_paused': False,
                            'time_speed': 1.0,
                            'workday_start': 9,
                            'workday_end': 18
                        }
                    else:
                        # Обновляем год для старых сохранений
                        if data['game_time'].get('year', 1984) == 1984:
                            data['game_time']['year'] = 2140
                        # Обновляем скорость времени
                        if data['game_time'].get('time_speed', 6.0) != 1.0:
                            data['game_time']['time_speed'] = 1.0
                    
                    # Создаем экземпляр GameState
                    game_state = cls(
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''),
                        day=data.get('day', 1),
                        shift_started=data.get('shift_started', False),
                        reputation=data.get('reputation', 0),
                        money=data.get('money', 500.0),
                        skills=data.get('skills', {}),
                        game_time=data.get('game_time', {}),
                        time_paused=data.get('time_paused', False),
                        error_email_sent=data.get('error_email_sent', False),
                        mvd_mission_email_sent=data.get('mvd_mission_email_sent', False),
                        welcome_email_sent=data.get('welcome_email_sent', False),
                        cutscene_shown=data.get('cutscene_shown', False),
                        save_slot=data.get('save_slot', slot),
                        last_hour_checked=data.get('last_hour_checked', 9),
                        spam_cooldown=data.get('spam_cooldown', {}),
                        spam_types_sent_today=data.get('spam_types_sent_today', set()),
                        special_emails_config=data.get('special_emails_config', {}),
                        email_system=data.get('email_system'),
                        shift_time=data.get('shift_time', 0),
                        energy=data.get('energy', 100),
                        stress=data.get('stress', 0)
                    )
                    
                    return game_state
                    
            except Exception as e:
                print(tr("game.load_error", "[ОШИБКА] Не удалось загрузить сохранение: {error}").format(error=e))
                game_state = cls()
                game_state.save_slot = slot
                return game_state
        else:
            print(tr("game.save_not_found", "[ИНФО] Сохранение не найдено: {filename}").format(filename=filename))
            game_state = cls()
            game_state.save_slot = slot
            return game_state
    
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
    
    def update_time(self, minutes: int = 1):
        """Обновить игровое время на указанное количество минут"""
        if self.game_time.get('is_paused', False):
            return
        
        # Сохраняем предыдущий час для проверки смены часа
        previous_hour = self.game_time.get('current_hour', 9)
        
        # Учитываем ускорение времени
        time_multiplier = self.game_time.get('time_speed', 1.0)
        adjusted_minutes = int(minutes * time_multiplier)
        
        self.game_time['current_minute'] += adjusted_minutes
        self.shift_time += adjusted_minutes
        
        # Проверка переполнения минут
        if self.game_time['current_minute'] >= 60:
            self.game_time['current_minute'] = 0
            self.game_time['current_hour'] += 1
            
            # ПРОВЕРКА ПОЧАСОВОГО СПАМА
            self.check_hourly_spam(previous_hour)
            
            # Проверка окончания рабочего дня
            if self.game_time['current_hour'] >= self.game_time.get('workday_end', 18):
                # Конец рабочего дня
                self.end_workday()
            
            # Смена дня
            if self.game_time['current_hour'] >= 24:
                self.game_time['current_hour'] = 0
                self.game_time['day'] += 1
                
                # Сбрасываем статистику спама при смене дня
                self.spam_types_sent_today = set()
                
                # Упрощенная логика месяцев
                if self.game_time['day'] > 30:
                    self.game_time['day'] = 1
                    self.game_time['month'] += 1
                    
                    if self.game_time['month'] > 12:
                        self.game_state['month'] = 1
                        self.game_time['year'] += 1
        
        # Отправляем письмо от МВД через 60 минут
        if not self.mvd_mission_email_sent and self.shift_time >= 60:
            if self.email_system:
                self.email_system.add_template_email("mvd_mission_1_intro", date=self.get_formatted_time())
                self.mvd_mission_email_sent = True
                print("[ИГРА] Отправлено письмо от МВД (через 60 минут)")
    
    def check_hourly_spam(self, previous_hour: int):
        """Проверить возможность отправки спама в начале каждого часа"""
        current_hour = self.game_time.get('current_hour', 9)
        
        # Проверяем, сменился ли час
        if current_hour != previous_hour:
            
            # Не отправляем спам вне рабочего времени (9-18) или в первый день
            if not (9 <= current_hour < 18) or self.day == 1:
                return
            
            # 20% шанс на спам каждый час
            if random.random() < 0.2:
                self.send_hourly_spam_email()
            
            # Обновляем последний проверенный час
            self.last_hour_checked = current_hour
    
    def send_hourly_spam_email(self):
        """Отправить спам-письмо в текущий час"""
        if not hasattr(self, 'email_system') or self.email_system is None:
            return
        
        # Получаем генератор спама
        from core.spam_generator import get_spam_generator
        spam_generator = get_spam_generator()
        
        # Генерируем спам
        spam_data = spam_generator.generate_spam_data(
            player_name=self.player_name,
            avoid_recent=True
        )
        
        if spam_data:
            # Проверяем кд для этого типа спама
            spam_type = spam_data.get("type", "")
            
            # Не отправляем один и тот же тип спама чаще чем раз в 3 часа
            if spam_type in self.spam_cooldown:
                hours_since_last = self.game_time.get('current_hour', 9) - self.spam_cooldown[spam_type]
                if hours_since_last < 3:
                    return
            
            # Не отправляем более 3 разных типов спама за день
            if spam_type in self.spam_types_sent_today:
                return
            
            if len(self.spam_types_sent_today) >= 3:
                return
            
            # Добавляем письмо с текущим игровым временем
            spam_data["date"] = self.get_formatted_time()
            email_id = self.email_system.add_spam_email(spam_data)
            
            # Обновляем кд и статистику
            self.spam_cooldown[spam_type] = self.game_time.get('current_hour', 9)
            self.spam_types_sent_today.add(spam_type)
            
            print(f"[СПАМ] Отправлено письмо типа '{spam_type}' в {self.get_formatted_time()}")
            return email_id
        
        return None
    
    def mark_email_as_read(self, email_id: int):
        """Пометить письмо как прочитанное"""
        print(f"[GAME_STATE] mark_email_as_read для письма {email_id}")
        
        if not self.email_system:
            return False
        
        email = self.email_system.get_email_by_id(email_id)
        if not email:
            return False
        
        # Помечаем письмо как прочитанное в системе
        if self.email_system.mark_as_read(email_id):
            print(f"[GAME_STATE] Письмо {email_id} помечено как прочитанное")
            return {"status": "email_marked_read", "email_id": email_id}
        
        return False
    
    def get_formatted_time(self):
        """Получить отформатированное время"""
        hour = self.game_time.get('current_hour', 9)
        minute = self.game_time.get('current_minute', 0)
        return f"{hour:02d}:{minute:02d}"
    
    def get_formatted_date(self):
        """Получить отформатированную дату"""
        day = self.game_time.get('day', self.day)
        month = self.game_time.get('month', 1)
        year = self.game_time.get('year', 2140)
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
        
        return min(100, max(0, progress))
    
    def add_new_email(self, sender: str, subject: str, content: str, important: bool = False):
        """Добавить новое письмо"""
        return self.email_system.add_email(sender, subject, content, important)
    
    def get_current_time(self):
        """Получить текущее игровое время"""
        return self.get_formatted_time()
    
    def take_break(self):
        """Сделать перерыв"""
        if not self.shift_started:
            return False
        
        self.update_time(15)
        
        energy_restored = random.randint(20, 40)
        self.energy = min(100, self.energy + energy_restored)
        
        stress_reduced = random.randint(10, 25)
        self.stress = max(0, self.stress - stress_reduced)
        
        return True
    
    def get_money_display(self):
        """Получить отформатированную строку с деньгами"""
        return f"{self.money:,.2f} ₽".replace(',', ' ')
    
    def get_shift_time_display(self):
        """Получить отформатированное время смены"""
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
        """Окончание рабочего дня"""
        if not self.shift_started:
            return
        
        # Сбрасываем статистику спама
        self.spam_types_sent_today = set()
        
        shift_bonus = 1000  # Фиксированный бонус за смену
        self.money += shift_bonus
        
        self.day += 1
        
        self.shift_started = False
        self.shift_time = 0
        self.energy = 100
        self.stress = 0
        self.error_email_sent = False
        self.mvd_mission_email_sent = False
        self.welcome_email_sent = False
        
        self.game_time['day'] = self.day
        
        self.email_system.clear_old_emails()
        self.email_system.emails_received_today = False
        self.email_system.mvd_email_read = False
        
        self.email_system.day = self.day
        
        return shift_bonus
    
    def end_shift(self):
        """Закончить смену"""
        if not self.shift_started:
            return
        
        self.game_time['current_hour'] = self.game_time.get('workday_end', 18)
        self.game_time['current_minute'] = 0
        
        return self.end_workday()
    
    def get_statistics(self) -> dict:
        """Получить статистику игрока"""
        return {
            tr("game.statistics.name", "Имя"): self.player_name,
            tr("game.statistics.day", "День"): self.day,
            tr("game.statistics.reputation", "Репутация"): self.reputation,
            tr("game.statistics.balance", "Баланс"): self.get_money_display(),
            tr("game.statistics.shift_time", "Время смены"): self.get_formatted_time(),
            tr("game.statistics.energy", "Энергия"): f"{self.energy}% ({self.get_energy_level()})",
            tr("game.statistics.stress", "Стресс"): f"{self.stress}% ({self.get_stress_level()})",
            tr("game.statistics.unread_emails", "Непрочитанных писем"): self.unread_emails,
            tr("game.statistics.game_date", "Игровая дата"): self.get_formatted_date(),
            tr("game.statistics.shift_progress", "Прогресс смены"): f"{self.get_workday_progress():.1f}%",
            tr("game.statistics.skills", "Навыки"): {skill: f"{level}/10 ({self.get_skill_level_name(level)})" 
                      for skill, level in self.skills.items()},
            tr("game.statistics.cutscene_shown", "Кат-сцена показана"): 
                tr("game.yes", "Да") if self.cutscene_shown else tr("game.no", "Нет"),
            tr("game.statistics.save_slot", "Слот сохранения"): self.save_slot
        }
    
    def mark_cutscene_shown(self):
        """Отметить, что кат-сцена была показана"""
        self.cutscene_shown = True
        print(tr("game.cutscene_shown", "[ИГРА] Кат-сцена отмечена как показанная"))
    
    def should_show_cutscene(self) -> bool:
        """Нужно ли показывать кат-сцену"""
        return not self.cutscene_shown and bool(self.player_name.strip())
    
    def get_cutscene_texts(self) -> Tuple[str, str]:
        """
        Получить тексты для кат-сцены
        """
        full_story = tr("cutscene.default_story", "")
        
        if not full_story:
            full_story = """Год 2140. Мир изменился.

После многолетней войны власть сосредоточилась в руках большой корпорации.
SIBERIA-SOFTWARE стала самой наикрупнейшей корпорацией, контролируя 99% киберпространства Евразии.

Ты — новый сотрудник Отдела Кибербезопасности МВД.
Твоя задача — мониторить сетевую активность, отслеживать угрозы и обеспечивать безопасность граждан.
Так же твой задачей является сообщать о странных личностях.

Но в цифровом мире не всё так просто...
Тени скрываются за каждым байтом, секреты — за каждым протоколом.

Сегодня твой первый день.
Система ждет твоего входа.

Добро пожаловать в корпорацию SIBERIA-SOFTWARE."""
        
        lines = [line.strip() for line in full_story.strip().split('\n') if line.strip()]
        
        if len(lines) > 0:
            final_phrase = lines[-1]
            main_story = '\n\n'.join(lines[:-1])
        else:
            main_story = ""
            final_phrase = ""
        
        return main_story, final_phrase
    
    def is_workday_over(self):
        """Проверка, закончился ли рабочий день"""
        current_hour = self.game_time.get('current_hour', 9)
        workday_end = self.game_time.get('workday_end', 18)
        return current_hour >= workday_end