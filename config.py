import json
import os

if not os.path.isdir("Notes"):
    os.mkdir("Notes")
if not os.path.isdir("Log"):
    os.mkdir("Log")

token = '1949768648:AAHSQ9G_lLBDUbJ3z5Ji4i-RRwVNpYguODc'

admin = {'m_adm': 434351723, 's_adm': 388287605}

password = 'BrwUcp+=eEw?2u6X;2H~*OimruxBV!'

hi_stickers = ['CAACAgIAAxkBAAICGWEID1pcu4U-NrzeeM7rD8DSIGDnAAJ1EgAC6NbiEka2Ut_SDVfOIAQ',
               'CAACAgIAAxkBAAICHWEIEJeh6uXHoSt2xtXq0iI_xQLUAAINBwACnebQSDlE3V0e4u2NIAQ',
               'CAACAgIAAxkBAAICH2EIEKbqPZUE-bZtFyvlVIGdThl7AAJZEgAC6NbiEjAIkw41AAGcAiAE',
               'CAACAgIAAxkBAAICIWEIEK9a3oa2Al5oi-4neJbUP0GHAAK5BwACGELuCFo2wvNObcOmIAQ',
               'CAACAgIAAxkBAAICI2EIEL2EdlJYUkB_1tvzW_J52CuYAAIfAAOc_jIwIFbyPPe22tEgBA',
               'CAACAgIAAxkBAAICJWEIEMwXsEToMTNHYoTwKT0qDDY0AAIhAAOtZbwUOqOdv9te40ggBA',
               'CAACAgIAAxkBAAICJ2EIENfcLZV4CIeZxGxOh2GRjwrmAAIciAACns4LAAE1cls1K7EuLyAE',
               'CAACAgIAAxkBAAICKWEIEOLX6zXQsI8YbJQbHa2VuyQnAAJFAwACtXHaBpOIEByJ3A0bIAQ',
               'CAACAgIAAxkBAAICK2EIEOm6cojItjjIFaLySa6AJlwQAAJnAQACFkJrCnOJvs6llmgiIAQ',
               'CAACAgIAAxkBAAICLWEIEPCl9WdEMMHnvJjzhhB4Lm4YAAL2EQAC6NbiEurBZq3G6YDIIAQ',
               'CAACAgIAAxkBAAICL2EIEP96zhRU7Fk5D-Nsl3tCRwAB0wACPwADJHFiGi-qU-kYfTtnIAQ',
               'CAACAgIAAxkBAAICMWEIEQ64gKle4cyCkGKmbTIt5YmzAAJPAAOtZbwUa5EcjYesr5MgBA',
               'CAACAgIAAxkBAAICM2EIERjv3JJ75gpMoIXekMb5wv3vAAKCAAOmysgMnFoH8pxBBGcgBA',
               'CAACAgIAAxkBAAICNWEIESGaIztxqzyiWBjAwARxxsH7AAJvAAP3AsgP6TP9mweCjjIgBA',
               'CAACAgIAAxkBAAICN2EIES3dSt9ZiMg2Ybru6XgBr0eSAAJuAAPANk8TbYftSrN4mZcgBA',
               'CAACAgIAAxkBAAICOWEIET-cfwNGKuCIba0Z27IafKS5AALnDAAC-gPYS70Gp4iIkr9mIAQ',
               'CAACAgIAAxkBAAICO2EIEVtnFofszPdMqU_sXY00mAvYAAJOAAPBnGAMrfGnEynbvkggBA']

if not os.path.exists('Log/users.json'):
    with open('Log/users.json', 'w+', encoding='utf-8') as f:
        json.dump({434351723: {'name': 'Mike Tolstov'},
                   388287605: {'name': 'Sergey Tolstov'}}, f)
