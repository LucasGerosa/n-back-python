import IOUtils
from TestCase import TestCase
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import notes_config
import configparser
import tkinter as tk

class MyGUI:
    
    def __init__(self) -> None:
        
        self.root = tk.Tk()
        self.root.title(PROJECT_NAME)
        self.root.geometry("800x500")
        #self.label = tk.Label(self.root, text='')
        #self.check_state = tk.IntVar()
        self.set_main_menu()
        self.set_settings()
        self.main_menu.pack()
        self.root.mainloop()
        self.last_frame = None
    
    def destroy_all_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_main_menu_button(self, frame):
        main_menu_button = tk.Button(frame, text='Main menu', font=('Arial', 18), command=lambda:self.main_menu.tkraise())
        return main_menu_button

    def set_main_menu(self):
        self.main_menu = tk.Frame(self.root)
        self.get_settings_button(self.main_menu).pack()
    
    def set_settings(self):
        self.settings = tk.Frame(self.root)
        self.get_main_menu_button(self.settings).pack()

    def go_back(self):
        if self.last_frame != None:
            self.last_frame.tkraise()
        else:
            raise Exception("No last frame.")

    def get_back_button(self):
        back_arrow = tk.PhotoImage(file="static/back_button.png")
        back_label = tk.Label(self.root, image=back_arrow)
        back_label.bind("<Button-1>", lambda event: self.go_back())
        return back_label

    def get_settings_button(self, frame):
        button_settings = tk.Button(frame, text='Settings', font=('Arial', 18), command=lambda:self.settings.tkraise())
        return button_settings
    
''' def settings(self):
        self.root.destroy() #destroys the window itself
        self.destroy_all_widgets()
        self.get_back_button().pack()
        self.get_main_menu_button().pack()
        notes_setting_label = notes_config.get_setting(notes_config.NOTES_SETTING)

        print("Settings accessed")'''
    



def retrieveInfo():
        name = input("Player Name:\n")
        while True:
            bpm = input(f"Bpm (default: {DEFAULT_BPM}bpm):\n")
            if bpm == "":
                bpm = DEFAULT_BPM
                break
            elif bpm.isnumeric():
                bpm = float(bpm)
                break
            print('That is not a valid bpm number. Try again.')
        
        while True:
            instrument = input(f"Instrument ({' or '.join(INSTRUMENTS)}; {DEFAULT_INSTRUMENT } is default):\n")
            if instrument == "":
                instrument = 'piano'
                break
            elif instrument in INSTRUMENTS:
                break
            print('That is not a valid instrument; try again.')
        return name, bpm, instrument

def home() -> str:
    return input("1 -> Start\n2 -> Import from file\n0 -> Quit\nsettings -> to change the settings\nsettings_reset -> to reset all settings to default (this might fix some bugs regarding settings\n> ")
    
def settings_prompt():
    try:
        while True:
            setting = input(f"""
What setting do you want to alter? Current values:
{notes_config.NOTES_SETTING} = {notes_config.get_setting(notes_config.NOTES_SETTING)}
{notes_config.NOTE_INTENSITY_SETTING} = {notes_config.get_setting(notes_config.NOTE_INTENSITY_SETTING)}
{notes_config.NOTE_VALUE_SETTING} = {notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)}
""")    
        
            if notes_config.does_setting_exist(setting):
                new_value = input("What value do you want to alter it to?\n")
                notes_config.change_setting(setting, new_value)
                print("Settings saved.")
                break
            print("Setting doesn't exist. Try again.")
    except (KeyError, configparser.ParsingError) as e:
        reset_bool = input(f"{e}\nsettings.ini file is probably corrupted. Reset it to default settings?\n ({user_input_messages.yes_or_no})")
        if reset_bool == user_input_messages.yes:
            notes_config.reset_settings()
            print("All settings have been successfully reset.\n")
        else:
            print('Cancelling operation. Fix your settings.ini file or contact the developers.\n')

def old_main() -> None:
    IOUtils.cls()
    while True:
        option = home()
        if option == "debug":
            TestCase.debug()
            input("Debugging session finished.\nPress ENTER to continue.")
            return
        if option == 'settings':
            settings_prompt()
        
        elif option == 'settings_reset':
            notes_config.reset_settings()
            print("All settings have been successfully reset.")

        elif not option.isnumeric() or not 0 <= int(option) <= 2:
            print(f"The input needs to be a number from 0 to 2. '{option}' was given. Try again.\n\n")
        
        else:

            while True:
                if option == '0':
                    return
                info =  retrieveInfo()  
                if option == '2':
                    TestCase.executeFromFile(*info)
                        
                elif option == '1':
                    TestCase.executeLoop(*info)
                
                else:
                    raise TypeError(f"The input needs to be a number from 0 to 2. {option} was given.")
                
def main():
    MyGUI()
        
if __name__ == "__main__":
    main()
