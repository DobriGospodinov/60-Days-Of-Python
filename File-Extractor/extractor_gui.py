import FreeSimpleGUI as sg
from extractor_backend import extract_archive


label1 = sg.Text("Select file to extract:")
input1 = sg.Input()
choose_button1 = sg.FileBrowse("Choose", key="file")

label2 = sg.Text("Select destination folder:")
input2 = sg.Input()
choose_button2 = sg.FolderBrowse("Choose", key="folder")

extract_button = sg.Button("Extract")
output_label = sg.Text(key="output", text_color="black")

col1 = sg.Column([[label1], [label2]])
col2 = sg.Column([[input1], [input2]])
col3 = sg.Column([[choose_button1], [choose_button2]])

window = sg.Window("File Extractor",
                   layout=[[col1, col2, col3],
                           [extract_button, output_label]])
while True:
    event, values = window.read()
    archive_path = values["file"]
    dest_dir = values["folder"]
    extract_archive(archive_path, dest_dir)
    window["output"].update(value="Extraction completed!")

window.close()