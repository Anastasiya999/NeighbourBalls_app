# -*- coding: utf-8 -*-
import chardet
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from datetime import datetime, timedelta
from popuptype import PopupType
from tasktype import *
from flashcards import *
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from specialbuttons import HoverButton, ImageButton
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.fullscreen = 'auto'


# store = JsonStore('pl.json', encoding='utf-8', ensure_ascii=False)
class Vocabulary(BoxLayout):
    def set_content(self, content):
        text = ''
        f = open(content, "r", encoding="utf-8")
        for x in f:
            self.add_widget(
                Label(text=x, size_hint_y=None, font_size='14sp', height=30,
                      color=(0, 0, 0, 1)))


class FactButton(HoverButton):
    def __init__(self, description=None, label=None, fact_content=None, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.description = description
        self.description.color = (0.97, 0.6, 0.25, 1)
        self.description.italic = True
        self.label = label
        self.background_color = (0.25, 0.5, 0.5, 1)
        self.background_normal = '1,1,1,1'
        self.fact_content = JsonStore(fact_content)
        self.popup = Popup(title='', size_hint=(1, 1))

    def on_press(self):
        self.background_normal = '0.5,1,1,1'

    def on_release(self):
        self.background_normal = '1,1,1,1'
        layout_popup = FactLayout(fact=self, padding=(100, 5), spacing=70, size_hint_y=None, content=self.fact_content)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))
        layout_popup.set_content()
        root = ScrollView(size_hint=(1, None), size=(Window.width - 10, Window.height - 50))
        root.add_widget(layout_popup)
        # self.popup = Popup(title='', content=root, size_hint=(1, 1))
        self.popup.content = root
        self.popup.open()
        # new Fact pop up

    def on_enter(self, *args):
        Window.set_system_cursor('hand')
        self.description.text = self.label

    def on_leave(self, *args):
        Window.set_system_cursor('arrow')
        self.description.text = ''


class FactsScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.update, .5)
        Clock.schedule_interval(self.on_enter, .5)

    def on_enter(self, *args):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.articles = JsonStore('json/' + App.get_running_app().lang + '/facts.json')
        items = self.articles.count()
        for i in range(1, items + 1):
            article = self.articles[str(i)]
            self.grid.add_widget(
                Label(text=article['level'], height=50, size_hint_y=None, size_hint_x=.3, font_size='23sp', bold=True,
                      color=(0.2, 0.3, 0.43, 1)))
            self.grid.add_widget(
                FactButton(text=article['head'], label=article['description'], description=self.description_l,
                           height=50, size_hint_y=None, fact_content=article['source']))
        for j in range(3, 15):
            self.grid.add_widget(
                Label(text='level', height=50, size_hint_y=None, font_size='23sp', bold=True, color=(0.2, 0.3, 0.43, 1),
                      size_hint_x=.3))
            self.grid.add_widget(Button(text='Article ' + str(j) + '(to do)', height=50, size_hint_y=None))


    def on_pre_enter(self, *args):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)

    def update(self, *args):
        self.articles = JsonStore('json/' + App.get_running_app().lang + '/facts.json')
        print('json/' + App.get_running_app().lang + '/facts.json')
        self.store = App.get_running_app().STORE
        self.flag.source = self.store.get('flag')['source']


class FactLayout(StackLayout):

    def __init__(self, content=None, fact=None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.fact = fact

    def set_content(self):
        self.add_widget(
            Label(text=self.content['main_header']['text'], size_hint_x=0.95, size_hint_y=None, font_size='30sp',
                  bold=True, color=(0.99, 0.98, 0.7, 1)))
        btn_exit = ImageButton(size_hint_y=None, size_hint_x=0.05, source='images/exit_btn.png')
        btn_exit.bind(on_press=self.fact.popup.dismiss)
        self.add_widget(btn_exit)
        if self.content.exists('images'):

            self.add_widget(Image(size_hint_y=.18, size_hint_x=0.35, source=self.content['images']['img_1']))
            self.add_widget(Label(text=self.content['p']['p_1'], size_hint_x=0.65, size_hint_y=.2, font_size='18sp',
                                  color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(
                Label(text=self.content['p']['p_2'], size_hint_x=1, text_size=(1200, None), size_hint_y=None,
                      font_size='18sp',
                      color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(
                Label(text=self.content['p']['p_3'], text_size=(600, None), size_hint_x=.6, size_hint_y=.25,
                      font_size='18sp',
                      color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(Image(size_hint_y=.3, size_hint_x=.4, source=self.content['images']['img_2']))

            self.add_widget(Image(size_hint_y=.2, size_hint_x=.5, source=self.content['images']['img_3']))
            self.add_widget(
                Label(text=self.content['p']['p_4'], size_hint_x=.5, size_hint_y=.2, font_size='18sp',
                      text_size=(600, None),
                      color=(0.1, 0.1, 0.1, 1)))
        else:
            self.spacing = 100
            p = self.content['p']
            i=1
            for item in p:
                self.add_widget(
                    Label(text=p['p_'+str(i)], text_size=(600, None), size_hint_x=1, size_hint_y=None,
                          font_size='18sp',
                          color=(0.1, 0.1, 0.1, 1)))
                i+=1



class HomeScreen(Screen):

    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.store = JsonStore('json/pl.json')
        self.study_l = self.store.get('homescreen')['study']
        self.exit_l = self.store.get('homescreen')['exit']
        self.settings_l = self.store.get('homescreen')['parameters']
        self.credits_l = 'Credits'
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.store = App.get_running_app().STORE
        '''self.study_l = self.store.get('homescreen')['study']
        self.exit_l = self.store.get('homescreen')['exit']
        self.settings_l = self.store.get('homescreen')['parameters']
        self.credits_l = self.store.get('homescreen')['credits']'''
        self.nauka.text = self.store.get('homescreen')['study']
        self.wyjscie.text = self.store.get('homescreen')['exit']
        self.ustawienia.text = self.store.get('homescreen')['parameters']
        self.flag.source = self.store.get('flag')['source']


class SettingsScreen(Screen):
    pass


class ChooseTaskScreen(Screen):
    pass


class ChooseLevelScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.flag.source = App.get_running_app().STORE.get('flag')['source']


class CustomBoxLayout(BoxLayout):
    pass


class PopupLayout(BoxLayout):
    pass


class ChooseLevelScreen2(Screen):
    pass


class Task(ImageButton):
    def __init__(self, status=None, typ=None, category=None, number=None, level=None, task_panel=None,
                 task_content=None,
                 **kwargs):
        super(Task, self).__init__(**kwargs)

        self.typ = typ
        self.task_content = task_content
        self.level = level
        self.status = status
        self.category = category
        self.number = number
        self.task_type = TaskType(
            JsonStore('json/' + App.get_running_app().lang + '/' + self.level + '/' + self.category + '_' + str(
                self.number) + '.json'))
        self.source = 'images/' + 'zad_' + self.category + '/' + 'zad_' + self.category + '_' + self.status + str(
            self.number) + '.png'
        self.task_panel = task_panel

    def on_press(self):
        # App.get_running_app().add_task(task=self, content=self.task_content)
        print("disabled", self.disabled)
        self.task_type = TaskType(
            JsonStore('json/' + App.get_running_app().lang + '/' + self.level + '/' + self.category + '_' + str(
                self.number) + '.json'))
        print('json/' + App.get_running_app().lang + '/' + self.level + '/' + self.category + '_' + str(
            self.number) + '.json')
        App.get_running_app().add_task(task=self, typ=self.task_type.create(self.typ))
        print(self.task_type.content.get('title')['name'], self.level, self.category, self.source, self.number)
        # App.get_running_app().add_task(task=self, typ=self.task_type.create(self.typ))

    def change_task_status(self, status):
        self.lang = App.get_running_app().lang
        store = JsonStore('json/' + self.lang + '/' + self.level + '.json')
        time = datetime.now()
        if status == -1:
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = -1
            store[self.task_panel.topic] = store[self.task_panel.topic]
            App.get_running_app().update_cards(level=self.level, number=str(self.number), topic=self.task_panel.topic)
            self.disabled = True
        elif status == 1:
            treal = store[self.task_panel.topic][self.category][str(self.number)]['treal']
            if treal == 2:
                App.get_running_app().block_tasks[self.level] = {"topic": self.task_panel.topic,
                                                                 self.category: {str(self.number): {
                                                                     "time": {"year": time.year, "month": time.month,
                                                                              "day": time.day, "hour": time.hour,
                                                                              "min": time.minute}}}}
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = treal + 1
            store[self.task_panel.topic] = store[self.task_panel.topic]
        else:
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = 0
            store[self.task_panel.topic] = store[self.task_panel.topic]


class TasksPanelScreen(Screen):

    def __init__(self, store_name=None, topic=None, **kw):
        super(TasksPanelScreen, self).__init__(**kw)
        self.lang = App.get_running_app().lang
        self.store_name = store_name
        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        self.topic = topic
        # self.popup = Popup(title='', size_hint=(None, None),size=(Window.width-500, Window.height-100))
        Clock.schedule_interval(self.update, .5)

    def on_pre_enter(self, *args):
        self.lang = App.get_running_app().lang
        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.set_tasks('gram')
        self.set_tasks('czyt')
        self.set_tasks('sluch')

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_taskspanel_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()

    def update(self, *args):
        self.lang = App.get_running_app().lang

        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.set_tasks('gram')
        self.set_tasks('czyt')
        self.set_tasks('sluch')
        self.flag.source = App.get_running_app().STORE.get('flag')['source']

    def show_book(self):
        book_content = 'json/' + self.store_name + '/' + self.topic + '.txt'
        layout_popup = Vocabulary(orientation='vertical', size_hint_y=None)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))
        layout_popup.set_content(book_content)

        root = ScrollView(size_hint=(1, None), size=(Window.width - 100, Window.height - 100))
        root.add_widget(layout_popup)
        popup = Popup(title='', content=root, size_hint=(None, 1), size=(Window.width - 500, Window.height - 100))
        popup.open()

    def set_tasks(self, category):

        disabled_bool = False
        for i in range(1, 6):
            task = self.store.get(self.topic)[category][str(i)]
            if 3 > task['treal'] >= 0:
                status = 'new'
                disabled_bool = False
            elif task['treal'] == 3:
                status = 'block'
                disabled_bool = True

            elif task['treal'] < 0:
                status = 'done'
                disabled_bool = True
            else:
                status = 'block'
            self.grid.add_widget(
                Task(task_panel=self, status=status, category=category, number=i, level=self.store_name,
                     task_content=task['source'], typ=task['type'], disabled=disabled_bool, name=category + str(i),
                     id=category + str(i)))


class InfoPopup(FloatLayout):
    image = StringProperty('')

    def __init__(self, img, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.image = img

    def set_img(self, dt):
        self.ids.info.source = self.img


class FlashcardStartScreen(Screen):
    number_of_words = JsonStore('json/pl/cards.json').count()

    def __init__(self, **kw):
        super(FlashcardStartScreen, self).__init__(**kw)
        Clock.schedule_interval(self.update, .5)

    def popupcontent(self):
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Button())

        return self.layout

    def update(self, *args):
        self.flag.source = App.get_running_app().STORE.get('flag')['source']
        self.app = App.get_running_app()
        self.number_of_words = self.app.cards.count()

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_odpytywanie_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()

    def start(self):

        layout = CustomBoxLayout()
        layout.baza_slow.text = str(self.number_of_words) + '/50'
        layout.label_1.text = 'ZBYT MAŁA IŁOŚĆ SŁÓWEK!'
        layout.label_1.font_size = '30sp'
        layout.label_1.bold = True
        layout.label_1.color = (1, 0.7, 0.2, 1)
        layout.label_2.text = 'WYKONAJ JESZCZE KILKA ZADAŃ ABY ODBLOKOWAĆ TĄ AKTYWNOŚĆ'
        if self.number_of_words < 17:
            self.popup = Popup(title='', content=layout, size_hint=(None, None), size=(600, 300))
            self.popup.open()
        else:
            self.app.change_screen('flashcard_screen')


class FlashcardScreen(Screen):
    curr_card = None

    def __init__(self, **kw):
        super(FlashcardScreen, self).__init__(**kw)
        self.baza = JsonStore('json/pl/cards.json')

    def updatecard(self, *args):
        self.baza = App.get_running_app().cards
        self.answer.text = 'Sprawdż słówko'
        self.curr_card = getrandomcard(self.baza)
        self.question.text = getquestion(self.curr_card)

    def on_pre_enter(self, *args):
        self.updatecard()

    def updateAnsLabel(self, *args):
        self.answer.text = getanswer(self.curr_card)

    def dismiss_popup(self): pass

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_odpytywanie_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()


class StudyScreen(Screen):
    # store = JsonStore('json/pl.json', encoding='utf-8', ensure_ascii=False)

    def __init__(self, **kw):
        super(StudyScreen, self).__init__(**kw)
        self.store = JsonStore('json/pl.json')
        self.tasks_l = self.store.get('studyscreen')['tasks']
        self.flashcards_l = self.store.get('studyscreen')['flashcards']
        self.interesting_l = self.store.get('studyscreen')['interesting']
        self.achievements_l = self.store.get('studyscreen')['achievements']
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.store = App.get_running_app().STORE
        '''self.study_l = self.store.get('homescreen')['study']
        self.exit_l = self.store.get('homescreen')['exit']
        self.settings_l = self.store.get('homescreen')['parameters']
        self.credits_l = self.store.get('homescreen')['credits']'''
        self.tasks.text = self.store.get('studyscreen')['tasks']
        self.flashcards.text = self.store.get('studyscreen')['flashcards']
        self.interesting.text = self.store.get('studyscreen')['interesting']
        self.achievements.text = self.store.get('studyscreen')['achievements']
        self.flag.source = self.store.get('flag')['source']


with open('kivy/main.kv', encoding='utf8') as f:
    GUI = Builder.load_string(f.read())


# GUI = Builder.load_file("kivy/main.kv")


def my_callback(key, result):
    print('the key', key, 'has a value of', result)


class TaskScreen(Screen):
    def __init__(self, typ=None, task=None, name=None, **kw):
        super().__init__(**kw)
        self.task = task
        self.store = App.get_running_app().STORE
        self.typ = typ
        self.content = self.typ.content
        self.name = name
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.task_l.text = App.get_running_app().STORE.get('taskscreen')['task'] + " " + str(self.task.number)

        self.content = JsonStore(
            'json/' + App.get_running_app().lang + '/' + self.task.level + '/' + self.task.category + '_' + str(
                self.task.number) + '.json')
        self.typ.update(self.content)

    def on_enter(self, *args):

        self.typ.repeat()
        for child in [child for child in self.layout.children]:
            if isinstance(child, GridLayout):
                self.layout.remove_widget(child)
        self.title.text = self.content.get('title')['name']
        self.grid = self.typ.layout
        self.layout.add_widget(self.grid)

    def check_answers(self):
        self.store = App.get_running_app().STORE
        bad = self.typ.check()
        self.task.change_task_status(status=1) if bad else self.task.change_task_status(status=-1)
        self.popup = Popup(title='', size_hint=(None, None),
                           size=(600, 600))
        store = JsonStore(
            'json/' + App.get_running_app().lang + '/' + self.task.level +  '.json')
        print(store)
        #print(store['gram'][str(self.task.number)]['treal'])
        treal = store['P']['gram'][str(self.task.number)]['treal']

        if bad:
            self.popup.content = PopupType().create(popup=self.popup, msg='incorrect', content=self.store, treal=str(treal)+'/3')
        else:
            self.popup.content = PopupType().create(msg='correct', popup=self.popup, content=self.store)

        Clock.schedule_once(self.popup.open, 1.5)


class MainApp(App):
    pl = BooleanProperty(True)
    STORE = JsonStore('json/pl.json')
    cards = JsonStore('json/pl/cards.json')
    sound = SoundLoader.load('sound/music/arthur-vyncke_until-we-meet-again.mp3')
    sound.loop = True
    if sound:
        sound.play()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__()
        self.flag = 'images/Group 34.png'
        self.lang = 'pl'

    def build(self):
        time = datetime.now()

        print("color", get_color_from_hex('#F99B42'))

        Clock.schedule_interval(self.update_block, 1)
        '''self.st = JsonStore('json/pl/facts/eve.json')
        self.st.put('main_header', text="Jak obchodzi się w Polsce Boże Narodzenie?")
        self.st.put('p',
                     p_1="Święta Bożego Narodzenia są obchodzone 25 i 26 grudnia. \n24 natomiast obchodzi się Wigilię - uroczystą kolację \nrozpoczynającą święta. Inaczej niż na Ukrainie, gdzie święta \nobchodzi się 6 stycznia. Wtedy wówczas w Polsce jest święto \nTrzech Króli. ",
                     p_2="Boże Narodzenie zaczęto w Polsce obchodzić \nkrótko po tym, jak Polska stała się krajem chrześcijańskim w \n966 roku. Wtedy pierwszy władca kraju został poświęcony \nprzez kościół katolicki. Jednak przez wiele lat tradycja bardzo \nsię zmieniała.",
                     p_3="W dawnych czasach, zwłaszcza wtedy, Wigilia była pretekstem\n do wielkiego sprzątania. Kobiety sprzątały, prały \nfiranki, myły okna. Dzisiaj nie ma to tak wielkiego znaczenia i\n niektórzy się z tego śmieją mówiąc \„myję okna dla Jezusa\”,\n ale dalej dla wielu jest to okazja do nadrobienia obowiązków, \nktóre na codzień się zaniedbuje.",
                     p_4="Najważniejsza w Wigilii Bożego Narodzenia jest kolacja, co do\n której istnieją określone zasady. Stół musi być okryty białym \nobrusem. Pod nim znajduje się siano by przypominać w jakich \nw jakich warunkach urodził się Jezus. Przy stole powinno być \n wolne miejsce. Dla jednych oznacza to pamięć o zmarłych, \ndla innych na wypadek głodnego podróżnika, albo \nbezdomnego. Nawet jeśli mu nie otworzysz, to tradycja to \nnakazuje. Kolację zaczyna się gdy pojawi się pierwsza gwiazda \nna niebie. To nawiązanie do Gwiazdy Betlejemskiej.",
                    p_5="Na Wigilię powinno się przygotować 12 potraw. Dodatki, takie \njak sałatki, ciasta, kompot są liczone jako osobna potrawa. \nZ zup najczęściej się je barszcz czerwony, zupę grzybową. \nTradycyjnie dania są postne (bez mięsa, oprócz ryby). Z ryb  dawniej się jadło pstrąga, dorsza. Obecnie się je jednak karpia \ni wprowadziła to władza komunistyczna kilkadziesiąt lat temu. \nOprócz tego je się pierogi z kapustą i grzybami, sernik, \nlub inne ciasto, pije kompot z suszonych owoców. Pozostałe \ndania już nie są tak obowiązkowe i panuje tu dowolność.",
                    p_6="W trakcie Wigilii ludzie łamią się opłatkiem i składają sobie życzenia. \nRobi się to na znak przyjaźni i wzajemnej miłości. \nO północy odbywa się \ntakże \”pasterka\” – msza w kościele \nna upamiętnienie pasterzy którzy byli świadkami narodzin \nJezusa. Towarzyszy temu śpiewanie, lub słuchanie kolęd - \npiosenek bożonarodzeniowych.")
        '''
        return GUI

    def get_flag(self):
        return self.flag

    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name

    def add_task(self, task, typ):
        screen_manager = self.root.ids["screen_manager"]

        # screen_manager.add_widget(TaskScreen(task=task, content=content, type=1, name='zadanie' + str(task.number)))
        print(task.number)
        screen_manager.add_widget(TaskScreen(task=task, typ=typ, name='zadanie' + str(task.number)))
        screen_manager.current = 'zadanie' + str(task.number)

    def set_store(self, boolean):

        self.pl = boolean
        if self.pl:
            self.STORE = JsonStore('json/pl.json')
            self.lang = 'pl'
            self.cards = JsonStore('json/pl/cards.json')
            self.STORE.put('taskscreen', task='Zadanie')
            '''self.STORE.put('homescreen', study='Nauka', parameters='Ustawienia', credits='Credits',
                           exit='Wyjscie')
            self.STORE.put('studyscreen', tasks='Zadania', flashcards='Odpytywania', interesting='Ciekawostki',
                           achievements='Osiągnięcia')'''
            self.flag = 'images/Group 34.png'

        else:
            self.STORE = JsonStore('json/ukr.json')
            self.cards = JsonStore('json/ukr/cards.json')
            self.lang = 'ukr'
            self.STORE.put('taskscreen', task='Завдання')
            '''self.STORE.put('homescreen', study='Nauka', parameters='Ustawienia', credits='Credits',
                           exit='Wyjscie')
            self.STORE.put('studyscreen', tasks='Завдання', flashcards='Флешкарти', interesting='Цікавинки',
                           achievements='Досягнення')'''
            self.flag = 'images/pl_flag.png'

    def update_block(self, *args):
        self.block_tasks = JsonStore('json/' + self.lang + '/block_tasks.json')

        screen_manager = self.root.ids["screen_manager"]
        topics = ['P']
        category = ['gram', 'czyt', 'sluch']
        now = datetime.now()
        keys = self.block_tasks.keys()
        print(keys)
        for i in keys:
            task = self.block_tasks[i]
            for topic in topics:
                if task['topic'] == topic:
                    for categ in category:
                        if categ in task:
                            keys2 = task[categ].keys()
                            for j in keys2:
                                year = task[categ][j]['time']['year']
                                month = task[categ][j]['time']['month']
                                day = task[categ][j]['time']['day']
                                hour = task[categ][j]['time']['hour']
                                min = task[categ][j]['time']['min']
                                time2 = datetime(year=year, day=day, month=month, hour=hour, minute=min)
                                if (now - time2).total_seconds() >= 3600:
                                    store = JsonStore('json/' + self.lang + '/' + i + '.json')
                                    store[topic][categ][j]['treal'] = 0
                                    store[topic] = store[topic]
                                    self.block_tasks.delete(i)

    def update_cards(self, level=None, topic=None, number=None):
        words = JsonStore('json/' + self.lang + '/' + level + '/' + topic + number + '.json')
        self.cards = JsonStore('json/' + self.lang + '/cards.json')
        quantity = self.cards.count()
        j = 1
        for i in range(quantity, quantity + words.count() - 1):
            word = words[str(number) + '_' + str(j)]
            addCard(self.cards, question=word['question'], answer=word['answer'], category=words['category'], number=i)
            j += 1

    def set_level(self):
        screen_manager = self.root.ids["screen_manager"]
        level_a1 = TasksPanelScreen(name='a1', id='a1', store_name='a1', topic='P')
        screen_manager.add_widget(level_a1)



MainApp().run()
