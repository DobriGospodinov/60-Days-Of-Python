import FreeSimpleGUI
import FreeSimpleGUI as sg

FreeSimpleGUI.theme("BlueMono")

label1 = sg.Text("Enter feet:")
input1 = sg.Input(key="feet")

label2 = sg.Text("Enter inches:")
input2 = sg.Input(key="inches")

convert_button = sg.Button("Convert")
exit_button = sg.Button("Exit")
output_label = sg.Text(key="output", text_color="black")

col1 = sg.Column([[label1], [label2]])
col2 = sg.Column([[input1], [input2]])

window = sg.Window("Convertor", layout=[[col1, col2],
                                             [convert_button, exit_button, output_label]])

while True:
    event, values = window.read()

    match event:
        case "Convert":
            try:
                feet = float(values["feet"])
                inches = float(values["inches"])
                meters = feet * 0.3048 + inches * 0.0254
                window["output"].update(value=str(meters) + " m")
            except ValueError:
                sg.popup("Please enter feet and inches to convert!")

        case "Exit":
            break

        case sg.WIN_CLOSED:
            break

window.close()