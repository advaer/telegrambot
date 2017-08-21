from .utils import send_html_message
from .commands import BotCommands


class BotProcessing(BotCommands):
    def __init__(self):
        super().__init__()
        self.update_types_processors = {
            'message': self._process_message,
        }

    def _get_update_type(self, data):
        update_types = set(data.keys()) & set(self.update_types_processors.keys())
        if update_types:
            return list(update_types)[0]

    def _parse_command(self, request):
        request = request.split()
        command = self.known_commands.get(request[0].lower(), self.default)
        args = request[1:]

        return command, args

    def _process_message(self, data):
        message = data.get("message")
        request = message.get('text')
        chat_id = message.get('chat').get('id')
        command, args = self._parse_command(request)
        response_text = command(*args)
        response = send_html_message(chat_id=chat_id, content=response_text)
        return response.json()

    def _process_update_type(self, update_type, data):
        update_type_value = self.update_types_processors.get(update_type)
        if update_type_value:
            return update_type_value(data)
        return "Update type not implemented or incorrect"

    def process(self, data):
        update_type = self._get_update_type(data)
        response_text = self._process_update_type(update_type, data)
        return {'status': response_text}
