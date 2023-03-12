from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg

CAL_GOAL = 3000
PROT_GOAL = 180
FAT_GOAL = 80
CARBS_GOAL = 300

total_calories = 0

@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int

class Node:
    def __init__(self, food: Food, next_node=None):
        self.food = food
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
         

    def add_node(self, food: Food):
        new_node = Node(food)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
    
    

    def remove_node(self, name):
        temp = self.head
        prev = None

        if(temp is not None):
            if(temp.food.name == name):
                self.head = temp.next
                temp = None
                return
        while(temp is not None):
            if temp.food.name == name:
                break
            prev = temp
            temp = temp.next
        
        if(temp == None):
            return
        
        prev.next = temp.next

        temp = None


    def get_food(self, desired):
        node = self.head
        while node is not None:
            if node.food.name == desired:
                return node
            node = node.next
        return None








layout = [
    [sg.Text("PROGRESS BAR")],
    [sg.ProgressBar(CAL_GOAL, orientation='h', expand_x=True, size=(30, 20),  key='BAR')],
    [sg.Text("Choose an option:")],
    [sg.Button("Add new food", key="add_food"), sg.Button("Delete Food", key = 'delete_food'), sg.Button("Visualize progress", key="visualize"), sg.Button("Quit", key="quit")], 
    [sg.Multiline(size=(40, 10), key='-MULTILINE-')],
]

sg.theme('DarkAmber')

main_window = sg.Window("Macro Tracker", layout, size = (500,500), element_justification='c')
    
my_list = LinkedList()

text = ""


while True:
    event, values = main_window.read()

    if event == sg.WIN_CLOSED or event == 'quit':
        break

    if event == "add_food":
        layout = [
            [sg.Text("Adding a new food!")],
            [sg.Text("Name: "), sg.InputText()],
            [sg.Text("Cals: "), sg.InputText()],
            [sg.Text("Protiens: "), sg.InputText()],
            [sg.Text("Fats: "), sg.InputText()],
            [sg.Text("Carbs: "), sg.InputText()],
            [sg.Submit(), sg.Cancel()]      
        ]
       
        add_food_window = sg.Window("Add new food", layout)
        event, values = add_food_window.read()
        

        if event == "Submit":
            if values[0] == "":
                sg.popup("Missing Value")
                add_food_window.close()
            elif values[1] == "":
                sg.popup("Missing Value")
                add_food_window.close()
            elif values[2] == "":
                sg.popup("Missing Value")
                add_food_window.close()
            elif values[3] == "":
                sg.popup("Missing Value")
                add_food_window.close()
            elif values[4] == "":
                sg.popup("Missing Value")
                add_food_window.close()
            else:
                new_text = "Food: " + values[0] + " | " + "Cals: " + values[1]
                text += new_text + '\n'
                main_window['-MULTILINE-'].update(value=text)
                name = values[0]
                calories = int(values[1])
                proteins = int(values[2])
                fats = int(values[3])
                carbs = int(values[4])
                food = Food(name, calories, proteins, fats, carbs)
                my_list.add_node(food)
                add_food_window.close()
                total_calories += calories
                main_window['BAR'].update(total_calories)
                sg.popup("Done!")


    if event == 'delete_food':
        layout = [
        [sg.Text("Deleting a food item!")],
        [sg.Text("Name: "), sg.InputText()],
        [sg.Submit(), sg.Cancel()],
        [sg.Text("Type in Food name from main window")],
        
    ]

        delete_food_window = sg.Window("Delete Food", layout)
        event, values = delete_food_window.read()

        if event == "Submit":
            name = values[0]
            if my_list.get_food(name) is not None:
                deleted_food = my_list.get_food(name)
                total_calories -= deleted_food.food.calories
                my_list.remove_node(name)
                # Remove deleted food from the text
                text_lines = text.split('\n')
                text_lines = [line for line in text_lines if name not in line]
                text = '\n'.join(text_lines)
                # Update multiline with new text
                main_window['-MULTILINE-'].update(value=text)
                main_window['BAR'].update(total_calories)
                delete_food_window.close()
            else:
                sg.popup("Food Cannot Be Found")
                delete_food_window.close()

        elif event == "Cancel":
            delete_food_window.close()
        
            

        
            

               
       
        
        
            
    
    elif event == "visualize":
        calorie_sum = 0
        proteins_sum = 0
        fats_sum = 0
        carbs_sum = 0
        
        node = my_list.head
        while node is not None:
            food = node.food
            calorie_sum += food.calories
            proteins_sum += food.protein
            fats_sum += food.fat
            carbs_sum += food.carbs
            node = node.next
        if len(main_window['-MULTILINE-'].get()) > 0:
            fig, axs = plt.subplots(2,2)
            axs[0, 0].pie([proteins_sum, fats_sum, carbs_sum], labels=["Proteins", "Fats", "Carbs"], autopct="%1.1f%%")
            axs[0, 0].set_title("Macros")
            axs[0,1].bar([0, 1, 2], [proteins_sum, fats_sum, carbs_sum], width = 0.4)
            axs[0,1].bar([0.5, 1.5, 2.5], [PROT_GOAL, FAT_GOAL, CARBS_GOAL], width = 0.4)
            axs[0,1].set_xticks([0.5, 1.5, 2.5])
            axs[0,1].set_xticklabels(["Proteins", "Fats", "Carbs"])
            axs[0,1].set_title("Macros Goal")
            axs[1,0].bar(["Calories"], [calorie_sum], width = 0.4)
            axs[1,0].bar(["Calories Goal"], [CAL_GOAL], width = 0.4)
            axs[1,0].set_title("Calories Goal")
            axs[1,0].set_ylim([0, CAL_GOAL*1.2])
            plt.show()
        else:
            sg.popup("Not Enough Data")
    
    elif event == "quit":
        done = True
    