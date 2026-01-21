# core/email_system.py

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import random
from datetime import datetime
from core.email_templates import get_story_email_for_day, get_story_difficulty, get_story_deadline
from simple_translation import translation
import re


@dataclass
class Email:
    """Класс для представления электронного письма"""
    id: int
    sender_key: str  # Ключ отправителя
    subject_key: str  # Ключ темы
    template_key: str  # Ключ шаблона
    parameters: Dict[str, Any]  # Параметры для форматирования
    date: str
    read: bool = False
    important: bool = False
    is_spam: bool = False  # Флаг спам-письма
    spam_type: Optional[str] = None  # Тип спама (если спам)
    
    def get_sender(self) -> str:
        """Получить отправителя с учетом перевода"""
        return translation.t(self.sender_key, default="Unknown Sender")
    
    def get_subject(self) -> str:
        """Получить тему с учетом перевода"""
        return translation.t(self.subject_key, default="No Subject")
    
    def get_content(self) -> str:
        """Получить содержимое с учетом перевода и параметров"""
        content_template = translation.t(self.template_key, default="")
        if not content_template:
            return f"[Translation error for key: {self.template_key}]"
        
        try:
            # Форматируем с параметрами
            return content_template.format(**self.parameters)
        except KeyError as e:
            print(f"Ошибка форматирования письма {self.id}: отсутствует ключ {e}")
            return content_template
        except Exception as e:
            print(f"Ошибка при форматировании письма {self.id}: {e}")
            return content_template
    
    def get_html_content(self) -> str:
        """Получить содержимое письма в HTML формате с поддержкой ссылок"""
        content = self.get_content()
        
        # Проверяем, есть ли в контенте HTML теги
        if '<' in content and '>' in content:
            # В контенте уже есть HTML, возвращаем как есть
            html_content = content
        else:
            # Нет HTML тегов, преобразуем ссылки и добавляем форматирование
            # Преобразуем app.cyb ссылки в HTML ссылки
            pattern = r'(app\.cyb://[^\s<]+)'
            html_content = re.sub(pattern, r'<a href="\1" style="color:#00ffff; text-decoration:none;">\1</a>', content)
            
            # Заменяем переносы строк на <br>
            html_content = html_content.replace('\n', '<br>')
        
        # Оборачиваем в div с базовыми стилями
        final_html = f"""
        <div style="font-family: 'Courier New', monospace; color: #cccccc; line-height: 1.6;">
            {html_content}
        </div>
        """
        return final_html
    
    def is_mvd_email(self) -> bool:
        """Проверить, является ли письмо от МВД"""
        mvd_keywords = ["мвд", "mvd", "министерство", "министерства"]
        return any(keyword in self.sender_key.lower() for keyword in mvd_keywords)
    
    def to_dict(self) -> dict:
        """Преобразовать письмо в словарь"""
        return {
            "id": self.id,
            "sender_key": self.sender_key,
            "subject_key": self.subject_key,
            "template_key": self.template_key,
            "parameters": self.parameters,
            "date": self.date,
            "read": self.read,
            "important": self.important,
            "is_spam": self.is_spam,
            "spam_type": self.spam_type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Email':
        """Создать письмо из словаря"""
        return cls(
            id=data.get("id", 0),
            sender_key=data.get("sender_key", ""),
            subject_key=data.get("subject_key", ""),
            template_key=data.get("template_key", ""),
            parameters=data.get("parameters", {}),
            date=data.get("date", ""),
            read=data.get("read", False),
            important=data.get("important", False),
            is_spam=data.get("is_spam", False),
            spam_type=data.get("spam_type", None)
        )


class EmailSystem:
    """Система управления почтой"""
    
    def __init__(self, player_name: str = "", day: int = 1, reputation: int = 0, money: float = 0.0):
        self.player_name = player_name
        self.day = day
        self.reputation = reputation
        self.money = money
        
        self.inbox: List[Email] = []
        self.sent: List[Email] = []
        self.draft: List[Email] = []
        
        self.next_email_id = 1
        self.unread_emails = 0
        self.emails_received_today = False
        self.mvd_email_read = False  # Флаг прочтения письма от МВД
        
        # НЕ ИСПОЛЬЗУЕМ СТАРУЮ СИСТЕМУ СПЕЦИАЛЬНЫХ ПИСЕМ
        # Теперь сюжетные письма будут генерироваться через email_templates
    
    def add_email(self, sender_key: str, subject_key: str, template_key: str, 
                  parameters: Dict[str, Any] = None, important: bool = False, 
                  is_spam: bool = False, spam_type: str = None, date: str = None) -> int:
        """Добавить новое письмо"""
        if parameters is None:
            parameters = {}
        
        # Автоматически добавляем стандартные параметры
        parameters.setdefault("player_name", self.player_name)
        parameters.setdefault("day", self.day)
        parameters.setdefault("reputation", self.reputation)
        parameters.setdefault("money", self.money)
        
        # Используем переданное время или генерируем случайное
        email_date = date if date is not None else self._generate_random_time()
        
        email = Email(
            id=self.next_email_id,
            sender_key=sender_key,
            subject_key=subject_key,
            template_key=template_key,
            parameters=parameters,
            date=email_date,
            read=False,
            important=important,
            is_spam=is_spam,
            spam_type=spam_type
        )
        
        self.inbox.append(email)
        self.next_email_id += 1
        
        if not email.read:
            self.unread_emails += 1
        
        # Проверяем, является ли это письмо от МВД
        if email.is_mvd_email():
            # Если это первое письмо от МВД, ставим флаг, что оно еще не прочитано
            # (потому что только что добавлено и read=False)
            pass
        
        print(f"[EMAIL] Добавлено письмо: {email.get_subject()} от {email.get_sender()}")
        return email.id
    
    def add_template_email(self, template_name: str, **kwargs) -> int:
        """Добавить письмо из шаблона"""
        # Ключи для шаблона
        sender_key = f"email.templates.{template_name}.sender"
        subject_key = f"email.templates.{template_name}.subject"
        template_key = f"email.templates.{template_name}.template"
        
        # Проверяем, есть ли такой шаблон
        if not translation.has_key(template_key):
            print(f"[EMAIL] Шаблон '{template_name}' не найден")
            # Создаем заглушку
            sender_key = "email.templates.system_notification.sender"
            subject_key = f"email.errors.template_not_found"
            template_key = "email.errors.template_not_found_template"
        
        # Определяем важность письма
        important = template_name in ["mvd_mission", "mvd_mission_1_intro", 
                                     "mvd_mission_2_security_audit", "system_welcome"]
        
        # Добавляем параметры
        params = kwargs.copy()
        params.setdefault("player_name", self.player_name)
        params.setdefault("day", self.day)
        params.setdefault("reputation", self.reputation)
        params.setdefault("money", self.money)
        
        # Извлекаем переданное время, если есть
        date = kwargs.get('date')
        
        return self.add_email(
            sender_key=sender_key,
            subject_key=subject_key,
            template_key=template_key,
            parameters=params,
            important=important,
            date=date
        )
    
    def add_spam_email(self, spam_data: Dict) -> int:
        """Добавить спам-письмо"""
        # Извлекаем дату из spam_data, если есть
        date = spam_data.get("date")
        
        return self.add_email(
            sender_key=spam_data["sender_key"],
            subject_key=spam_data["subject_key"],
            template_key=spam_data["template_key"],
            parameters=spam_data.get("parameters", {}),
            important=False,
            is_spam=True,
            spam_type=spam_data.get("type"),
            date=date
        )
    
    def get_emails(self, folder: str = "inbox") -> List[Email]:
        """Получить письма из указанной папки"""
        if folder == "inbox":
            return self.inbox
        elif folder == "sent":
            return self.sent
        elif folder == "draft":
            return self.draft
        else:
            print(f"[EMAIL] Неизвестная папка: {folder}")
            return []
    
    def get_email_by_id(self, email_id: int) -> Optional[Email]:
        """Найти письмо по ID"""
        for email in self.inbox + self.sent + self.draft:
            if email.id == email_id:
                return email
        return None
    
    def mark_as_read(self, email_id: int) -> bool:
        """Пометить письмо как прочитанное"""
        email = self.get_email_by_id(email_id)
        if email and not email.read:
            email.read = True
            self.unread_emails -= 1
            
            # Проверяем, является ли это письмо от МВД
            if email.is_mvd_email():
                self.mvd_email_read = True
                print(f"[EMAIL] Письмо от МВД отмечено как прочитанное")
            
            print(f"[EMAIL] Письмо {email_id} отмечено как прочитанное")
            return True
        
        print(f"[EMAIL] Не удалось отметить письмо {email_id} как прочитанное")
        return False
    
    def mark_as_unread(self, email_id: int) -> bool:
        """Пометить письмо как непрочитанное"""
        email = self.get_email_by_id(email_id)
        if email and email.read:
            email.read = False
            self.unread_emails += 1
            
            # Если это письмо от МВД, снимаем флаг
            if email.is_mvd_email():
                self.mvd_email_read = False
            
            return True
        return False
    
    def delete_email(self, email_id: int) -> bool:
        """Удалить письмо"""
        # Ищем во всех папках
        for folder in [self.inbox, self.sent, self.draft]:
            for i, email in enumerate(folder):
                if email.id == email_id:
                    if not email.read:
                        self.unread_emails -= 1
                    del folder[i]
                    print(f"[EMAIL] Письмо {email_id} удалено")
                    return True
        return False
    
    def get_unread_count(self) -> int:
        """Получить количество непрочитанных писем"""
        return self.unread_emails
    
    def get_total_count(self) -> int:
        """Получить общее количество писем"""
        return len(self.inbox) + len(self.sent) + len(self.draft)
    
    def clear_old_emails(self, days_old: int = 7):
        """Очистить старые письма"""
        # Пока просто очищаем все, кроме важных
        old_count = len(self.inbox)
        self.inbox = [email for email in self.inbox if email.important]
        self.sent = [email for email in self.sent if email.important]
        self.unread_emails = len([email for email in self.inbox if not email.read])
        
        print(f"[EMAIL] Очищено {old_count - len(self.inbox)} старых писем")
        
        # Сбрасываем флаги для нового дня
        self.emails_received_today = False
        # НЕ сбрасываем mvd_email_read - это состояние сохраняется
    
    def add_initial_emails(self):
        """Добавить начальные письма"""
        if self.emails_received_today:
            print(f"[EMAIL] Письма уже были добавлены сегодня")
            return
        
        self.clear_old_emails()
        
        # 1. Системное приветствие (не от МВД, но важное)
        print("[EMAIL] Добавляем системное приветствие")
        self.add_template_email("system_welcome")
        
        # 2. Срочное письмо от МВД (самое важное, должно быть первым)
        print("[EMAIL] Добавляем письмо от МВД")
        self.add_template_email("mvd_mission_1_intro")
        
        # 3. Системное уведомление (неважное)
        print("[EMAIL] Добавляем системное уведомление")
        self.add_email(
            sender_key="email.templates.system_notification.sender",
            subject_key="email.system_notification.subject",
            template_key="email.system_notification.content",
            parameters={
                "player_name": self.player_name,
                "subject": translation.t("email.system_notification.subject", default="Уведомление"),
                "message": translation.t("email.welcome_message", 
                    default=f"Добро пожаловать в систему, {self.player_name}. Сегодня ваш первый день.")
            },
            important=False
        )
        
        self.emails_received_today = True
        print(f"[EMAIL] Добавлено {len(self.inbox)} начальных писем")
    
    def generate_daily_emails(self):
        """Сгенерировать ежедневные письма"""
        if self.emails_received_today:
            print(f"[EMAIL] Письма уже сгенерированы сегодня")
            return
        
        print(f"[EMAIL] Генерация писем для дня {self.day}")
        
        # 1. Сюжетное письмо для текущего дня (если есть)
        story_template = get_story_email_for_day(self.day)
        if story_template:
            print(f"[EMAIL] Добавляем сюжетное письмо: {story_template}")
            self.add_template_email(story_template)
        
        # 2. Случайный спам (30% шанс)
        if random.random() < 0.3:
            print(f"[EMAIL] Генерируем спам-письмо")
            try:
                from core.spam_generator import get_spam_generator
                spam_generator = get_spam_generator()
                spam_data = spam_generator.generate_spam_data(player_name=self.player_name)
                
                if spam_data:
                    self.add_spam_email(spam_data)
            except ImportError:
                print("[EMAIL] Модуль spam_generator не найден, пропускаем спам")
        
        # 3. Системное уведомление (50% шанс)
        if random.random() < 0.5:
            print(f"[EMAIL] Добавляем системное уведомление")
            notifications = [
                "email.system_notification.database_update",
                "email.system_notification.security_scan",
                "email.system_notification.network_maintenance"
            ]
            
            notification_key = random.choice(notifications)
            self.add_email(
                sender_key="email.templates.system_notification.sender",
                subject_key=notification_key + ".subject",
                template_key=notification_key + ".content",
                parameters={
                    "player_name": self.player_name,
                    "day": self.day
                },
                important=False
            )
        
        self.emails_received_today = True
        print(f"[EMAIL] Сгенерировано {len(self.inbox)} писем")
    
    def add_mission_email(self, mission_name: str, difficulty: str, deadline: str, description: str):
        """Добавить письмо с заданием"""
        print(f"[EMAIL] Добавляем письмо с заданием: {mission_name}")
        return self.add_template_email(
            "mvd_mission",
            mission_name=mission_name,
            difficulty=difficulty,
            deadline=deadline,
            description=description
        )
    
    def add_system_notification(self, message: str, important: bool = False, date: str = None):
        """Добавить системное уведомление"""
        print(f"[EMAIL] Добавляем системное уведомление: {message[:50]}...")
        return self.add_email(
            sender_key="email.templates.system_notification.sender",
            subject_key="email.templates.system_notification.subject",
            template_key="email.templates.system_notification.template",
            parameters={
                "player_name": self.player_name,
                "subject": translation.t("email.templates.system_notification.subject", default="Уведомление"),
                "message": message
            },
            important=important,
            date=date
        )
    
    def _generate_random_time(self) -> str:
        """Сгенерировать случайное время в формате ЧЧ:ММ"""
        hour = random.randint(9, 17)  # Рабочее время
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"
    
    def _get_current_time(self) -> str:
        """Получить текущее время (только часы:минуты)"""
        return datetime.now().strftime("%H:%M")
    
    def has_unread_mvd_emails(self) -> bool:
        """Есть ли непрочитанные письма от МВД"""
        for email in self.inbox:
            if email.is_mvd_email() and not email.read:
                return True
        return False
    
    def has_read_mvd_emails(self) -> bool:
        """Есть ли прочитанные письма от МВД"""
        for email in self.inbox:
            if email.is_mvd_email() and email.read:
                return True
        return False
    
    def get_mvd_emails(self) -> List[Email]:
        """Получить все письма от МВД"""
        return [email for email in self.inbox if email.is_mvd_email()]
    
    def to_dict(self) -> dict:
        """Преобразовать систему в словарь для сохранения"""
        return {
            "inbox": [email.to_dict() for email in self.inbox],
            "sent": [email.to_dict() for email in self.sent],
            "draft": [email.to_dict() for email in self.draft],
            "next_email_id": self.next_email_id,
            "unread_emails": self.unread_emails,
            "emails_received_today": self.emails_received_today,
            "mvd_email_read": self.mvd_email_read,
            "player_name": self.player_name,
            "day": self.day,
            "reputation": self.reputation,
            "money": self.money
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EmailSystem':
        """Создать систему из словаря"""
        email_system = cls(
            player_name=data.get("player_name", ""),
            day=data.get("day", 1),
            reputation=data.get("reputation", 0),
            money=data.get("money", 0.0)
        )
        
        email_system.next_email_id = data.get("next_email_id", 1)
        email_system.unread_emails = data.get("unread_emails", 0)
        email_system.emails_received_today = data.get("emails_received_today", False)
        email_system.mvd_email_read = data.get("mvd_email_read", False)
        
        # Восстанавливаем письма
        for email_data in data.get("inbox", []):
            email_system.inbox.append(Email.from_dict(email_data))
        
        for email_data in data.get("sent", []):
            email_system.sent.append(Email.from_dict(email_data))
        
        for email_data in data.get("draft", []):
            email_system.draft.append(Email.from_dict(email_data))
        
        print(f"[EMAIL] Загружено {len(email_system.inbox)} писем, непрочитанных: {email_system.unread_emails}")
        return email_system