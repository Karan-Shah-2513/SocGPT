from gpt4all import GPT4All

import curses
import requests
import json

class SocGPTBot:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.refresh()
        self.pad = curses.newpad(1000, 100)
        self.menu = ["Search Wazuh OSSEC Information", "Analyze Logs", "Get Running Processes from Agent", 
                     "Get Ports Information from Agent", "Get Packages Information from Agent", "Get Agent Information",
                        "Get Agent Network Protocols", "Get Agent Hardware",
                     "Exit"]
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
    
    def get_jwttoken(self):
        url = 'https://localhost:55000/security/user/authenticate'
        username = 'wazuh-wui'
        password = 'MyS3cr37P450r.*-'

        # Use the auth parameter to include basic authentication credentials
        response = requests.post(url, auth=(username, password), verify=False)  # Set verify to False if you want to ignore SSL verification (not recommended for production)

        print(response.status_code)
        
        return response.json().get('data').get('token')
    
    def get_running_processes(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/processes?pretty=true&limit=10'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()
    
    def get_running_ports(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/ports?pretty=true&limit=10'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()
    
    def get_running_packages(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/packages?pretty=true&limit=10'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()
    
    def get_agent_info(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/os?pretty=true'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()
    
    def get_agent_netproto(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/netproto?pretty=true'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()
    
    def get_agent_hardware(self):
        jwt_token = self.get_jwttoken()
        url = 'https://localhost:55000/syscollector/001/hardware?pretty=true'
        headers = {'Authorization': f'Bearer {jwt_token}'}
        
        response = requests.get(url, headers=headers, verify=False)

        return response.json()


    def display_json_pretty(self, data):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Running Processes (Pretty Format)", curses.A_BOLD)

        if data:
            json_str = json.dumps(data, indent=2)

            # Clear the pad before displaying new content
            self.pad.clear()

            # Display the formatted JSON string on the pad
            self.pad.addstr(0, 0, json_str)

            # Refresh the pad to update the screen
            self.pad.refresh(0, 0, 2, 0, curses.LINES - 1, curses.COLS - 1)
        else:
            self.stdscr.addstr(2, 0, "No processes found.")

        curses.napms(10000)
        
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
                    res = self.get_running_processes()
                    self.display_json_pretty(res)
                elif self.current_option == 3:
                    res = self.get_running_ports()
                    self.display_json_pretty(res)
                elif self.current_option == 4:
                    res = self.get_running_packages()
                    self.display_json_pretty(res)
                elif self.current_option == 5:
                    res = self.get_agent_info()
                    self.display_json_pretty(res)
                elif self.current_option == 6:
                    res = self.get_agent_netproto()
                    self.display_json_pretty(res)
                elif self.current_option == 7:
                    res = self.get_agent_hardware()
                    self.display_json_pretty(res)
                elif self.current_option == 8:
                    self.stdscr.addstr(10, 0, "Exiting SocGPT. Goodbye!")
                    self.stdscr.refresh()
                    curses.napms(1000)
                    break

            self.stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    soc_gpt = SocGPTBot(stdscr)
    soc_gpt.run()


if __name__ == "__main__":
    curses.wrapper(main)

   
    
