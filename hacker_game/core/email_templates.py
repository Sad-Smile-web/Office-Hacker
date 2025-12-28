from simple_translation import translation

# Ключи для получения сюжетных писем по дням
STORYLINE_EMAILS = {
    1: "system_welcome",                     # День 1: Приветственное письмо
    2: "mvd_mission_1_intro",                # День 2: Первое задание
    3: "mvd_mission_2_security_audit",       # День 3: Проверка безопасности
    # Здесь можно добавить дальнейшие сюжетные письма
}

# Уровни сложности для сюжетных заданий (ключи для перевода)
STORY_DIFFICULTY_KEYS = {
    1: "email.difficulties.easy",
    2: "email.difficulties.medium",
    3: "email.difficulties.hard",
    4: "email.difficulties.expert"
}

# Сроки выполнения для сюжетных заданий (ключи для перевода)
STORY_DEADLINE_KEYS = {
    1: "email.deadlines.until_shift_end",
    2: "email.deadlines.two_hours",
    3: "email.deadlines.one_hour",
    4: "email.deadlines.thirty_minutes"
}

def get_story_email_for_day(day: int) -> str:
    """Получить шаблон сюжетного письма для указанного дня"""
    return STORYLINE_EMAILS.get(day, "")

def get_story_difficulty(mission_number: int) -> str:
    """Получить сложность для сюжетного задания"""
    key = STORY_DIFFICULTY_KEYS.get(mission_number, "email.difficulties.easy")
    return translation.t(key)

def get_story_deadline(mission_number: int) -> str:
    """Получить срок для сюжетного задания"""
    key = STORY_DEADLINE_KEYS.get(mission_number, "email.deadlines.until_shift_end")
    return translation.t(key)