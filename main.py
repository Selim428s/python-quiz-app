import json
import os
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

Window.clearcolor = (0.08, 0.09, 0.12, 1)

SORU_SAYISI = 10
SURE = 20  # saniye / soru

RENK_NORMAL = (0.2, 0.25, 0.35, 1)
RENK_DOGRU = (0.15, 0.65, 0.3, 1)
RENK_YANLIS = (0.8, 0.2, 0.2, 1)


def sorulari_yukle():
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.json")
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def yazi(text, size=18, height=None, bold=False):
    lbl = Label(text=text, font_size=size, bold=bold, halign="center", valign="middle")
    if height:
        lbl.size_hint_y = None
        lbl.height = height
    lbl.bind(size=lambda w, s: setattr(w, "text_size", s))
    return lbl


def buton(text, cb, height=60, renk=RENK_NORMAL):
    b = Button(text=text, size_hint_y=None, height=height, font_size=17,
               background_normal="", background_color=renk, halign="center", valign="middle")
    b.bind(size=lambda w, s: setattr(w, "text_size", (s[0] - 20, None)))
    b.bind(on_release=cb)
    return b


class MenuEkrani(Screen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        kok = BoxLayout(orientation="vertical", padding=30, spacing=15)
        kok.add_widget(yazi("Python Sınavı", 34, bold=True))
        kok.add_widget(yazi("Zorluk seviyesini seç", 18, 40))
        for ad, anahtar in (("Kolay", "kolay"), ("Orta", "orta"), ("Zor", "zor")):
            kok.add_widget(buton(ad, lambda b, a=anahtar: App.get_running_app().baslat(a), 70))
        kok.add_widget(Label())
        self.add_widget(kok)


class SoruEkrani(Screen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        kok = BoxLayout(orientation="vertical", padding=20, spacing=10)
        ust = BoxLayout(size_hint_y=None, height=40)
        self.ilerleme = yazi("", 16)
        self.sayac = yazi("", 16)
        self.skor = yazi("", 16)
        for w in (self.ilerleme, self.sayac, self.skor):
            ust.add_widget(w)
        kok.add_widget(ust)
        self.soru_lbl = yazi("", 22, bold=True)
        kok.add_widget(self.soru_lbl)
        self.sik_butonlari = []
        for _ in range(4):
            b = buton("", self.cevapla)
            self.sik_butonlari.append(b)
            kok.add_widget(b)
        self.geri_bildirim = yazi("", 18, 40)
        kok.add_widget(self.geri_bildirim)
        self.sonraki = buton("Sonraki", lambda b: App.get_running_app().sonraki(), 55)
        self.sonraki.disabled = True
        kok.add_widget(self.sonraki)
        self.add_widget(kok)
        self.goster()

    def goster(self):
        app = App.get_running_app()
        s = app.sorular[app.indeks]
        secenekler = s["secenekler"][:]
        random.shuffle(secenekler)
        self.soru_lbl.text = s["soru"]
        for b, t in zip(self.sik_butonlari, secenekler):
            b.text = t
            b.background_color = RENK_NORMAL
            b.disabled = False
        self.geri_bildirim.text = ""
        self.sonraki.disabled = True
        self.ilerleme.text = f"Soru {app.indeks + 1}/{len(app.sorular)}"
        self.skor.text = f"Doğru: {app.dogru}"
        self.kalan = SURE
        self.sayac.text = f"{self.kalan} sn"
        self.cevaplandi = False
        Clock.unschedule(self.tik)
        Clock.schedule_interval(self.tik, 1)

    def tik(self, dt):
        self.kalan -= 1
        self.sayac.text = f"{self.kalan} sn"
        if self.kalan <= 0:
            Clock.unschedule(self.tik)
            self.bitir(None)

    def cevapla(self, btn):
        if not self.cevaplandi:
            Clock.unschedule(self.tik)
            self.bitir(btn)

    def bitir(self, secilen):
        app = App.get_running_app()
        self.cevaplandi = True
        dogru = app.sorular[app.indeks]["dogru"]
        for b in self.sik_butonlari:
            b.disabled = True
            if b.text == dogru:
                b.background_color = RENK_DOGRU
        if secilen is not None and secilen.text == dogru:
            app.dogru += 1
            self.geri_bildirim.text = "Doğru!"
        else:
            app.yanlis += 1
            if secilen is not None:
                secilen.background_color = RENK_YANLIS
                self.geri_bildirim.text = "Yanlış!"
            else:
                self.geri_bildirim.text = "Süre doldu!"
        self.skor.text = f"Doğru: {app.dogru}"
        son = app.indeks + 1 >= len(app.sorular)
        self.sonraki.text = "Sonucu Gör" if son else "Sonraki"
        self.sonraki.disabled = False


class SonucEkrani(Screen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        app = App.get_running_app()
        toplam = app.dogru + app.yanlis
        yuzde = round(100 * app.dogru / toplam) if toplam else 0
        kok = BoxLayout(orientation="vertical", padding=30, spacing=15)
        kok.add_widget(yazi("Sınav Bitti", 32, bold=True))
        kok.add_widget(yazi(f"Doğru: {app.dogru}\nYanlış: {app.yanlis}\nBaşarı: %{yuzde}", 24))
        kok.add_widget(buton("Tekrar Dene", lambda b: app.baslat(app.zorluk), 65))
        kok.add_widget(buton("Ana Menü", lambda b: app.menuye_don(), 65))
        self.add_widget(kok)


class SinavApp(App):
    def build(self):
        self.title = "Python Sınavı"
        self.tum_sorular = sorulari_yukle()
        self.sm = ScreenManager()
        for ekran in (MenuEkrani(name="menu"), SoruEkrani(name="soru"), SonucEkrani(name="sonuc")):
            self.sm.add_widget(ekran)
        return self.sm

    def baslat(self, zorluk):
        self.zorluk = zorluk
        havuz = [q for q in self.tum_sorular if q["zorluk"] == zorluk]
        self.sorular = random.sample(havuz, min(SORU_SAYISI, len(havuz)))
        self.indeks = 0
        self.dogru = 0
        self.yanlis = 0
        self.sm.current = "soru"
        self.sm.get_screen("soru").on_pre_enter()

    def sonraki(self):
        self.indeks += 1
        if self.indeks >= len(self.sorular):
            self.sm.current = "sonuc"
        else:
            self.sm.get_screen("soru").goster()

    def menuye_don(self):
        self.sm.current = "menu"


if __name__ == "__main__":
    SinavApp().run()
