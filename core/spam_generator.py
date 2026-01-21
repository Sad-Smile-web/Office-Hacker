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
                },
                {
                    "sender_key": "spam.advertisement.discount_club.sender",
                    "subject_key": "spam.advertisement.discount_club.subject",
                    "template_key": "spam.advertisement.discount_club.template"
                },
                {
                    "sender_key": "spam.advertisement.travel_agency.sender",
                    "subject_key": "spam.advertisement.travel_agency.subject", 
                    "template_key": "spam.advertisement.travel_agency.template"
                },
                {
                    "sender_key": "spam.advertisement.real_estate.sender",
                    "subject_key": "spam.advertisement.real_estate.subject",
                    "template_key": "spam.advertisement.real_estate.template"
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
                },
                {
                    "sender_key": "spam.scam.free_phone.sender",
                    "subject_key": "spam.scam.free_phone.subject",
                    "template_key": "spam.scam.free_phone.template"
                },
                {
                    "sender_key": "spam.scam.tax_refund.sender",
                    "subject_key": "spam.scam.tax_refund.subject",
                    "template_key": "spam.scam.tax_refund.template"
                },
                {
                    "sender_key": "spam.scam.inheritance.sender",
                    "subject_key": "spam.scam.inheritance.subject",
                    "template_key": "spam.scam.inheritance.template"
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
                },
                {
                    "sender_key": "spam.notification.bank_alert.sender",
                    "subject_key": "spam.notification.bank_alert.subject",
                    "template_key": "spam.notification.bank_alert.template"
                },
                {
                    "sender_key": "spam.notification.energy_company.sender",
                    "subject_key": "spam.notification.energy_company.subject",
                    "template_key": "spam.notification.energy_company.template"
                },
                {
                    "sender_key": "spam.notification.internet_provider.sender",
                    "subject_key": "spam.notification.internet_provider.subject",
                    "template_key": "spam.notification.internet_provider.template"
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
                },
                {
                    "sender_key": "spam.personal.friend_request.sender",
                    "subject_key": "spam.personal.friend_request.subject",
                    "template_key": "spam.personal.friend_request.template"
                },
                {
                    "sender_key": "spam.personal.health_check.sender",
                    "subject_key": "spam.personal.health_check.subject",
                    "template_key": "spam.personal.health_check.template"
                },
                {
                    "sender_key": "spam.personal.university.sender",
                    "subject_key": "spam.personal.university.subject",
                    "template_key": "spam.personal.university.template"
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
        
        # Генерируем случайные номера телефонов для шаблонов, которые их используют
        if any(keyword in template.get("template_key", "") 
               for keyword in ["phone", "call", "номер", "звоните"]):
            # Генерируем номер в формате 87-800-XXX-XX-XX
            phone_base = "87-800"
            phone_middle = f"{random.randint(100, 999)}"
            phone_end = f"{random.randint(10, 99)}-{random.randint(10, 99)}"
            parameters["phone_number"] = f"{phone_base}-{phone_middle}-{phone_end}"
        
        # Генерируем случайные email-адреса для спам-писем
        if "cyb" in template.get("template_key", ""):
            email_domains = ["$banki.cyb", "$finance.cyb", "$support.cyb", "$service.cyb"]
            email_name = random.choice(["support", "info", "contact", "service", "help", "admin"])
            parameters["email_address"] = f"{email_name}{random.choice(email_domains)}"
        
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
    
    def add_custom_template(self, spam_type: str, sender_key: str, subject_key: str, template_key: str):
        """Добавить пользовательский шаблон спама"""
        if spam_type not in self.spam_templates:
            self.spam_templates[spam_type] = []
        
        new_template = {
            "sender_key": sender_key,
            "subject_key": subject_key,
            "template_key": template_key
        }
        
        self.spam_templates[spam_type].append(new_template)
        
        print(translation.t("email.spam.generator.custom_template_added", 
                           default="[СПАМ] Добавлен новый шаблон типа '{template_type}': {template_subject}").format(
            template_type=spam_type,
            template_subject=subject_key
        ))
    
    def clear_history(self):
        """Очистить историю отправленных спам-писем"""
        self.last_sent_spam = []
        print(translation.t("email.spam.generator.history_cleared", 
                           default="[СПАМ] История спам-писем очищена"))
    
    def update_probabilities(self, new_probabilities: Dict[str, float]):
        """Обновить вероятности типов спама"""
        # Проверяем, что сумма вероятностей равна 1.0 (с небольшой погрешностью)
        total = sum(new_probabilities.values())
        if abs(total - 1.0) > 0.01:
            print(translation.t("email.spam.generator.probability_warning",
                               default="[СПАМ] Внимание: сумма вероятностей {total} не равна 1.0").format(
                total=total
            ))
            # Нормализуем вероятности
            normalized = {}
            for spam_type, prob in new_probabilities.items():
                normalized[spam_type] = prob / total
            new_probabilities = normalized
        
        self.spam_probabilities = new_probabilities
        
        print(translation.t("email.spam.generator.probabilities_updated",
                           default="[СПАМ] Вероятности спама обновлены: {probabilities}").format(
            probabilities=str(new_probabilities)
        ))
    
    def get_spam_type_count(self) -> Dict[str, int]:
        """Получить количество шаблонов для каждого типа спама"""
        return {spam_type: len(templates) for spam_type, templates in self.spam_templates.items()}
    
    def test_generator(self, count: int = 5, player_name: str = "Тестовый Игрок"):
        """Протестировать генератор спама"""
        print(translation.t("email.spam.generator.testing", default="Тестирование генератора спама:"))
        print("-" * 50)
        
        stats = {}
        for i in range(count):
            spam = self.generate_spam(player_name)
            if spam:
                spam_type = spam["type"]
                stats[spam_type] = stats.get(spam_type, 0) + 1
                
                print(translation.t("email.spam.generator.spam_generated", default="\nСпам #{number}:").format(number=i+1))
                print(translation.t("email.spam.generator.from", default="От: {sender}").format(sender=spam["sender"]))
                print(translation.t("email.spam.generator.subject", default="Тема: {subject}").format(subject=spam["subject"]))
                print(translation.t("email.spam.generator.type", default="Тип: {spam_type}").format(spam_type=spam_type))
                
                # Показываем только превью содержимого
                content_preview = spam["content"][:150] + "..." if len(spam["content"]) > 150 else spam["content"]
                print(translation.t("email.spam.generator.content_preview", 
                                   default="Содержимое:\n{content}...").format(content=content_preview))
        
        print("\n" + "=" * 50)
        print(translation.t("email.spam.generator.total_templates", 
                           default="Всего шаблонов: {count}").format(count=sum(len(t) for t in self.spam_templates.values())))
        
        if stats:
            stats_str = ", ".join([f"{k}: {v}" for k, v in stats.items()])
            print(translation.t("email.spam.generator.statistics", 
                               default="\nСтатистика: {stats}").format(stats=stats_str))
        
        print("-" * 50)


# Синглтон для доступа к генератору спама
_spam_generator_instance = None

def get_spam_generator() -> SpamGenerator:
    """Получить экземпляр генератора спама (синглтон)"""
    global _spam_generator_instance
    if _spam_generator_instance is None:
        _spam_generator_instance = SpamGenerator()
    return _spam_generator_instance


# Пример использования
if __name__ == "__main__":
    # Тестирование генератора
    generator = get_spam_generator()
    print("Тест генератора спам-писем:")
    print("=" * 50)
    generator.test_generator(3, "Иван Иванов")