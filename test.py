# test_db.py
import psycopg2
import os
from dotenv import load_dotenv

# 1. Загружаем настройки из .env
load_dotenv("bd.env")

print("="*50)
print("ПРОВЕРКА ПОДКЛЮЧЕНИЯ К POSTGRESQL")
print("="*50)

# 2. Показываем, что загрузилось
print(f"📋 Загруженные параметры:")
print(f"  DB_HOST: {os.getenv('DB_HOST')}")
print(f"  DB_PORT: {os.getenv('DB_PORT')}")
print(f"  DB_NAME: {os.getenv('DB_NAME')}")
print(f"  DB_USER: {os.getenv('DB_USER')}")
print(f"  DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")

print("\n" + "="*50)
print("Пытаемся подключиться...")
print("="*50)

try:
    # 3. Пробуем подключиться
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    print("✅ УСПЕШНО ПОДКЛЮЧИЛИСЬ!")
    
    # 4. Создаем курсор и проверяем версию
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"\n📊 Информация о сервере:")
    print(f"  Версия PostgreSQL: {version[0]}")
    
    # 5. Проверяем список баз данных
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    databases = cursor.fetchall()
    
    print(f"\n🗄 Доступные базы данных:")
    for db in databases:
        if db[0] == os.getenv('DB_NAME'):
            print(f"  ✅ {db[0]} (используем эту)")
        else:
            print(f"  • {db[0]}")
    
    # 6. Проверяем таблицы в нашей базе
    print(f"\n📋 Проверяем таблицы в базе '{os.getenv('DB_NAME')}':")
    cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        for table in tables:
            print(f"  • {table[0]}")
    else:
        print("  ⚠ Таблиц нет. База пустая.")
    
    # 7. Закрываем соединение
    cursor.close()
    connection.close()
    print("\n🔒 Соединение закрыто")
    
except psycopg2.OperationalError as e:
    print(f"\n❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
    print("\n" + "="*50)
    print("ВОЗМОЖНЫЕ РЕШЕНИЯ:")
    print("="*50)
    
    if "password authentication failed" in str(e):
        print("1. ❌ Неправильный пароль")
        print("   • Проверьте пароль в pgAdmin")
        print("   • Попробуйте сменить пароль:")
        print("     pgAdmin → Сервер → Login/Group Roles")
        print("     → postgres → Properties → Definition")
    
    elif "database \"dnd_database\" does not exist" in str(e):
        print("1. ❌ База данных 'dnd_database' не существует")
        print("2. Создайте её через pgAdmin или скриптом")
        print("\n💡 Хотите создать базу автоматически? (y/n)")
        answer = input().strip().lower()
        if answer == 'y':
            create_database()
    
    elif "could not connect to server" in str(e):
        print("1. ❌ PostgreSQL сервер не запущен")
        print("2. Запустите PostgreSQL:")
        print("   • Windows: Services → PostgreSQL")
        print("   • Mac/Linux: sudo systemctl start postgresql")
        print("   • Или запустите через pgAdmin")
    
    else:
        print("1. Проверьте, запущен ли PostgreSQL")
        print("2. Проверьте правильность параметров в .env")
        print("3. Проверьте, не блокирует ли брандмауэр порт 5432")

except Exception as e:
    print(f"\n❌ НЕИЗВЕСТНАЯ ОШИБКА: {e}")

def create_database():
    """Создать базу данных, если её нет"""
    print("\n🔄 Пытаемся создать базу данных...")
    
    try:
        # Подключаемся к системной базе 'postgres'
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database='postgres',  # Системная база, всегда существует
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        conn.autocommit = True  # Для создания базы нужно
        cursor = conn.cursor()
        
        # Создаем базу данных
        cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
        print(f"✅ База '{os.getenv('DB_NAME')}' успешно создана!")
        
        cursor.close()
        conn.close()
        
        # Теперь пробуем подключиться снова
        print("\n🔄 Пробуем подключиться к новой базе...")
        # Здесь можно вызвать основной код снова или перезапустить скрипт
        
    except Exception as e:
        print(f"❌ Не удалось создать базу: {e}")

print("\n" + "="*50)
print("Готово! Проверьте вывод выше.")
print("="*50)