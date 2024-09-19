import FreeSimpleGUI as sg

label1 = sg.Text("Enter feet:")
input1 = sg.Input(key="feet")

label2 = sg.Text("Enter inches:")
input2 = sg.Input(key="inches")

button = sg.Button("Convert")
output_label = sg.Text(key="output", text_color="black")

window = sg.Window("Convertor", layout=[[label1, input1],
                                        [label2, input2],
                                        [button, output_label]])

while True:
    event, values = window.read()
    print(event)
    print(values)
    match event:
        case "Convert":
            feet = float(values["feet"])
            inches = float(values["inches"])
            meters = feet * 0.3048 + inches * 0.0254
            window["output"].update(value=str(meters) + " m")

        case sg.WIN_CLOSED:
            break

window.close()