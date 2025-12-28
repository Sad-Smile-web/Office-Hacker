"""
Генератор спам-писем для игры Office Hacker
Система предотвращает частые повторения и создает разнообразный спам
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from simple_translation import translation


class SpamGenerator:
    """Генератор разнообразных спам-писем"""
    
    def __init__(self):
        self.spam_templates = self._init_spam_templates()
        self.last_sent_spam = []  # История отправленных спам-писем
        self.max_history_size = 10  # Максимальный размер истории
        
        # Вероятности различных типов спама
        self.spam_probabilities = {
            "advertisement": 0.4,      # 40% - реклама
            "scam": 0.3,               # 30% - мошенничество
            "notification": 0.2,        # 20% - уведомления
            "personal": 0.1             # 10% - персональные
        }
    
    def _init_spam_templates(self) -> Dict[str, List[Dict]]:
        """Инициализировать шаблоны спам-писем"""
        return {
            "advertisement": [
                {
                    "sender_key": "spam.advertisement.megamarket.sender",
                    "subject_key": "spam.advertisement.megamarket.subject",
                    "template_key": "spam.advertisement.megamarket.template"
                },
                {
                    "sender_key": "spam.advertisement.technomir.sender",
                    "subject_key": "spam.advertisement.technomir.subject",
                    "template_key": "spam.advertisement.technomir.template"
                },
                {
                    "sender_key": "spam.advertisement.online_cinema.sender",
                    "subject_key": "spam.advertisement.online_cinema.subject",
                    "template_key": "spam.advertisement.online_cinema.template"
                },
                {
                    "sender_key": "spam.advertisement.fitness_center.sender",
                    "subject_key": "spam.advertisement.fitness_center.subject",
                    "template_key": "spam.advertisement.fitness_center.template"
                }
            ],
            "scam": [
                {
                    "sender_key": "spam.scam.fast_loan.sender",
                    "subject_key": "spam.scam.fast_loan.subject",
                    "template_key": "spam.scam.fast_loan.template"
                },
                {
                    "sender_key": "spam.scam.cybersecurity.sender",
                    "subject_key": "spam.scam.cybersecurity.subject",
                    "template_key": "spam.scam.cybersecurity.template"
                },
                {
                    "sender_key": "spam.scam.lottery.sender",
                    "subject_key": "spam.scam.lottery.subject",
                    "template_key": "spam.scam.lottery.template"
                },
                {
                    "sender_key": "spam.scam.investments.sender",
                    "subject_key": "spam.scam.investments.subject",
                    "template_key": "spam.scam.investments.template"
                }
            ],
            "notification": [
                {
                    "sender_key": "spam.notification.social_network.sender",
                    "subject_key": "spam.notification.social_network.subject",
                    "template_key": "spam.notification.social_network.template"
                },
                {
                    "sender_key": "spam.notification.postal_service.sender",
                    "subject_key": "spam.notification.postal_service.subject",
                    "template_key": "spam.notification.postal_service.template"
                },
                {
                    "sender_key": "spam.notification.payment_system.sender",
                    "subject_key": "spam.notification.payment_system.subject",
                    "template_key": "spam.notification.payment_system.template"
                }
            ],
            "personal": [
                {
                    "sender_key": "spam.personal.dating.sender",
                    "subject_key": "spam.personal.dating.subject",
                    "template_key": "spam.personal.dating.template"
                },
                {
                    "sender_key": "spam.personal.astrology.sender",
                    "subject_key": "spam.personal.astrology.subject",
                    "template_key": "spam.personal.astrology.template"
                },
                {
                    "sender_key": "spam.personal.career.sender",
                    "subject_key": "spam.personal.career.subject",
                    "template_key": "spam.personal.career.template"
                }
            ]
        }
    
    def generate_spam_data(self, player_name: str = "", avoid_recent: bool = True) -> Optional[Dict]:
        """
        Сгенерировать данные для спам-письма (ключи, а не текст)
        
        Returns:
            Словарь с данными для создания письма
        """
        if not self.spam_templates:
            return None
        
        # Выбираем тип спама по вероятности
        spam_type = self._select_spam_type()
        if not spam_type:
            return None
        
        # Получаем доступные шаблоны для выбранного типа
        templates = self.spam_templates.get(spam_type, [])
        if not templates:
            return None
        
        # Фильтруем шаблоны, чтобы избежать повторений
        available_templates = templates
        if avoid_recent and self.last_sent_spam:
            recent_templates = [item.get("template_key") for item in self.last_sent_spam[-3:]]
            available_templates = [t for t in templates if t.get("template_key") not in recent_templates]
        
        # Если все шаблоны недавно использовались, используем любые
        if not available_templates:
            available_templates = templates
        
        # Выбираем случайный шаблон
        template = random.choice(available_templates)
        
        # Создаем параметры для письма
        parameters = {}
        if player_name:
            parameters["player_name"] = player_name
        
        # Добавляем случайные данные для определенных шаблонов
        if "lottery" in template.get("template_key", ""):
            parameters["ticket_number"] = f"{random.randint(100000, 999999)}"
        
        # Обновляем историю
        self._update_history(template)
        
        # Создаем данные для письма
        spam_data = {
            "sender_key": template["sender_key"],
            "subject_key": template["subject_key"],
            "template_key": template["template_key"],
            "parameters": parameters,
            "type": spam_type,
            "generated_at": datetime.now().strftime("%H:%M")
        }
        
        return spam_data
    
    def generate_spam(self, player_name: str = "", avoid_recent: bool = True) -> Optional[Dict]:
        """
        Сгенерировать спам-письмо с текстом (старый метод для совместимости)
        
        Returns:
            Словарь с готовым текстом письма
        """
        spam_data = self.generate_spam_data(player_name, avoid_recent)
        if not spam_data:
            return None
        
        # Получаем переводы
        sender = translation.t(spam_data["sender_key"], default="Unknown Sender")
        subject = translation.t(spam_data["subject_key"], default="No Subject")
        content_template = translation.t(spam_data["template_key"], default="")
        
        if not content_template:
            print(translation.t("email.spam.generator.template_not_found", default="[СПАМ] Шаблон не найден"))
            return None
        
        # Форматируем содержимое
        content = content_template
        try:
            if spam_data["parameters"]:
                content = content.format(**spam_data["parameters"])
        except KeyError as e:
            print(f"Ошибка форматирования спама: отсутствует ключ {e}")
        
        # Возвращаем старый формат для совместимости
        return {
            "sender": sender,
            "subject": subject,
            "content": content,
            "type": spam_data["type"],
            "generated_at": spam_data["generated_at"]
        }
    
    def _select_spam_type(self) -> Optional[str]:
        """Выбрать тип спама по вероятности"""
        rand_value = random.random()
        cumulative = 0.0
        
        for spam_type, probability in self.spam_probabilities.items():
            cumulative += probability
            if rand_value <= cumulative:
                return spam_type
        
        # Если не выбрали (из-за погрешности), возвращаем самый вероятный
        return max(self.spam_probabilities.items(), key=lambda x: x[1])[0]
    
    def _update_history(self, template: Dict):
        """Обновить историю отправленных спам-писем"""
        self.last_sent_spam.append(template)
        
        # Ограничиваем размер истории
        if len(self.last_sent_spam) > self.max_history_size:
            self.last_sent_spam = self.last_sent_spam[-self.max_history_size:]


# Синглтон для доступа к генератору спама
_spam_generator_instance = None

def get_spam_generator() -> SpamGenerator:
    """Получить экземпляр генератора спама (синглтон)"""
    global _spam_generator_instance
    if _spam_generator_instance is None:
        _spam_generator_instance = SpamGenerator()
    return _spam_generator_instance