import PySimpleGUI as sg      

window_rows = [[sg.Text('SHA-1 and SHA-256 Hashes for the file')],      
                 [sg.InputText(), sg.FileBrowse()],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('SHA-1 & 256 Hash', window_rows)    

event, values = window.Read()    
window.Close()

source_filename = values[0]    