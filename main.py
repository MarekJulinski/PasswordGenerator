from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import os

DIR = os.path.dirname(os.path.realpath(__file__))
# ---------------------------- FUNCTIONS ----------------------------------------#
def create_window():
    root = Tk()
    root.title('Password Generator')
    root.config(padx=70, pady=35)
    root.focus_force()
    
    return root

def create_canvas():
    canvas = Canvas(master=root, width=200, height=200)
    img = PhotoImage(file = str(DIR) + '/logo.png')
    canvas.grid(row=0, column=1)
    return canvas, img

def create_website():
    label = Label(master=root, text='Website:', font=("New Roman Times", 15, 'italic'))
    label.grid(row=1, column=0, pady=2)
    
    
    frame = Frame(master = root)
    entry_text = StringVar()
    entry = Entry(master=frame, width=22, textvariable=entry_text)
    entry.grid(row=0, column=0)
    
    button = Button(master=frame, text='Search', font=('New Roman Times', 15, 'italic'), command=search_password)
    button.grid(row=0, column=1)
    
    frame.grid(row=1, column=1, pady=2)
    
    return label, entry, entry_text

def create_username():
    label = Label(master=root, text='Email/Username:', font=('New Roman Times', 15, 'italic'))
    label.grid(row=2, column=0, pady=2)
    
    entry_text = StringVar()
    entry = Entry(width=31, textvariable=entry_text)
    entry.grid(row=2, column=1, pady=2)
    
    return label, entry, entry_text

def create_password():
    label = Label(master=root, text='Password:', font=("New Roman Times", 15, 'italic'))
    label.grid(row=3, column=0, pady = 2)
    
    frame = Frame(master=root)
    entry_text = StringVar()
    entry = Entry(master=frame, textvariable=entry_text)
    entry.grid(row=0, column=0)
    button = Button(master=frame, text='Generate', font=('New Roman Times', 15, 'italic'), command=password_generate)
    button.grid(row=0, column=1)
    frame.grid(row=3, column=1, pady=2)
    
    
    return label, frame, entry, button, entry_text

def create_save():
    button = Button(master=root, text='Save', font=('New Roman Times', 15, 'italic'), command=save_password, width=26)
    button.grid(row=4, column=1, pady= 10)
    
    return Button
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generate():
    password_length = random.randrange(8, 33)
    
    password_letters = "qwertyuiopasdfghjklzxcvbnm"
    password_numbers = "1234567890"
    password_symbols = "!@£$%^&*()€#\\{/}[']\"<>?,.~`+=-_"
    
    password_groups = [password_letters, password_numbers, password_symbols]
    
    password_structure = password_stage_one(password_groups, password_length)
    
    password_structure = password_stage_two(password_structure, len(password_structure), password_groups)
    
    password_structure = password_stage_three(password_structure, password_groups)
    
    password_structure = password_stage_four(password_structure, password_letters)
    
    password_text.set(password_structure)
    
    pyperclip.copy(password_structure)
          
def password_stage_one(groups, length):
    
    structure = [random.choice(groups) for i in range(length + 1)]
        
    if structure.count(groups[0]) < 2 or structure.count(groups[1]) < 2 or structure.count(groups[0]) < 2: 
        structure = password_stage_one(groups, length)
      
    return structure

def password_stage_two(structure, length, groups):

    for i in range(length-2):
        if structure[i] == structure[i+1] and structure[i] == structure[i+2]:
            
            while structure[i+2] == structure[i]:
                structure[i+2] = random.choice(groups)

    return structure

def password_stage_three(structure, groups):
    
    password = ''
    
    for i in structure:
        char = random.choice(i)
        
        if password.count(char) > 1:
            for group in groups:
                if i in group:
                    group.replace(char, '')
        
        password += char
    
    return password

def password_stage_four(structure, group):
    
    structure = list(structure)
    
    for i in range(len(structure)):
        if structure[i] in group:
            chance = random.randrange(0, 100)
            
            if chance % 2 == 0:
                structure[i] = structure[i].upper()
    
    structure = ''.join(char for char in structure)
    
    return structure
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    values = {'website':website_value.get(), 'username':username_value.get(), 'password':password_value.get()}
    filled = True
    
    for (entry, value) in values.items():
        value = value.replace(' ', '')
        if len(value) < 1:
            messagebox.showwarning('Empy Fields', 'All fields must be filled before saving!')
            filled = False
            break
        else:
            filled = True
            
    if filled:
        website = website_value.get()
        username = username_value.get()
        password = password_value.get()
        
        data = {website : 
            {'username' : username,
             'password' : password}
            }
        
        try:
            with open(str(DIR) + '/data.json', 'r') as f:
                file = json.load(f)
                file.update(data)
        except:
            file = data
        finally:
            with open(str(DIR) + '/data.json', 'w') as f:
                json.dump(file, f, indent = 4)
                f.close()
            website_value.delete(0, END)
            username_value.delete(0, END)
            password_value.delete(0, END)
# ---------------------------- SEARCH PASSWORD ----------------------------#
def search_password():
    
    website = website_value.get()
    
    website = website.lower()
    
    website.replace(' ', '')
    
    if len(website) > 0:
        
        try:
            with open(str(DIR) + '/data.json', 'r') as f:
                    file = json.load(f)
                    if website in file:
                        username_entry_text.set(file[website]['username'])
                        password_text.set(file[website]['password'])
                        pyperclip.copy(password_value.get())
                    else:
                        messagebox.showwarning('Unkown website', 'Sorry, the website has not been found!')
                    f.close()
                    
        except:
            messagebox('Unkown website', 'Sorry, the website has not been found!')
            
            
    
    pass
# ---------------------------- UI SETUP ------------------------------- #
if __name__ == '__main__':
    root = create_window()

    canvas, img = create_canvas()
    canvas_logo = canvas.create_image(100, 100, image = img)
    
    website_label, website_value, website_entry_text = create_website()

    username_label, username_value, username_entry_text = create_username()
    
    password_label, password_frame, password_value, password_button, password_text = create_password()
    
    save_button = create_save()

    root.mainloop()