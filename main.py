import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

# Arka plan rengini hoş bir koyu lacivert yapalım
Window.clearcolor = (0.08, 0.12, 0.2, 1)

# ==========================================================
# PYTHON SINAV SORULARI VERİ KÜMESİ
# ==========================================================
ALL_QUESTIONS = [
    ("Python'da ekrana yazı yazdırmak için hangi fonksiyon kullanılır?", ["print()", "write()", "echo()", "output()"], "print()"),
    ("Python'da kullanıcıdan bilgi almak için hangi fonksiyon kullanılır?", ["input()", "get()", "read()", "scan()"], "input()"),
    ("Python'da yorum satırı hangi simge ile başlar?", ["#", "//", "/*", "<!--"], "#"),
    ("Python'da metinsel ifadeler hangi veri tipiyle temsil edilir?", ["str", "int", "float", "bool"], "str"),
    ("Python'da tam sayılar hangi veri tipiyle temsil edilir?", ["int", "float", "str", "double"], "int"),
    ("Python'da ondalıklı sayılar hangi veri tipiyle temsil edilir?", ["float", "int", "str", "decimal"], "float"),
    ("Python'da Doğru/Yanlış değerlerini tutan veri tipi hangisidir?", ["bool", "int", "str", "logical"], "bool"),
    ("print(3 + 5) kodunun çıktısı ne olur?", ["8", "35", "3+5", "Hata verir"], "8"),
    ("print('3' + '5') kodunun çıktısı ne olur?", ["35", "8", "3+5", "Hata verir"], "35"),
    ("print(10 - 4) kodunun çıktısı nedir?", ["6", "14", "4", "104"], "6"),
    ("print(4 * 2) kodunun çıktısı nedir?", ["8", "6", "42", "16"], "8"),
    ("print(10 / 2) kodunun çıktısı nedir?", ["5.0", "5", "2", "20"], "5.0"),
    ("Bir kelimenin harf sayısını veya listenin eleman sayısını bulan fonksiyon hangisidir?", ["len()", "count()", "size()", "length()"], "len()"),
    ("Aşağıdakilerden hangisi geçerli bir değişken adıdır?", ["sayi", "1sayi", "sayi-1", "for"], "sayi"),
    ("Aşağıdaki değerlerden hangisi 'bool' veri tipindedir?", ["True", "'True'", "10", "3.14"], "True"),
    ("Aşağıdakilerden hangisi bir liste (list) tanımıdır?", ["[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}", "<1, 2, 3>"], "[1, 2, 3]"),
    ("Listeye yeni bir eleman eklemek için hangi metod kullanılır?", ["append()", "add()", "push()", "insert()"], "append()"),
    ("Listeden bir eleman çıkarmak/silmek için hangi metod kullanılır?", ["remove()", "delete()", "clear()", "cut()"], "remove()"),
    ("print(type(5)) kodu ekrana ne yazdırır?", ["<class 'int'>", "<class 'str'>", "<class 'float'>", "5"], "<class 'int'>"),
    ("Aşağıdakilerden hangisi 'Eşittir' anlamına gelen karşılaştırma operatörüdür?", ["==", "=", "!=", "=>"], "=="),
    ("Koşullu durumları kontrol etmek için hangi anahtar kelime kullanılır?", ["if", "for", "while", "def"], "if"),
    ("if koşulu sağlanmadığında alternatif durum için ne kullanılır?", ["else", "then", "or", "stop"], "else"),
    ("Döngüyü tamamen durdurup çıkmak için hangi komut kullanılır?", ["break", "stop", "exit", "end"], "break"),
    ("Python'da fonksiyon tanımlamak için hangi kelime kullanılır?", ["def", "func", "function", "define"], "def"),
    ("Python dosyasının uzantısı nedir?", [".py", ".pt", ".python", ".txt"], ".py")
]

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        title = Label(
            text="[b]PYTHON MİNİ SINAVI[/b]", 
            markup=True, 
            font_size='22sp', 
            size_hint_y=None, 
            height=60,
            color=(0.2, 0.6, 1, 1)
        )
        subtitle = Label(
            text="Lütfen Bir Zorluk Seviyesi Seçin:", 
            font_size='15sp', 
            size_hint_y=None, 
            height=40,
            color=(0.8, 0.8, 0.8, 1)
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)

        # Butonlar
        btn_kolay = Button(
            text="KOLAY (10 Soru)", 
            background_color=(0.1, 0.7, 0.4, 1), 
            size_hint_y=None, 
            height=55
        )
        btn_kolay.bind(on_release=lambda x: self.start_quiz(10))

        btn_orta = Button(
            text="ORTA (15 Soru)", 
            background_color=(1, 0.5, 0, 1), 
            size_hint_y=None, 
            height=55
        )
        btn_orta.bind(on_release=lambda x: self.start_quiz(15))

        btn_zor = Button(
            text="ZOR (25 Soru)", 
            background_color=(0.8, 0.2, 0.2, 1), 
            size_hint_y=None, 
            height=55
        )
        btn_zor.bind(on_release=lambda x: self.start_quiz(25))

        layout.add_widget(btn_kolay)
        layout.add_widget(btn_orta)
        layout.add_widget(btn_zor)

        self.add_widget(layout)

    def start_quiz(self, count):
        app = App.get_running_app()
        app.questions = random.sample(ALL_QUESTIONS, min(count, len(ALL_QUESTIONS)))
        app.current_index = 0
        app.correct_count = 0
        app.wrong_count = 0
        
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.load_question()
        self.manager.current = 'quiz'


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.counter_label = Label(
            text="", 
            font_size='14sp', 
            size_hint_y=None, 
            height=30,
            color=(0.6, 0.7, 0.8, 1)
        )
        self.question_label = Label(
            text="", 
            font_size='16sp', 
            size_hint_y=None, 
            height=100,
            halign='center',
            valign='middle'
        )
        self.question_label.bind(size=self.question_label.setter('text_size'))

        self.options_layout = BoxLayout(orientation='vertical', spacing=10)
        self.feedback_label = Label(
            text="", 
            font_size='15sp', 
            size_hint_y=None, 
            height=40
        )

        self.layout.add_widget(self.counter_label)
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.options_layout)
        self.layout.add_widget(self.feedback_label)

        self.add_widget(self.layout)

    def load_question(self):
        app = App.get_running_app()
        self.options_layout.clear_widgets()
        self.feedback_label.text = ""

        if app.current_index < len(app.questions):
            q_text, options, self.correct_answer = app.questions[app.current_index]
            
            self.counter_label.text = f"Soru: {app.current_index + 1} / {len(app.questions)}"
            self.question_label.text = q_text

            shuffled_options = options.copy()
            random.shuffle(shuffled_options)

            for opt in shuffled_options:
                btn = Button(
                    text=opt, 
                    size_hint_y=None, 
                    height=50,
                    background_color=(0.2, 0.3, 0.4, 1)
                )
                btn.bind(on_release=lambda btn_obj: self.check_answer(btn_obj))
                self.options_layout.add_widget(btn)
        else:
            self.manager.current = 'result'

    def check_answer(self, btn_obj):
        app = App.get_running_app()
        
        # Seçenekleri kilitle
        for child in self.options_layout.children:
            child.disabled = True

        selected_option = btn_obj.text
        if selected_option == self.correct_answer:
            app.correct_count += 1
            btn_obj.background_color = (0.1, 0.8, 0.3, 1)
            self.feedback_label.text = "Doğru Cevap! ✓"
            self.feedback_label.color = (0.2, 0.9, 0.4, 1)
        else:
            app.wrong_count += 1
            btn_obj.background_color = (0.9, 0.2, 0.2, 1)
            self.feedback_label.text = f"Yanlış! Doğru Cevap: {self.correct_answer}"
            self.feedback_label.color = (0.9, 0.3, 0.3, 1)

        Clock.schedule_once(lambda dt: self.next_question(), 1.5)

    def next_question(self):
        app = App.get_running_app()
        app.current_index += 1
        self.load_question()


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.title_label = Label(
            text="[b]SINAV TAMAMLANDI![/b]", 
            markup=True,
            font_size='22sp',
            color=(0.2, 0.6, 1, 1)
        )
        self.result_label = Label(
            text="", 
            font_size='16sp',
            halign='center'
        )
        
        btn_retry = Button(
            text="Tekrar Denemek İster Misin?", 
            size_hint_y=None, 
            height=50,
            background_color=(0.2, 0.5, 0.8, 1)
        )
        btn_retry.bind(on_release=self.restart)

        layout.add_widget(self.title_label)
        layout.add_widget(self.result_label)
        layout.add_widget(btn_retry)

        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        total = app.correct_count + app.wrong_count
        rate = (app.correct_count / total * 100) if total > 0 else 0
        self.result_label.text = (
            f"Doğru Sayısı: {app.correct_count}\n"
            f"Yanlış Sayısı: {app.wrong_count}\n\n"
            f"Başarı Oranı: %{rate:.1f}"
        )

    def restart(self, instance):
        self.manager.current = 'difficulty'


class MobileQuizApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DifficultyScreen(name='difficulty'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(ResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    MobileQuizApp().run()
