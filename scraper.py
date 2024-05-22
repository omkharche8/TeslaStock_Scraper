import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.properties import StringProperty


# Function to fetch stock prices
def fetch_stock_price():
    url = "https://finance.yahoo.com/quote/TSLA/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    price_tag = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
    change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
    percent_change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})

    price = price_tag.text.strip() if price_tag else "N/A"
    change = change_tag.text.strip() if change_tag else "N/A"
    percent_change = percent_change_tag.text.strip() if percent_change_tag else "N/A"

    return price, change, percent_change


# Custom Button with 3D Effect and Animation
class AnimatedButton(ButtonBehavior, Widget):
    text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_button_release')
        with self.canvas.before:
            Color(0.1, 0.6, 0.6, 1)  # Button color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        anim = Animation(size=(self.size[0] * 0.98, self.size[1] * 0.98), duration=0.1)
        anim.start(self)

    def on_release(self):
        anim = Animation(size=(self.size[0] / 0.98, self.size[1] / 0.98), duration=0.1)
        anim.start(self)
        self.dispatch('on_button_release')

    def on_button_release(self):
        pass


# Kivy App
class StockApp(App):
    def build(self):
        # Set window properties
        Window.clearcolor = (0, 0, 0, 1)
        self.title = "Tesla Stock Price"

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title label
        title_label = Label(
            text="TESLA COST PRICE",
            font_size='32sp',
            color=(1, 1, 1, 1),
            font_name='Arial.ttf',
            size_hint=(1, 0.2)
        )

        # Price label
        self.price_label = Label(
            text="Fetching...",
            font_size='24sp',
            color=(1, 1, 1, 1),
            font_name='Arial.ttf',
            size_hint=(1, 0.6)
        )

        # Refresh button
        refresh_button = AnimatedButton(
            size_hint=(None, None),
            size=(200, 50),
            text="Refresh"
        )
        refresh_button.bind(on_button_release=self.refresh_stock_price)

        # Adding widgets to layout
        layout.add_widget(title_label)
        layout.add_widget(self.price_label)
        layout.add_widget(BoxLayout(size_hint=(1, 0.2)))  # Spacer

        # Center align the button using a box layout
        button_container = BoxLayout(size_hint=(1, 0.2))
        button_container.add_widget(BoxLayout(size_hint=(0.25, 1)))  # Left spacer
        button_container.add_widget(refresh_button)
        button_container.add_widget(BoxLayout(size_hint=(0.25, 1)))  # Right spacer

        layout.add_widget(button_container)

        self.refresh_stock_price()

        return layout

    def refresh_stock_price(self, *args):
        try:
            price, change, percent_change = fetch_stock_price()
            self.price_label.text = f"Tesla Stock (TSLA):\nPrice: ${price}\nChange: {change}\nPercentage Change: {percent_change}"
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=str(e)), size_hint=(0.6, 0.4))
            popup.open()


# Run the app
if __name__ == '__main__':
    StockApp().run()
