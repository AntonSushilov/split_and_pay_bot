from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data


def validate_telegram_webapp_hash(bot_token, init_data):
    """
    Проверяет подпись и извлекает данные из initData.
    Возвращает словарь с данными пользователя или вызывает ValueError при ошибке.
    """
    print(bot_token, init_data)
    print("Validating Telegram WebApp hash...", check_webapp_signature(bot_token, init_data))
    return check_webapp_signature(bot_token, init_data)

def parse_webapp_init_data(bot_token, init_data):
    return safe_parse_webapp_init_data(bot_token, init_data)

