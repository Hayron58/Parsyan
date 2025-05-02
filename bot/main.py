
    import logging
    from aiogram import Bot, Dispatcher, executor, types
    from utils.parser import YandexParser
    from utils.analyzer import SiteAnalyzer
    from utils.report_generator import ReportGenerator
    from dotenv import load_dotenv
    import os

    # Загрузка переменных окружения
    load_dotenv()
    API_TOKEN = os.getenv('BOT_TOKEN')

    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    parser = YandexParser()
    analyzer = SiteAnalyzer()
    report_gen = ReportGenerator()

    @dp.message_handler(commands=['start'])
    async def start_cmd(message: types.Message):
        await message.answer(
            "Привет! Я бот для поиска и анализа компаний.\n"
            "Используйте команду /search запрос, город\n"
            "Например: /search кафе, Москва"
        )

    @dp.message_handler(commands=['search'])
    async def search_cmd(message: types.Message):
        try:
            query = message.text.replace('/search', '').strip()
            if ',' not in query:
                await message.answer("Пожалуйста, укажите запрос и город через запятую")
                return
            
            search_query, city = query.split(',', 1)
            await message.answer("🔍 Ищу компании...")
            
            # Парсинг
            companies = parser.parse_company(search_query.strip(), city.strip())
            
            # Анализ сайтов
            for company in companies:
                if company.get('website'):
                    company['site_analysis'] = analyzer.analyze_site(company['website'])
            
            # Генерация отчетов
            excel_path = report_gen.generate_excel(companies)
            pdf_path = report_gen.generate_pdf(companies)
            
            # Отправка отчетов
            with open(excel_path, 'rb') as excel:
                await message.answer_document(excel, caption="Отчет в Excel")
            
            with open(pdf_path, 'rb') as pdf:
                await message.answer_document(pdf, caption="Отчет в PDF")
            
        except Exception as e:
            logging.exception("Ошибка при обработке запроса")
            await message.answer("Произошла ошибка. Попробуйте позже.")

    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
