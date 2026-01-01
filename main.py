from core.utils import CheckInput

class MainMenu:
    def __init__(self, total_menu):
        self.total_menu = total_menu
        self.choosen_menu = 0
        self.choosen_sub_menu = 0
        self.running = True
        
    def show_menu(self):
        print("Daily Expenses Manager")
        print("< ------------------ >")
        print("1. Salary DATA")
    
    def show_sub_menu(self):
        pass
    
    def handle_choices(self, index):
        while True:
            if CheckInput.check_digit(index, 1, self.total_menu):
                index = int(index)
                if index == 1:
                    break
            elif index.lower() == "q":
                self.exit()
    
    def run(self):
        while True:
            self.show_menu()
            index = input("Select by index (q to exit)")
            self.handle_choices(index)
            
    def exit(self):
        self.running = False
    
if __name__ == "__main__":
    app = MainMenu(1)
    app.run()