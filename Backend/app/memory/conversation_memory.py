class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_formatted_history(self):
        formatted = ""
        for msg in self.history:
            formatted += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return formatted

    def clear(self):
        self.history = []
