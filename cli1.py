import requests
import curses
import os


class SocGPTBot:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.refresh()
        self.menu = ["Upload Log File", "Ask Questions", "Exit"]
        self.current_option = 0
        self.log_content = None
        self.base_url = 'http://127.0.0.1:5000'
        self.user_input = ""  # Initialize user_input attribute

    def upload_log(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Upload Log File", curses.A_BOLD)
        self.stdscr.addstr(2, 0, "Enter the path of the log file: ")
        log_path = self.stdscr.getstr(2, 30, 60).decode("utf-8")

        if os.path.exists(log_path):
            with open(log_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(
                    f'{self.base_url}/upload_log', files=files)
                if response.status_code == 200:
                    self.log_content = response.json()['message']
                    self.stdscr.addstr(4, 0, "Log file uploaded successfully.")
                else:
                    self.stdscr.addstr(4, 0, "Error uploading log file.")
        else:
            self.stdscr.addstr(4, 0, "Invalid file path.")

        self.stdscr.getch()
        self.run()

    def update_user_input(self, char):
        if char == curses.KEY_ENTER or char == 10:
            # Handle user input here
            self.stdscr.addstr(10, 0, f"User Input: {self.user_input}")
            self.stdscr.refresh()
            self.user_input = ""
        elif char == curses.KEY_BACKSPACE or char == 127:
            self.user_input = self.user_input[:-1]
        else:
            self.user_input += chr(char)

    def ask_questions(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Ask Questions", curses.A_BOLD)
        if self.log_content is None:
            self.stdscr.addstr(2, 0, "Please upload a log file first.")
        else:
            while True:
                # self.stdscr.clear()
                # self.stdscr.addstr(0, 0, "Ask Questions", curses.A_BOLD)

                self.stdscr.addstr(
                    2, 0, "Ask a question about the log (type 'exit' to go back): ")
                question = self.stdscr.getstr(2, 45, 60).decode("utf-8")

                if question.lower() == 'exit':
                    break

                self.stdscr.clear()

                payload = {'prompt': question}
                response = requests.post(
                    f'{self.base_url}/generate', json=payload)

                if response.status_code == 200:
                    self.stdscr.addstr(4, 0, f"User: {question}")
                    self.stdscr.addstr(
                        5, 0, f"Bot: {response.json()['response']}")
                else:
                    self.stdscr.addstr(
                        4, 0, "Error fetching response from server.")

        self.stdscr.getch()
        self.run()

    def display_menu(self):
        self.stdscr.clear()
        self.stdscr.addstr(
            0, 0, "Welcome to SocGPT - Your Security Analyst Helper", curses.A_BOLD)
        for idx, option in enumerate(self.menu):
            x = 2 + idx
            y = 1
            if idx == self.current_option:
                self.stdscr.addstr(x, y, f"> {option}", curses.A_REVERSE)
            else:
                self.stdscr.addstr(x, y, f"  {option}")

    def run(self):
        while True:
            self.display_menu()
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_option > 0:
                self.current_option -= 1
            elif key == curses.KEY_DOWN and self.current_option < len(self.menu) - 1:
                self.current_option += 1
            elif key in [curses.KEY_ENTER, ord('\n')]:
                if self.current_option == 0:
                    self.upload_log()
                elif self.current_option == 1:
                    self.ask_questions()
                elif self.current_option == 2:
                    self.stdscr.addstr(10, 0, "Exiting SocGPT. Goodbye!")
                    break

            self.stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    soc_gpt = SocGPTBot(stdscr)
    soc_gpt.run()


if __name__ == "__main__":
    curses.wrapper(main)
