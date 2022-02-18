import pyttsx3
engine = pyttsx3.init()
sss = """

Малиновая Lada,
Малиновый закат
Хотела на Канары
А везу тебя за МКАД
Холодный как Россия
Красивый, холостой
Тебя все звали с ними
А поехала со мной

"""
engine.say(sss)

engine.runAndWait()
