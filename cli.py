from gpt4all import GPT4All

import curses


class SocGPTBot:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.refresh()
        self.menu = ["Search Wazuh OSSEC Information", "Analyze Logs", "Exit"]
        self.current_option = 0

        # Initializing GPT4All model
        # self.gpt_model = GPT4All("gpt4all-falcon-q4_0.gguf")

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

    def search_wazuh_ossec(self):
        # Implement code to search and retrieve information from Wazuh OSSEC
        pass

    def analyze_logs(self):
        # self.stdscr.clear()
        # self.stdscr.addstr(
        #     0, 0, "Analyzing Logs - Chat Interface", curses.A_BOLD)
        # self.stdscr.refresh()

        # conversation = []

        # with self.gpt_model.chat_session() as chat:
        #     while True:
        #         self.stdscr.addstr(2, 0, "User: ")
        #         user_input = self.stdscr.getstr(2, 6, 60).decode("utf-8")

        #         conversation.append(f"User: {user_input}")
        #         # Display last 5 messages
        #         self.stdscr.addstr(4, 0, "\n".join(conversation[-5:]))

        #         response = chat.generate(prompt=user_input, temp=0)

        #         conversation.append(f"Bot: {response}")
        #         # Display last 5 messages
        #         self.stdscr.addstr(6, 0, "\n".join(conversation[-5:]))

        #         if user_input.lower() == "exit":
        #             break

        #         self.stdscr.refresh()
        pass

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
                    self.search_wazuh_ossec()
                elif self.current_option == 1:
                    self.analyze_logs()
                elif self.current_option == 2:
                    self.stdscr.addstr(10, 0, "Exiting SocGPT. Goodbye!")
                    self.stdscr.refresh()
                    curses.napms(1000)
                    break

            self.stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    soc_gpt = SocGPTBot(stdscr)
    soc_gpt.run()


if __name__ == "__main__":
    curses.wrapper(main)
