import PySimpleGUI as sg

def get_popup_window(text_for_student, img_for_student):
    images = []


    layout = [[sg.Text(text_for_student)]]
    if len(img_for_student) > 0:
        current_block = []
        for ind, _img in enumerate(img_for_student):
            current_block.append(sg.Image(filename=_img))
            if ind % 5 == 4:
                images.append(current_block)
                current_block = []
        images.append(current_block)
        img_column = sg.Column(images, scrollable=True, size=(1000, 300))
        layout.append([img_column])
    result_popup = sg.Window('Отчет о полете', layout, size=(1000, 400))
    return result_popup