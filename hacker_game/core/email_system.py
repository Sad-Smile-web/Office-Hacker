# core/email_system.py

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import random
from datetime import datetime
from core.spam_generator import get_spam_generator
from core.email_templates import get_story_email_for_day, get_story_difficulty, get_story_deadline
from simple_translation import translation

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
            # Добавляем игрока в параметры, если его там нет
            if "player_name" in content_template and "player_name" not in self.parameters:
                # Попробуем достать имя игрока из других параметров
                pass
            
            return content_template.format(**self.parameters)
        except KeyError as e:
            print(f"Ошибка форматирования письма {self.id}: отсутствует ключ {e}")
            return content_template
        except Exception as e:
            print(f"Ошибка при форматировании письма {self.id}: {e}")
            return content_template
    
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
        self.mvd_email_read = False
        
        # НОВОЕ: отслеживание отправки специальных писем
        self.special_emails_sent = {
            "error_message": False,
        }
    
    def add_email(self, sender_key: str, subject_key: str, template_key: str, 
                  parameters: Dict[str, Any] = None, important: bool = False, 
                  is_spam: bool = False, spam_type: str = None) -> int:
        """Добавить новое письмо (сохраняем ключи, а не текст)"""
        if parameters is None:
            parameters = {}
        
        # Автоматически добавляем стандартные параметры
        parameters.setdefault("player_name", self.player_name)
        parameters.setdefault("day", self.day)
        parameters.setdefault("reputation", self.reputation)
        parameters.setdefault("money", self.money)
        
        email = Email(
            id=self.next_email_id,
            sender_key=sender_key,
            subject_key=subject_key,
            template_key=template_key,
            parameters=parameters,
            date=self._get_current_time(),
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
        if "mvd" in sender_key.lower() or "мвд" in sender_key.lower():
            self.mvd_email_read = False
        
        return email.id
    
    def add_template_email(self, template_name: str, **kwargs) -> int:
        """Добавить письмо из шаблона (с использованием ключей)"""
        # Ключи для шаблона
        sender_key = f"email.templates.{template_name}.sender"
        subject_key = f"email.templates.{template_name}.subject"
        template_key = f"email.templates.{template_name}.template"
        
        # Проверяем, есть ли такой шаблон
        if not translation.has_key(template_key):
            raise ValueError(translation.t("email.errors.template_not_found", 
                                         template=template_name, 
                                         default=f"Шаблон '{template_name}' не найден"))
        
        # Определяем важность письма
        important = template_name in ["mvd_mission", "mvd_mission_1_intro", 
                                     "mvd_mission_2_security_audit", "system_welcome"]
        
        # Добавляем параметры
        params = kwargs.copy()
        params.setdefault("player_name", self.player_name)
        params.setdefault("day", self.day)
        params.setdefault("reputation", self.reputation)
        params.setdefault("money", self.money)
        
        return self.add_email(
            sender_key=sender_key,
            subject_key=subject_key,
            template_key=template_key,
            parameters=params,
            important=important
        )
    
    def add_spam_email(self, spam_data: Dict) -> int:
        """Добавить спам-письмо"""
        return self.add_email(
            sender_key=spam_data["sender_key"],
            subject_key=spam_data["subject_key"],
            template_key=spam_data["template_key"],
            parameters=spam_data.get("parameters", {}),
            important=False,
            is_spam=True,
            spam_type=spam_data.get("type")
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
            raise ValueError(translation.t("email.errors.unknown_folder", 
                                         folder=folder, 
                                         default=f"Неизвестная папка: {folder}"))
    
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
            
            if "mvd" in email.sender_key.lower() or "мвд" in email.sender_key.lower():
                self.mvd_email_read = True
            
            return True
        return False
    
    def mark_as_unread(self, email_id: int) -> bool:
        """Пометить письмо как непрочитанное"""
        email = self.get_email_by_id(email_id)
        if email and email.read:
            email.read = False
            self.unread_emails += 1
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
        self.inbox = [email for email in self.inbox if email.important]
        self.sent = [email for email in self.sent if email.important]
        self.unread_emails = len([email for email in self.inbox if not email.read])
        
        # Сбрасываем флаги отправки специальных писем для нового дня
        self.special_emails_sent = {key: False for key in self.special_emails_sent}
        self.emails_received_today = False
    
    def add_initial_emails(self):
        """Добавить начальные письма"""
        self.clear_old_emails()
        
        # Письмо от МВД
        self.add_template_email("system_welcome")
        
        # Системное уведомление
        self.add_email(
            sender_key="email.templates.system_notification.sender",
            subject_key="email.system_notification.subject",
            template_key="email.system_notification.content",
            parameters={},
            important=False
        )
        
        self.emails_received_today = True
    
    def generate_daily_emails(self):
        """Сгенерировать ежедневные письма"""
        if not self.emails_received_today:
            # Отправляем сюжетное письмо для текущего дня
            story_template = get_story_email_for_day(self.day)
            if story_template:
                self.add_template_email(story_template)
            
            # Случайный спам (30% шанс)
            if random.random() < 0.3:
                spam_generator = get_spam_generator()
                spam_data = spam_generator.generate_spam_data(player_name=self.player_name)
                
                if spam_data:
                    self.add_spam_email(spam_data)
            
            self.emails_received_today = True
    
    def add_mission_email(self, mission_name: str, difficulty: str, deadline: str, description: str):
        """Добавить письмо с заданием"""
        return self.add_template_email(
            "mvd_mission",
            mission_name=mission_name,
            difficulty=difficulty,
            deadline=deadline,
            description=description
        )
    
    def add_system_notification(self, message: str, important: bool = False):
        """Добавить системное уведомление"""
        return self.add_email(
            sender_key="email.templates.system_notification.sender",
            subject_key="email.templates.system_notification.subject",
            template_key="email.templates.system_notification.template",
            parameters={
                "player_name": self.player_name,
                "subject": translation.t("email.templates.system_notification.subject", default="Уведомление"),
                "message": message
            },
            important=important
        )
    
    def _get_current_time(self) -> str:
        """Получить текущее время"""
        return datetime.now().strftime("%H:%M")
    
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
            "special_emails_sent": self.special_emails_sent,
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
        email_system.special_emails_sent = data.get("special_emails_sent", {"error_message": False})
        
        # Восстанавливаем письма
        for email_data in data.get("inbox", []):
            email_system.inbox.append(Email.from_dict(email_data))
        
        for email_data in data.get("sent", []):
            email_system.sent.append(Email.from_dict(email_data))
        
        for email_data in data.get("draft", []):
            email_system.draft.append(Email.from_dict(email_data))
        
        return email_system