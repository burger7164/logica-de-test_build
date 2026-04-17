window hide
screen puzzle_choice(task_text="", options=None):
    tag menu
    if options is None:
        $ options = ["Да", "Нет"]
        
    frame:
        xalign 0.5 yalign 0.5
        xpadding 60 ypadding 40
        vbox:
            spacing 20
            text "[task_text]" size 32 xalign 0.5
            for opt in options:
                textbutton str(opt):
                    xsize 300
                    action Return(str(opt))
            textbutton "Отмена" action Return("") xalign 0.5

screen puzzle_drag(task_text="", items=None, hint=""):
    default dropped_items = []
    if items is None:
        $ items = []
        
    frame:
        xalign 0.5 yalign 0.5
        xpadding 60 ypadding 40
        vbox:
            text "[task_text]" size 32 xalign 0.5
            if hint:
                text "[hint]" size 22 color "#aaa" xalign 0.5
            null height 15
            hbox:
                spacing 15
                for item in items:
                    drag:
                        drag_name item
                        child Text(str(item), size=26, color="#fff", outlines=[(2,"#000",0,0)])
                        draggable True
                        dragged on_drag_drop(dropped_items, item)
            null height 15
            hbox:
                spacing 10
                text "Порядок: " size 22
                text " ".join(dropped_items) size 22 color "#ffcc00"
            textbutton "Подтвердить" action Return(",".join(dropped_items)) xalign 0.5

init python:
    def on_drag_drop(dropped_list, item):
        if item not in dropped_list:
            dropped_list.append(item)