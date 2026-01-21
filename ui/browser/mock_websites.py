# ui/browser/mock_websites.py
import random
from typing import Dict, Optional
from datetime import datetime
from simple_translation import translation


class MockWebsites:
    """Генератор контента для вымышленных сайтов"""
    
    def __init__(self):
        self.websites = self._load_website_templates()
        
    def _load_website_templates(self) -> Dict:
        """Загрузить шаблоны сайтов"""
        return {
            "market.sale": self._generate_marketplace_site,
            "film.distribution.sale": self._generate_cinema_site,
            "career.consultant": self._generate_career_site,
            "horoscope": self._generate_horoscope_site,
            "investor.deposits.profit": self._generate_investment_site,
            "computer.wizard": self._generate_security_site,
            "payments.security": self._generate_payment_site,
            "SIBERIA.communication": self._generate_social_site,
            "dating.nearby": self._generate_dating_site,
            "default": self._generate_default_site
        }
        
    def get_website_content(self, domain: str, path: str) -> str:
        """Получить контент для указанного домена и пути"""
        # Ищем подходящий генератор
        for key, generator in self.websites.items():
            if key in domain:
                return generator(domain, path)
                
        # Если не нашли, используем генератор по умолчанию
        return self.websites["default"](domain, path)
        
    def _generate_marketplace_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт интернет-магазина"""
        products = [
            {"name": "Смартфон XPhone ZX", "price": 9999, "old_price": 39999, "discount": 75},
            {"name": "Ноутбук CyberBook Pro", "price": 54999, "old_price": 79999, "discount": 31},
            {"name": "Умные часы Watch 5", "price": 8999, "old_price": 14999, "discount": 40},
            {"name": "Наушники SoundBlast", "price": 4999, "old_price": 8999, "discount": 44},
            {"name": "Игровая консоль GameBox", "price": 29999, "old_price": 49999, "discount": 40},
        ]
        
        product_list = ""
        for i, product in enumerate(products[:3], 1):
            product_list += f"""
            <div class="product">
                <h3>{product['name']}</h3>
                <p class="price-old">{product['old_price']:,d} ₽</p>
                <p class="price-new">{product['price']:,d} ₽</p>
                <p class="discount">-{product['discount']}%</p>
                <button onclick="buy({i})">КУПИТЬ</button>
            </div>
            """
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>МегаМаркет - Скидки до 75%</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a1a; color: #00ffff; margin: 0; padding: 20px; }}
                .header {{ background: linear-gradient(90deg, #ff0066, #ff9900); padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                h1 {{ color: white; text-shadow: 0 0 10px #ff0066; }}
                .products {{ display: flex; gap: 20px; flex-wrap: wrap; }}
                .product {{ background: #1a1a2e; border: 2px solid #00ffff; padding: 15px; border-radius: 10px; width: 250px; }}
                .price-old {{ color: #ff4444; text-decoration: line-through; }}
                .price-new {{ color: #00ff00; font-size: 24px; font-weight: bold; }}
                .discount {{ background: #ff0066; color: white; padding: 5px; border-radius: 5px; display: inline-block; }}
                button {{ background: #00ff00; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }}
                button:hover {{ background: #00cc00; }}
                .warning {{ background: #ff9900; color: black; padding: 10px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔥 МЕГАМАРКЕТ - РАСПРОДАЖА 🔥</h1>
                <p>Скидки до 75%! Только сегодня!</p>
            </div>
            
            <div class="warning">
                ⚠ ВНИМАНИЕ: Это демонстрационная страница. Покупки невозможны.
            </div>
            
            <div class="products">
                {product_list}
            </div>
            
            <script>
                function buy(productId) {{
                    alert("Это демонстрационная страница. В реальной игре здесь была бы система покупок.");
                }}
            </script>
            
            <p style="margin-top: 30px; color: #888; font-size: 12px;">
                © 2142 МегаМаркет | app.cyb://market.sale | Лицензия МВД №2142-КБ-5678
            </p>
        </body>
        </html>
        """
        
    def _generate_cinema_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт онлайн-кинотеатра"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Кино Онлайн - Премиум подписка</title>
            <style>
                body { font-family: Arial, sans-serif; background: #000022; color: #ffffff; margin: 0; padding: 20px; }
                .header { background: linear-gradient(90deg, #8a2be2, #4b0082); padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center; }
                h1 { color: white; text-shadow: 0 0 15px #8a2be2; font-size: 36px; }
                .offer { background: rgba(255, 215, 0, 0.1); border: 2px solid #ffd700; padding: 20px; border-radius: 10px; margin: 20px 0; }
                .price { font-size: 48px; color: #ffd700; font-weight: bold; }
                .movies { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }
                .movie { background: #1a1a3a; border-radius: 10px; overflow: hidden; }
                .movie img { width: 100%; height: 150px; background: #333; }
                .movie-title { padding: 10px; font-weight: bold; }
                button { background: linear-gradient(90deg, #ff00ff, #00ffff); color: black; border: none; padding: 15px 30px; border-radius: 25px; cursor: pointer; font-size: 18px; font-weight: bold; margin: 20px 0; }
                button:hover { transform: scale(1.05); }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎬 КИНО ОНЛАЙН ПРЕМИУМ</h1>
                <p>Более 50 000 фильмов и сериалов без ограничений</p>
            </div>
            
            <div class="offer">
                <h2>ГОДОВАЯ ПОДПИСКА ВСЕГО ЗА</h2>
                <div class="price">1 ₽</div>
                <p>Вместо 9 999 ₽ в месяц</p>
                <p>🔥 АКЦИЯ ДЕЙСТВУЕТ 24 ЧАСА 🔥</p>
            </div>
            
            <div class="movies">
                <div class="movie">
                    <div style="background: linear-gradient(45deg, #ff0066, #ff9900); height: 150px;"></div>
                    <div class="movie-title">КИБЕРПАНК: Восстание машин</div>
                </div>
                <div class="movie">
                    <div style="background: linear-gradient(45deg, #0066ff, #00ffff); height: 150px;"></div>
                    <div class="movie-title">SIBERIA: Тайны корпорации</div>
                </div>
                <div class="movie">
                    <div style="background: linear-gradient(45deg, #00ff00, #ffff00); height: 150px;"></div>
                    <div class="movie-title">МВД: Секретная миссия</div>
                </div>
            </div>
            
            <center>
                <button onclick="subscribe()">ПОЛУЧИТЬ ПОДПИСКУ ЗА 1 ₽</button>
            </center>
            
            <div style="background: #ff4444; color: white; padding: 15px; border-radius: 10px; margin-top: 30px;">
                ⚠ ПРЕДУПРЕЖДЕНИЕ: Это мошеннический сайт. Не вводите реальные данные!
            </div>
            
            <script>
                function subscribe() {
                    alert("Это демонстрационная страница. В реальной жизни это мошенничество!");
                }
            </script>
            
            <p style="margin-top: 30px; color: #888; font-size: 12px; text-align: center;">
                app.cyb://film.distribution.sale | Лицензия отсутствует
            </p>
        </body>
        </html>
        """
        
    def _generate_career_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт карьерного консультанта"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Карьера Pro - Вакансия мечты</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #001122; color: #ffffff; margin: 0; padding: 30px; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background: linear-gradient(90deg, #0055aa, #0088ff); padding: 25px; border-radius: 12px; margin-bottom: 30px; }
                .salary { font-size: 42px; color: #00ff00; font-weight: bold; text-shadow: 0 0 10px #00ff00; }
                .requirements { background: rgba(255, 165, 0, 0.1); border-left: 5px solid #ffaa00; padding: 15px; margin: 20px 0; }
                .benefits { display: flex; gap: 15px; margin: 25px 0; flex-wrap: wrap; }
                .benefit { background: #1a2a3a; padding: 15px; border-radius: 8px; flex: 1; min-width: 150px; }
                .apply-btn { background: linear-gradient(90deg, #00ff00, #00cc00); color: black; border: none; padding: 18px 40px; border-radius: 8px; font-size: 20px; font-weight: bold; cursor: pointer; display: block; margin: 30px auto; }
                .apply-btn:hover { background: linear-gradient(90deg, #00cc00, #009900); }
                .warning { background: rgba(255, 0, 0, 0.2); border: 2px solid #ff0000; padding: 15px; border-radius: 8px; margin: 25px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💼 КИБЕРБЕЗОПАСНОСТЬ В МЕЖДУНАРОДНОЙ КОМПАНИИ</h1>
                    <p>Уникальная возможность для специалистов высокого уровня</p>
                </div>
                
                <div class="salary">от 300 000 ₽</div>
                <p>+ ежегодный бонус до 1 000 000 ₽</p>
                
                <div class="requirements">
                    <h3>📋 Требования:</h3>
                    <ul>
                        <li>Опыт работы от 1 года в сфере кибербезопасности</li>
                        <li>Знание сетевых технологий и протоколов</li>
                        <li>Готовность к ненормированному графику</li>
                        <li>Умение работать в стрессовых ситуациях</li>
                        <li>Знание английского языка (техническая документация)</li>
                    </ul>
                </div>
                
                <div class="benefits">
                    <div class="benefit">🏠 Удаленная работа</div>
                    <div class="benefit">💻 Современное оборудование</div>
                    <div class="benefit">🏥 Медицинская страховка</div>
                    <div class="benefit">✈️ Командировки за границу</div>
                </div>
                
                <div class="warning">
                    ⚠ ВНИМАНИЕ: Для отклика необходимо внести страховой депозит в размере 5 000 ₽.
                    Деньги будут возвращены после успешного прохождения собеседования.
                </div>
                
                <button class="apply-btn" onclick="applyForJob()">ОТКЛИКНУТЬСЯ НА ВАКАНСИЮ</button>
                
                <script>
                    function applyForJob() {
                        alert("Это демонстрационная страница. В реальной жизни это может быть мошенничеством!");
                    }
                </script>
                
                <p style="color: #888; font-size: 12px; text-align: center; margin-top: 40px;">
                    app.cyb://career.consultant | Карьерное агентство "Pro Career" © 2142
                </p>
            </div>
        </body>
        </html>
        """
        
    def _generate_horoscope_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт гороскопа"""
        signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", 
                "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
        
        sign = random.choice(signs)
        predictions = [
            "Сегодня вас ждет неожиданная встреча, которая изменит вашу жизнь.",
            "Будьте осторожны с финансами - возможны неожиданные расходы.",
            "Звезды благоволят новым начинаниям. Смело беритесь за сложные задачи.",
            "В личной жизни возможны перемены к лучшему.",
            "Коллеги могут преподнести неприятный сюрприз. Будьте внимательны.",
            "Удача на вашей стороне в вопросах, связанных с технологиями.",
            "Возможен конфликт с начальством. Проявите дипломатичность.",
            "День идеально подходит для обучения и саморазвития."
        ]
        
        prediction = random.choice(predictions)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Астрологический Портал - Ваш гороскоп</title>
            <style>
                body {{ font-family: 'Times New Roman', serif; background: #2a1b3a; color: #e6d5ff; margin: 0; padding: 30px; }}
                .container {{ max-width: 700px; margin: 0 auto; background: rgba(0, 0, 0, 0.5); padding: 30px; border-radius: 15px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .zodiac-sign {{ font-size: 48px; margin: 20px 0; }}
                .prediction {{ background: rgba(255, 215, 0, 0.1); border: 2px solid #ffd700; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; }}
                .tarot {{ display: flex; justify-content: space-around; margin: 30px 0; flex-wrap: wrap; }}
                .card {{ width: 100px; height: 150px; background: linear-gradient(45deg, #8b4513, #d2691e); border-radius: 8px; margin: 10px; position: relative; }}
                .card:before {{ content: '🃏'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 40px; }}
                .premium {{ background: linear-gradient(45deg, #ffd700, #ff9900); color: black; padding: 20px; border-radius: 10px; margin: 25px 0; text-align: center; }}
                .buy-btn {{ background: #ff00ff; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 18px; cursor: pointer; }}
                .buy-btn:hover {{ background: #cc00cc; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔮 АСТРОЛОГИЧЕСКИЙ ПОРТАЛ 🔮</h1>
                    <p>Точные предсказания на основе древних знаний</p>
                </div>
                
                <div class="zodiac-sign">♌ {sign}</div>
                
                <div class="prediction">
                    <h2>Ваш гороскоп на сегодня:</h2>
                    <p>{prediction}</p>
                </div>
                
                <div class="tarot">
                    <div class="card"></div>
                    <div class="card"></div>
                    <div class="card"></div>
                </div>
                
                <div class="premium">
                    <h2>✨ ПРЕМИУМ ПРОГНОЗ ✨</h2>
                    <p>Получите детальный прогноз на месяц с персональными рекомендациями!</p>
                    <p>Всего за 999 ₽</p>
                    <button class="buy-btn" onclick="buyPremium()">ПОЛУЧИТЬ ПРЕМИУМ ПРОГНОЗ</button>
                </div>
                
                <div style="background: rgba(255, 0, 0, 0.2); padding: 15px; border-radius: 8px; margin-top: 25px;">
                    ⚠ Гороскопы носят развлекательный характер. Не принимайте важные решения на их основе.
                </div>
                
                <script>
                    function buyPremium() {{
                        alert("Это демонстрационная страница. Астрология не является наукой!");
                    }}
                </script>
                
                <p style="text-align: center; color: #aaa; font-size: 12px; margin-top: 30px;">
                    app.cyb://horoscope | © 2142 Астрологическая ассоциация SIBERIA
                </p>
            </div>
        </body>
        </html>
        """
        
    def _generate_investment_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт инвестиций"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Крипто-Инвестиции - 300% прибыли</title>
            <style>
                body { font-family: 'Courier New', monospace; background: #000000; color: #00ff00; margin: 0; padding: 20px; }
                .matrix-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.1; }
                .container { max-width: 900px; margin: 0 auto; position: relative; }
                .header { text-align: center; margin-bottom: 40px; }
                .profit { font-size: 72px; color: #00ff00; text-shadow: 0 0 20px #00ff00; animation: glow 1s infinite alternate; }
                @keyframes glow { from { text-shadow: 0 0 20px #00ff00; } to { text-shadow: 0 0 30px #00ff00, 0 0 40px #00ff00; } }
                .calculator { background: #001100; border: 2px solid #00ff00; padding: 25px; border-radius: 10px; margin: 25px 0; }
                input { background: #000; color: #00ff00; border: 1px solid #00ff00; padding: 10px; width: 200px; font-family: 'Courier New'; }
                .invest-btn { background: #00ff00; color: black; border: none; padding: 15px 30px; font-size: 18px; font-weight: bold; cursor: pointer; margin: 20px 0; }
                .invest-btn:hover { background: #00cc00; }
                .testimonials { display: flex; gap: 20px; margin: 30px 0; flex-wrap: wrap; }
                .testimonial { background: #002200; border: 1px solid #008800; padding: 15px; border-radius: 8px; flex: 1; min-width: 200px; }
                .warning { border: 3px solid #ff0000; padding: 20px; margin: 30px 0; background: rgba(255, 0, 0, 0.1); }
            </style>
        </head>
        <body>
            <div class="matrix-bg">
                <!-- Эффект матрицы будет добавлен через JavaScript -->
            </div>
            
            <div class="container">
                <div class="header">
                    <h1>🚀 КРИПТО-ИНВЕСТИЦИИ БУДУЩЕГО 🚀</h1>
                    <p>Инвестируйте в технологии следующего поколения</p>
                </div>
                
                <div class="profit">300% ПРИБЫЛИ</div>
                <p>Гарантированная доходность за первый месяц</p>
                
                <div class="calculator">
                    <h2>💎 КАЛЬКУЛЯТОР ДОХОДНОСТИ</h2>
                    <p>Ваш депозит: <input type="number" id="deposit" value="10000" oninput="calculateProfit()"> ₽</p>
                    <p>Ваша прибыль через месяц: <span id="profit" style="color: #00ff00; font-weight: bold;">30 000 ₽</span></p>
                    <p>Общая сумма через месяц: <span id="total" style="color: #ffff00; font-weight: bold;">40 000 ₽</span></p>
                </div>
                
                <button class="invest-btn" onclick="startInvesting()">НАЧАТЬ ИНВЕСТИРОВАТЬ</button>
                
                <div class="testimonials">
                    <div class="testimonial">
                        "Вложил 50 000 ₽, получил 150 000 ₽ через месяц! Спасибо команде!"<br>
                        - Иван К., Москва
                    </div>
                    <div class="testimonial">
                        "Лучшая инвестиционная платформа! Простая регистрация, высокая доходность."<br>
                        - Мария С., Новосибирск
                    </div>
                    <div class="testimonial">
                        "За 3 месяца увеличил капитал в 10 раз! Рекомендую всем!"<br>
                        - Алексей П., Санкт-Петербург
                    </div>
                </div>
                
                <div class="warning">
                    ⚠ ВНИМАНИЕ: Высокая доходность = высокие риски. Это демонстрационная страница.<br>
                    В реальной жизни подобные предложения часто являются мошенничеством.
                </div>
                
                <script>
                    function calculateProfit() {
                        const deposit = parseInt(document.getElementById('deposit').value) || 0;
                        const profit = deposit * 3;
                        const total = deposit + profit;
                        document.getElementById('profit').textContent = profit.toLocaleString() + ' ₽';
                        document.getElementById('total').textContent = total.toLocaleString() + ' ₽';
                    }
                    
                    function startInvesting() {
                        alert("Это демонстрационная страница. Инвестируйте только в лицензированные организации!");
                    }
                    
                    // Эффект матрицы
                    const bg = document.querySelector('.matrix-bg');
                    for(let i = 0; i < 50; i++) {
                        const char = document.createElement('div');
                        char.textContent = String.fromCharCode(0x30A0 + Math.random() * 96);
                        char.style.position = 'absolute';
                        char.style.left = Math.random() * 100 + '%';
                        char.style.top = Math.random() * 100 + '%';
                        char.style.color = '#00ff00';
                        char.style.opacity = Math.random() * 0.5 + 0.1;
                        char.style.fontSize = (Math.random() * 10 + 10) + 'px';
                        bg.appendChild(char);
                    }
                </script>
                
                <p style="text-align: center; color: #008800; font-size: 12px; margin-top: 40px;">
                    app.cyb://investor.deposits.profit | Крипто-лицензия №CRYPTO-2142-MVD
                </p>
            </div>
        </body>
        </html>
        """
        
    def _generate_security_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт кибербезопасности"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>КиберБезопасность Pro - Ваш компьютер заражен!</title>
            <style>
                body { font-family: Arial, sans-serif; background: #1a0000; color: #ff4444; margin: 0; padding: 20px; }
                .alert { background: #ff0000; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; animation: pulse 2s infinite; }
                @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
                .scan-results { background: #330000; border: 3px solid #ff4444; padding: 25px; border-radius: 10px; margin: 25px 0; }
                .threat { display: flex; justify-content: space-between; margin: 15px 0; padding: 10px; background: #550000; border-radius: 5px; }
                .fix-btn { background: #00ff00; color: black; border: none; padding: 20px 40px; font-size: 24px; font-weight: bold; border-radius: 10px; cursor: pointer; display: block; margin: 30px auto; }
                .fix-btn:hover { background: #00cc00; }
                .timer { font-size: 36px; color: #ffff00; text-align: center; margin: 20px 0; }
                .fake-warning { background: rgba(255, 255, 0, 0.1); border: 2px solid #ffff00; padding: 20px; border-radius: 10px; margin: 25px 0; }
            </style>
        </head>
        <body>
            <div class="alert">
                <h1>🚨 КРИТИЧЕСКАЯ ОШИБКА БЕЗОПАСНОСТИ 🚨</h1>
                <p>Обнаружено 5 вирусов и 3 шпионские программы!</p>
            </div>
            
            <div class="timer">
                ⏰ Время до полного повреждения системы: <span id="time">04:59</span>
            </div>
            
            <div class="scan-results">
                <h2>🔍 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ:</h2>
                
                <div class="threat">
                    <span>Trojan.Win32.Stealer</span>
                    <span style="color: #ff0000;">ВЫСОКАЯ ОПАСНОСТЬ</span>
                </div>
                
                <div class="threat">
                    <span>Ransomware.CryptoLocker</span>
                    <span style="color: #ff0000;">КРИТИЧЕСКАЯ ОПАСНОСТЬ</span>
                </div>
                
                <div class="threat">
                    <span>Spyware.Keylogger</span>
                    <span style="color: #ff9900;">СРЕДНЯЯ ОПАСНОСТЬ</span>
                </div>
                
                <div class="threat">
                    <span>Adware.PopupMaster</span>
                    <span style="color: #ffff00;">НИЗКАЯ ОПАСНОСТЬ</span>
                </div>
            </div>
            
            <button class="fix-btn" onclick="fixVirus()">ИСПРАВИТЬ УГРОЗЫ СЕЙЧАС</button>
            
            <div class="fake-warning">
                ⚠ Для очистки системы необходимо приобрести полную версию программы за 1999 ₽.
                Бесплатная версия может только обнаружить угрозы.
            </div>
            
            <script>
                // Таймер обратного отсчета
                let timeLeft = 5 * 60; // 5 минут
                const timerElement = document.getElementById('time');
                
                function updateTimer() {
                    const minutes = Math.floor(timeLeft / 60);
                    const seconds = timeLeft % 60;
                    timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                    
                    if (timeLeft > 0) {
                        timeLeft--;
                        setTimeout(updateTimer, 1000);
                    }
                }
                
                function fixVirus() {
                    alert("Это демонстрационная страница. Настоящие антивирусы не работают таким образом!\n\nЕсли вы видите подобное сообщение в реальной жизни - это мошенничество!");
                }
                
                updateTimer();
            </script>
            
            <p style="text-align: center; color: #888; font-size: 12px; margin-top: 40px;">
                app.cyb://computer.wizard | Это демонстрационная страница для игры
            </p>
        </body>
        </html>
        """
        
    def _generate_payment_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт платежной системы"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Безопасность Платежей - Подтверждение аккаунта</title>
            <style>
                body { font-family: Arial, sans-serif; background: #001a33; color: #ffffff; margin: 0; padding: 30px; }
                .container { max-width: 600px; margin: 0 auto; background: rgba(0, 50, 100, 0.5); padding: 30px; border-radius: 15px; }
                .bank-header { background: linear-gradient(90deg, #0055aa, #0088ff); padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }
                .form-group { margin: 20px 0; }
                label { display: block; margin-bottom: 8px; color: #aaddff; }
                input { width: 100%; padding: 12px; border: 2px solid #0088ff; border-radius: 6px; background: #002244; color: white; font-size: 16px; }
                .card-icons { display: flex; gap: 15px; margin: 20px 0; }
                .card-icon { width: 60px; height: 40px; background: #003366; border-radius: 5px; display: flex; align-items: center; justify-content: center; }
                .verify-btn { background: linear-gradient(90deg, #00ff00, #00cc00); color: black; border: none; padding: 18px; width: 100%; border-radius: 8px; font-size: 20px; font-weight: bold; cursor: pointer; margin: 25px 0; }
                .verify-btn:hover { background: linear-gradient(90deg, #00cc00, #009900); }
                .warning-box { background: rgba(255, 0, 0, 0.2); border: 2px solid #ff0000; padding: 20px; border-radius: 10px; margin: 25px 0; }
                .ssl { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 20px 0; color: #00ff00; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="bank-header">
                    <h1>🏦 БЕЗОПАСНОСТЬ ПЛАТЕЖЕЙ</h1>
                    <p>Подтверждение личности для защиты вашего аккаунта</p>
                </div>
                
                <div class="warning-box">
                    ⚠ Обнаружена подозрительная активность в вашем аккаунте.<br>
                    Для предотвращения несанкционированного доступа подтвердите ваши данные.
                </div>
                
                <div class="ssl">
                    🔒 Защищенное соединение SSL 256-bit
                </div>
                
                <form id="paymentForm">
                    <div class="form-group">
                        <label>Номер банковской карты:</label>
                        <input type="text" placeholder="0000 0000 0000 0000" maxlength="19">
                    </div>
                    
                    <div class="form-group">
                        <label>Срок действия (ММ/ГГ):</label>
                        <input type="text" placeholder="MM/YY">
                    </div>
                    
                    <div class="form-group">
                        <label>CVV код (3 цифры на обороте):</label>
                        <input type="password" placeholder="123" maxlength="3">
                    </div>
                    
                    <div class="form-group">
                        <label>Код из SMS:</label>
                        <input type="text" placeholder="Введите код из SMS">
                    </div>
                    
                    <div class="card-icons">
                        <div class="card-icon">💳</div>
                        <div class="card-icon">🏦</div>
                        <div class="card-icon">🔐</div>
                    </div>
                    
                    <button type="button" class="verify-btn" onclick="verifyAccount()">
                        ПОДТВЕРДИТЬ АККАУНТ
                    </button>
                </form>
                
                <div style="background: rgba(255, 255, 0, 0.1); padding: 15px; border-radius: 8px; margin-top: 25px;">
                    ℹ️ После подтверждения аккаунт будет защищен от мошенников.<br>
                    Проверка занимает 2-3 минуты.
                </div>
                
                <script>
                    function verifyAccount() {
                        alert("Это демонстрационная страница! Никогда не вводите реальные данные карты на подозрительных сайтах!\n\nНастоящие банки никогда не запрашивают CVV код и код из SMS одновременно.");
                    }
                    
                    // Форматирование номера карты
                    document.querySelector('input[placeholder="0000 0000 0000 0000"]').addEventListener('input', function(e) {
                        let value = e.target.value.replace(/\s/g, '').replace(/\D/g, '');
                        let formatted = '';
                        for (let i = 0; i < value.length; i++) {
                            if (i > 0 && i % 4 === 0) formatted += ' ';
                            formatted += value[i];
                        }
                        e.target.value = formatted.substring(0, 19);
                    });
                </script>
                
                <p style="text-align: center; color: #888; font-size: 12px; margin-top: 30px;">
                    app.cyb://payments.security | Это учебная страница для тренировки кибербезопасности
                </p>
            </div>
        </body>
        </html>
        """
        
    def _generate_social_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт социальной сети"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SIBERIA Communication - Социальная сеть</title>
            <style>
                body { font-family: Arial, sans-serif; background: #0a1a2a; color: #ffffff; margin: 0; padding: 0; }
                .navbar { background: linear-gradient(90deg, #0066cc, #0099ff); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
                .logo { font-size: 24px; font-weight: bold; }
                .profile { display: flex; align-items: center; gap: 15px; }
                .avatar { width: 50px; height: 50px; background: linear-gradient(45deg, #ff0066, #ff9900); border-radius: 50%; }
                .container { display: flex; padding: 20px; }
                .sidebar { width: 250px; background: rgba(0, 50, 100, 0.3); padding: 20px; border-radius: 10px; margin-right: 20px; }
                .feed { flex: 1; }
                .post { background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; margin-bottom: 20px; }
                .post-header { display: flex; align-items: center; margin-bottom: 15px; }
                .post-avatar { width: 40px; height: 40px; background: #555; border-radius: 50%; margin-right: 15px; }
                .interactions { display: flex; gap: 20px; margin-top: 15px; }
                .like, .comment, .share { cursor: pointer; padding: 8px 15px; border-radius: 20px; background: rgba(255, 255, 255, 0.1); }
                .like:hover { background: rgba(255, 0, 0, 0.2); }
                .new-post { background: rgba(0, 100, 200, 0.3); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                textarea { width: 100%; height: 80px; background: rgba(255, 255, 255, 0.1); border: 1px solid #0099ff; border-radius: 8px; padding: 10px; color: white; }
                .post-btn { background: #0099ff; color: white; border: none; padding: 10px 25px; border-radius: 20px; cursor: pointer; margin-top: 10px; }
                .notification { position: fixed; top: 20px; right: 20px; background: #ff9900; color: black; padding: 15px; border-radius: 8px; display: none; }
            </style>
        </head>
        <body>
            <div class="navbar">
                <div class="logo">SIBERIA.communication</div>
                <div class="profile">
                    <div class="avatar"></div>
                    <div>Игрок</div>
                </div>
            </div>
            
            <div class="container">
                <div class="sidebar">
                    <h3>👥 Друзья онлайн (5)</h3>
                    <div style="margin: 15px 0;">
                        <div style="display: flex; align-items: center; margin: 10px 0;">
                            <div style="width: 30px; height: 30px; background: #ff0066; border-radius: 50%; margin-right: 10px;"></div>
                            <span>Иван Петров</span>
                        </div>
                        <div style="display: flex; align-items: center; margin: 10px 0;">
                            <div style="width: 30px; height: 30px; background: #00ff00; border-radius: 50%; margin-right: 10px;"></div>
                            <span>Мария Сидорова</span>
                        </div>
                    </div>
                    
                    <h3>📨 Сообщения (3)</h3>
                    <div style="margin: 15px 0;">
                        <div style="background: rgba(0, 150, 255, 0.2); padding: 10px; border-radius: 5px; margin: 5px 0;">
                            Новое сообщение от Алексея
                        </div>
                    </div>
                </div>
                
                <div class="feed">
                    <div class="new-post">
                        <textarea placeholder="Что у вас нового?"></textarea>
                        <button class="post-btn" onclick="createPost()">Опубликовать</button>
                    </div>
                    
                    <div class="post">
                        <div class="post-header">
                            <div class="post-avatar" style="background: linear-gradient(45deg, #ff0066, #ff9900);"></div>
                            <div>
                                <strong>Иван Петров</strong><br>
                                <small>2 часа назад</small>
                            </div>
                        </div>
                        <p>Только что завершил важный проект по кибербезопасности для МВД. Очень сложная задача, но справился!</p>
                        <div class="interactions">
                            <div class="like" onclick="likePost(this)">👍 Нравится (24)</div>
                            <div class="comment" onclick="commentPost()">💬 Комментировать</div>
                            <div class="share" onclick="sharePost()">🔗 Поделиться</div>
                        </div>
                    </div>
                    
                    <div class="post">
                        <div class="post-header">
                            <div class="post-avatar" style="background: linear-gradient(45deg, #00ff00, #00cc00);"></div>
                            <div>
                                <strong>Мария Сидорова</strong><br>
                                <small>5 часов назад</small>
                            </div>
                        </div>
                        <p>Нашла интересный баг в системе безопасности SIBERIA-SOFTWARE. Сообщила начальству, жду ответа.</p>
                        <div class="interactions">
                            <div class="like" onclick="likePost(this)">👍 Нравится (18)</div>
                            <div class="comment" onclick="commentPost()">💬 Комментировать (3)</div>
                            <div class="share" onclick="sharePost()">🔗 Поделиться</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="notification" id="notification">
                Это демонстрационная версия социальной сети
            </div>
            
            <script>
                function createPost() {
                    showNotification("В реальной социальной сети здесь был бы ваш пост");
                }
                
                function likePost(element) {
                    const text = element.textContent;
                    const likes = parseInt(text.match(/\((\d+)\)/)[1]) || 0;
                    element.textContent = `👍 Нравится (${likes + 1})`;
                }
                
                function commentPost() {
                    showNotification("Здесь была бы форма комментария");
                }
                
                function sharePost() {
                    showNotification("Здесь была бы функция поделиться");
                }
                
                function showNotification(message) {
                    const notification = document.getElementById('notification');
                    notification.textContent = message;
                    notification.style.display = 'block';
                    setTimeout(() => {
                        notification.style.display = 'none';
                    }, 3000);
                }
                
                // Показываем уведомление при загрузке
                setTimeout(() => showNotification("Добро пожаловать в SIBERIA.communication!"), 1000);
            </script>
            
            <p style="text-align: center; color: #888; font-size: 12px; padding: 20px;">
                app.cyb://SIBERIA.communication | Официальная социальная сеть корпорации SIBERIA-SOFTWARE
            </p>
        </body>
        </html>
        """
        
    def _generate_dating_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт знакомств"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Знакомства Рядом - Новые сообщения</title>
            <style>
                body { font-family: Arial, sans-serif; background: #2a0033; color: #ff66ff; margin: 0; padding: 20px; }
                .header { background: linear-gradient(90deg, #ff00ff, #cc00cc); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
                .profiles { display: flex; gap: 20px; margin: 30px 0; flex-wrap: wrap; justify-content: center; }
                .profile { width: 180px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; overflow: hidden; text-align: center; }
                .profile-img { height: 150px; background: linear-gradient(45deg, #ff66ff, #ffaa00); }
                .profile-name { padding: 10px; font-weight: bold; }
                .profile-age { color: #aaa; }
                .message-me { background: #ff00ff; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; }
                .premium-offer { background: linear-gradient(45deg, #ffd700, #ff9900); color: black; padding: 20px; border-radius: 10px; margin: 25px 0; text-align: center; }
                .upgrade-btn { background: #ff00ff; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 18px; cursor: pointer; }
                .warning { background: rgba(255, 0, 0, 0.2); border: 2px solid #ff0000; padding: 20px; border-radius: 10px; margin: 25px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>❤️ ЗНАКОМСТВА РЯДОМ ❤️</h1>
                <p>5 девушек ждут вашего сообщения!</p>
            </div>
            
            <div class="profiles">
                <div class="profile">
                    <div class="profile-img"></div>
                    <div class="profile-name">Анна, 24</div>
                    <div class="profile-age">1 км от вас</div>
                    <button class="message-me" onclick="messageUser('Анна')">НАПИСАТЬ</button>
                </div>
                
                <div class="profile">
                    <div class="profile-img" style="background: linear-gradient(45deg, #00ffff, #0066ff);"></div>
                    <div class="profile-name">Екатерина, 26</div>
                    <div class="profile-age">3 км от вас</div>
                    <button class="message-me" onclick="messageUser('Екатерина')">НАПИСАТЬ</button>
                </div>
                
                <div class="profile">
                    <div class="profile-img" style="background: linear-gradient(45deg, #00ff00, #ffff00);"></div>
                    <div class="profile-name">Виктория, 22</div>
                    <div class="profile-age">5 км от вас</div>
                    <button class="message-me" onclick="messageUser('Виктория')">НАПИСАТЬ</button>
                </div>
            </div>
            
            <div class="premium-offer">
                <h2>💎 ПРЕМИУМ ДОСТУП 💎</h2>
                <p>Читайте сообщения и общайтесь без ограничений!</p>
                <p>Всего 999 ₽ в месяц</p>
                <button class="upgrade-btn" onclick="upgradeToPremium()">ПОЛУЧИТЬ ПРЕМИУМ</button>
            </div>
            
            <div class="warning">
                ⚠ ВНИМАНИЕ: Это демонстрационная страница. Реальные сайты знакомств могут быть опасны.<br>
                Никогда не переводите деньги незнакомым людям в интернете!
            </div>
            
            <script>
                function messageUser(name) {
                    alert(`Для отправки сообщения ${name} необходим премиум-доступ.`);
                }
                
                function upgradeToPremium() {
                    alert("Это демонстрационная страница. В реальной жизни будьте осторожны с оплатой на сайтах знакомств!");
                }
            </script>
            
            <p style="text-align: center; color: #888; font-size: 12px; margin-top: 30px;">
                app.cyb://dating.nearby | Тренировочная страница для изучения социальной инженерии
            </p>
        </body>
        </html>
        """
        
    def _generate_default_site(self, domain: str, path: str) -> str:
        """Сгенерировать сайт по умолчанию"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{domain} - Вымышленный сайт</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #000000; color: #00ff00; margin: 0; padding: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; background: rgba(0, 50, 0, 0.2); padding: 30px; border-radius: 15px; border: 2px solid #00ff00; }}
                h1 {{ color: #00ffff; text-shadow: 0 0 10px #00ffff; }}
                .url-info {{ background: rgba(0, 100, 100, 0.3); padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .cyber-effect {{ animation: glitch 0.3s infinite; }}
                @keyframes glitch {{
                    0% {{ transform: translate(0); }}
                    20% {{ transform: translate(-2px, 2px); }}
                    40% {{ transform: translate(-2px, -2px); }}
                    60% {{ transform: translate(2px, 2px); }}
                    80% {{ transform: translate(2px, -2px); }}
                    100% {{ transform: translate(0); }}
                }}
                .links {{ margin: 30px 0; }}
                .link {{ display: inline-block; background: #003300; color: #00ff00; padding: 10px 20px; margin: 5px; border-radius: 5px; text-decoration: none; }}
                .link:hover {{ background: #005500; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="cyber-effect">🌐 ВЫМЫШЛЕННЫЙ САЙТ</h1>
                
                <div class="url-info">
                    <p><strong>Протокол:</strong> app.cyb</p>
                    <p><strong>Домен:</strong> {domain}</p>
                    <p><strong>Путь:</strong> {path}</p>
                    <p><strong>Полный URL:</strong> app.cyb://{domain}{path}</p>
                </div>
                
                <p>Это демонстрационная страница вымышленного сайта в игровом браузере.</p>
                <p>В реальной игре здесь мог бы быть контент, связанный с сюжетом или заданиями.</p>
                
                <div class="links">
                    <a href="app.cyb://market.sale" class="link">🛒 Интернет-магазин</a>
                    <a href="app.cyb://film.distribution.sale" class="link">🎬 Кинотеатр</a>
                    <a href="app.cyb://career.consultant" class="link">💼 Карьера</a>
                    <a href="app.cyb://horoscope" class="link">🔮 Гороскоп</a>
                </div>
                
                <div style="margin-top: 40px; padding: 20px; background: rgba(255, 0, 0, 0.1); border-radius: 10px;">
                    <h3>⚠ ИНФОРМАЦИЯ О БЕЗОПАСНОСТИ</h3>
                    <p>В реальном интернете:</p>
                    <ul>
                        <li>Проверяйте URL сайтов</li>
                        <li>Не вводите данные карт на подозрительных сайтах</li>
                        <li>Не верьте обещаниям быстрой прибыли</li>
                        <li>Используйте антивирусы</li>
                    </ul>
                </div>
                
                <p style="text-align: center; color: #888; margin-top: 40px;">
                    Это учебный симулятор кибербезопасности.<br>
                    Все сайты являются вымышленными и созданы для обучения.
                </p>
            </div>
            
            <script>
                // Простой эффект глитча
                const title = document.querySelector('h1');
                setInterval(() => {{
                    if (Math.random() < 0.3) {{
                        title.classList.add('cyber-effect');
                        setTimeout(() => title.classList.remove('cyber-effect'), 300);
                    }}
                }}, 1000);
            </script>
        </body>
        </html>
        """