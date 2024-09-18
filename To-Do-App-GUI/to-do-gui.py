import functions
import FreeSimpleGUI as sg


label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo")
add_button = sg.Button("Add")


# The label and input box below are displayed on the same line, if they are part of the same list [[label, input_box]].

# If they are in two different lists, like [[label], [input_box]], they would have been displayed above one another.

# So with the current layout=[[label], [input_box, add_button]], the label is displayed on the first row, then
# the input box and 'add' button are displayed on the second row.

window = sg.Window('My To-Do App', layout=[[label], [input_box, add_button]])
window.read()
window.close()