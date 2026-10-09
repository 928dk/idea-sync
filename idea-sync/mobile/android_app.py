from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import requests
import threading

# CONFIG (Update with your home IP)
HUB_URL = "http://198.51.100.10:8888"
TOKEN = "your-secret-token-here"

class AIClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Header
        self.add_widget(Label(text="AI GRID MOBILE", font_size='24sp', size_hint_y=None, height=50))

        # Input
        self.input_field = TextInput(hint_text="Ask the Supercomputer...", multiline=False, size_hint_y=None, height=100)
        self.add_widget(self.input_field)

        # Buttons
        self.btn = Button(text="SEND TO GRID", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        self.btn.bind(on_press=self.send_prompt)
        self.add_widget(self.btn)

        # Output area
        self.scroll = ScrollView()
        self.output_label = Label(text="Welcome. Ready for requests.", size_hint_y=None, halign='left', valign='top')
        self.output_label.bind(size=self.output_label.setter('text_size'))
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)

    def send_prompt(self, instance):
        prompt = self.input_field.text
        if not prompt: return
        
        self.output_label.text = "Processing on home grid..."
        threading.Thread(target=self.bg_request, args=(prompt,)).start()

    def bg_request(self, prompt):
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}
        
        try:
            resp = requests.post(f"{HUB_URL}/proxy/generate", json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                self.output_label.text = resp.json().get('response', 'No response')
            else:
                self.output_label.text = f"Error: {resp.status_code}"
        except Exception as e:
            self.output_label.text = f"Failed to connect to home: {str(e)}"

class AIApp(App):
    def build(self):
        return AIClient()

if __name__ == "__main__":
    AIApp().run()
