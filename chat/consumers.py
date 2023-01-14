from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        self.send(text_data=text_data)
    
    def send(self, text_data=None, bytes_data=None, close=False):
        self.send_text(text_data=text_data)

