import requests

start_text = """
Assalomu alaykum! 🎓
Biznes Universitetiga xush kelibsiz! 📚

Ushbu bot sizning ma'lumotlaringizni qayta ishlash uchun xizmat qiladi. Iltimos, kerakli ma'lumotlarni yuboring.
""" 

register_failed = """
Agar bunaqa ma'lumot CRM da bo'lmasa:

❗️ Afsuski, sizning ma'lumotlaringiz hozircha tizimda topilmadi.

Bu holat odatda siz hali ro‘yxatga olinmagan bo‘lsangiz yuz beradi. Iltimos, biroz kuting. Sizning ma’lumotlaringiz tez orada tizimga kiritiladi. Bu jarayon odatda bir necha daqiqa yoki soat davom etadi.

Keyinchalik botga qayta kirib urinib ko‘ring. ⏳
"""

def status_not_complited(user_id):
    response = requests.get(f'https://buyuk.zamon.repid.uz/api/v1/bot/bot/student_group_info/{user_id}/')
    if response.status_code == 200:
        return f"""
        Bonus darslardan foydalanish imkoniyatini qoʻldan boy bermang!
        {response.json().get('start_date')} sanasigacha toʻlovni 100% amalga oshirib, bonus darslarga ega boʻling.
        """
    else:
        return f"""
            Bonus darslardan foydalanish imkoniyatini qoʻldan boy bermang!
            boshlanish sanasi sanasigacha toʻlovni 100% amalga oshirib, bonus darslarga ega boʻling
        """

def status_complited(user_id):
    response = requests.get(f'https://buyuk.zamon.repid.uz/api/v1/bot/bot/student_group_info/{user_id}/')
    if response.status_code ==200:
        return f"""
            Biznes Universitetining “{response.json().get('name')}” guruhiga qo‘shilganingiz bilan tabriklaymiz!
            Iltimos, barcha bonus darslarni ko‘rib chiqing va {response.json().get('start_date')} sanasidan boshlab 7 kun davomida oflayn darslarga tayyorgarlik ko‘ring.

            🕘 Darslar vaqti: 09:00 — 19:00
        """
    else:
        return """Biznes Universitetining “Guruh nomi” guruhiga qo‘shilganingiz bilan tabriklaymiz!
        Iltimos, barcha bonus darslarni ko‘rib chiqing va boshlash sana sanasidan boshlab 7 kun davomida oflayn darslarga tayyorgarlik ko‘ring.

        🕘 Darslar vaqti: 09:00 — 19:00
        """

last_text = """
Diqqat!
Barcha muhim ma’lumotlar sizga aynan ushbu bot orqali yuboriladi.
Iltimos, kelgan xabarlarga e’tiborli bo‘ling va ularni befarq qoldirmang.
"""

def graduate_text():
    res = requests.get(f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/student_group_info/")
    if res.status_code == 200:
        return  f"""
        Biznes universitet {res.json().get('name')} {res.json().get('start_date')} shu sanadan boshlanadi online qatnashishni istaysizmi?
        """

callback_no = """
Botdagi xabarlarni kuzatib boring, muhim habarlarni shu bot orqali olishingiz mumkin
"""