from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial

class Node:
    def __init__(self, name, nature, year, sector):
        self.nature = nature
        self.name = name
        self.year = year
        self.sector = sector
        self.leftChild = None
        self.rightChild = None

    def dfs(self, conditions):
        stack = []
        files = []
        stack.append(self)
        while stack:
            actualNode = stack.pop(-1)
            if actualNode.leftChild:
                stack.append(actualNode.leftChild)
            if actualNode.rightChild:
                stack.append(actualNode.rightChild)
            if (conditions[0] == 1 and actualNode.nature) or (conditions[1] == 1 and not actualNode.nature):
                files.append(actualNode)
            if (
                    (conditions[2][0] == 1 and actualNode.year == 2023) or
                    (conditions[2][1] == 1 and actualNode.year == 2022) or
                    (conditions[2][2] == 1 and actualNode.year == 2021) or
                    (conditions[2][3] == 1 and actualNode.year == 2020)
            ):
                files.append(actualNode)
            if (
                    (conditions[3][0] == 1 and actualNode.sector.lower() == 'business expenses') or
                    (conditions[3][1] == 1 and actualNode.sector.lower() == 'transportation') or
                    (conditions[3][2] == 1 and actualNode.sector.lower() == 'restaurants') or
                    (conditions[3][3] == 1 and actualNode.sector.lower() == 'professional fees')
            ):
                files.append(actualNode)
        return files[::-1]


class BinaryTree():
    def __init__(self):
        self.root = None

    def insert(self, nodo):
        if not self.root:
            self.root = nodo
        else:
            self.insertNode(nodo, self.root)

    # STEP2
    def insertNode(self, nodo, parent_node):
        if not self.root.leftChild and nodo.nature == 0: self.root.leftChild = nodo
        elif not self.root.rightChild and nodo.nature == 1: self.root.rightChild = nodo
        else:
            if nodo.year < parent_node.year:
                if parent_node.leftChild:
                    self.insertNode(nodo, parent_node.leftChild)
                else:
                    parent_node.leftChild = nodo
            else:
                if parent_node.rightChild:
                    self.insertNode(nodo, parent_node.rightChild)
                else:
                    parent_node.rightChild = nodo

class MainApp(App):
    def build(self):
        self.icon = 'wax_seal-512.png'
        self.operators = ['Export', 'Filter', 'Upload']
        self.last_was_operator = None
        self.last_button = None
        self.nodes = []
        self.binary_tree = BinaryTree()
        self.file_paths = {}

        self.main_layout = BoxLayout(orientation='vertical')
        self.solution = TextInput(background_color = 'grey', foreground_color = 'black', readonly = True)
        self.document_label = Label()
        self.main_layout.add_widget(self.document_label)

        for i in self.operators:
            h_layout = BoxLayout()
            button = Button(
                text=i, font_size=30, background_color='blue',
                pos_hint={'center_x': 0.5, "center_y": 0.5}
            )
            if i == 'Export': button.bind(on_press=self.export_files)
            elif i == 'Filter': button.bind(on_press=self.show_filter_popup)
            else: button.bind(on_press=self.upload_selected_file)
            h_layout.add_widget(button)
            self.main_layout.add_widget(h_layout)

        return self.main_layout

    def show_filter_popup(self, instance):
        filter_layout = BoxLayout(orientation='vertical')
        buttons = [
            ['Deduced taxes'],
            ['Non-Deduced taxes'],
            ['Year'],
            ['   2023'],
            ['   2022'],
            ['   2021'],
            ['   2020'],
            ['Sector'],
            ['   Business Expenses'],
            ['   Transportation'],
            ['   Restaurants'],
            ['   Professional fees'],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label, font_size=30, background_color='blue',
                    pos_hint={'center_x': 0.5, "center_y": 0.5}
                )
                button.bind(on_press=self.filter_data)
                h_layout.add_widget(button)
            filter_layout.add_widget(h_layout)

        def submit_callback(submit_instance):
            filter_popup.dismiss()

        enter_button = Button(
            text='Enter', font_size=30, background_color='white',
            pos_hint={'center_x': 0.5, "center_y": 0.5}, on_press=submit_callback
        )
        filter_layout.add_widget(enter_button)

        filter_popup = Popup(title='Filters', content=filter_layout, size_hint=(0.8, 0.8))
        filter_popup.open()

    def filter_data(self, instance):
        try:
            button_text = instance.text
            conditions = [0, 0, [0, 0, 0, 0], [0, 0, 0, 0]]

            if button_text == 'Deduced taxes':
                conditions[0] = 1
            elif button_text == 'Non-Deduced taxes':
                conditions[1] = 1
            elif button_text.strip() == '2023':
                conditions[2][0] = 1
            elif button_text.strip() == '2022':
                conditions[2][1] = 1
            elif button_text.strip() == '2021':
                conditions[2][2] = 1
            elif button_text.strip() == '2020':
                conditions[2][3] = 1
            elif button_text.strip() == 'Business Expenses':
                conditions[3][0] = 1
            elif button_text.strip() == 'Transportation':
                conditions[3][1] = 1
            elif button_text.strip() == 'Restaurants':
                conditions[3][2] = 1
            elif button_text.strip() == 'Professional fees':
                conditions[3][3] = 1

            self.last_button = button_text
            self.last_was_operator = self.last_button in self.operators
            result = self.binary_tree.root.dfs(conditions)
            self.update_main_screen(result)
        except Exception as e:
            print(f"Error processing input: {e}")


    def upload_selected_file(self, instance):
        upload_layout = BoxLayout(orientation='vertical')
        file_path = TextInput(multiline=False, text='', hint_text='Enter file path')
        upload_layout.add_widget(file_path)

        name_input = TextInput(multiline=False, text='', hint_text='Enter name')
        upload_layout.add_widget(name_input)
        nature_input = TextInput(multiline=False, text='', hint_text='Enter nature (0 for deduced, 1 for non-deduced)')
        upload_layout.add_widget(nature_input)
        year_input = TextInput(multiline=False, text='', hint_text='Enter year (from 2020 to 2023)')
        upload_layout.add_widget(year_input)
        sector_input = TextInput(multiline=False, text='', hint_text='Enter sector (Transportation/ Business expenses/ Professional fees/ Restaurants)')
        upload_layout.add_widget(sector_input)

        def submit_callback(submit_instance):
            try:
                name = str(name_input.text)
                nature = int(nature_input.text)
                year = int(year_input.text)
                sector = str(sector_input.text)

                node = Node(name=name, nature=nature, year=year, sector=sector)
                self.nodes.append(node)
                self.file_paths[node.name] = str(file_path.text)
                self.binary_tree.insert(node)

                self.update_main_screen(self.nodes)
                upload_popup.dismiss()

            except Exception as e:
                print(f"Error processing input: {e}")

        submit_button = Button(text='Submit', on_press=submit_callback)
        upload_layout.add_widget(submit_button)

        upload_popup = Popup(title='File Information', content=upload_layout, size_hint=(0.8, 0.8))
        upload_popup.open()

    def export_files(self, instance):
        try:
            select_layout = BoxLayout(orientation='vertical')
            self.lista_export = []

            for file in self.nodes:
                button = Button(
                    text=f'Path for {file.name}: {self.file_paths[file.name]}', font_size=30, background_color='white',
                    pos_hint={'center_x': 0.5, "center_y": 0.5}
                )
                select_layout.add_widget(button)

            for n in self.nodes:
                if instance.text == f'Path for {n.name}: {self.file_paths[n.name]}': self.lista_export.append(n)

            def submit_callback(instance):
                select_popup.dismiss()
                self.update_main_screen(self.lista_export)

            print(self.lista_export)
            enter_button = Button(text='Enter', on_press= submit_callback)
            select_layout.add_widget(enter_button)

            select_popup = Popup(title='Export files', content=select_layout, size_hint=(0.8, 0.8))
            select_popup.open()

        except Exception as e:
            print(f"Error processing input: {e}")

    def update_main_screen(self, lista_nodos):
        self.main_layout.clear_widgets()

        # Re-add buttons for select, filter, and upload
        for op in self.operators:
            button = Button(
                text=op, font_size=30, background_color='blue',
                pos_hint={'center_x': 0.5, "center_y": 0.5}
            )
            if op == 'Export':
                button.bind(on_press=self.export_files)
            elif op == 'Filter':
                button.bind(on_press=self.show_filter_popup)
            elif op == 'Upload':
                button.bind(on_press=self.upload_selected_file)
            self.main_layout.add_widget(button)

        for node in lista_nodos:
            document_label = Label(text=node.name)
            self.main_layout.add_widget(document_label)


if __name__ == '__main__':
        app = MainApp()
        app.run()