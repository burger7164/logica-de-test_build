window hide

style action_button:
    outlines [ (2, "#000000", 0, 0) ] size 35 color "#c49227" xalign 0.5

style frame_style:
    background Frame("gui/frame.png", 20, 20)
    xpadding 30
    ypadding 20

label leave_lvl:
    init python:
        Return("")
    jump level_generic

screen puzzle_choice(task_text="", options=None):
    tag menu
    if options is None:
        $ options = ["Да", "Нет"]

    frame:
        xalign 0.5 yalign 0.5
        xpadding 110 ypadding 57
        vbox:
            spacing 20
            text "[task_text]" outlines [ (1, "#000000", 0, 0) ] size 35 xalign 0.5 yalign 0.1 
            
            for opt in options:
                button:
                    xalign 0.5
                    xsize 300
                    ysize 50
                    background None
                    hover_background None
                    action Return(str(opt))
                    
                    text str(opt):
                        xalign 0.5
                        yalign 0.5
                        outlines [ (1, "#000000", 0, 0) ] 
                        size 35
                        hover_color "#7e4525"

            text "\n{a=jump:leave_lvl}Отмена{/a}" outlines [ (2, "#000000", 0, 0) ] size 35 color "#c49227" xalign 0.5

# ============== Порядок ==============

screen puzzle_order(task_text="", items=None, hint=""):
    default selected_order = []
    default available_items = list(items) if items else []
    
    frame:
        xalign 0.5 yalign 0.5
        xpadding 110 ypadding 90
        background Frame("gui/frame.png", 10, 10)
        
        vbox:
            xalign 0.5
            spacing 20
            text task_text outlines [ (1, "#000000", 0, 0) ] size 35 xalign 0.5 yalign 0.1 
            
            null height 20
            
            # Выбранный порядок
            frame:
                xalign 0.5
                xpadding 20 ypadding 20
                background Frame("gui/frame.png", 10, 10)
                vbox:
                    text "Порядок:" size 35 xalign 0.5 outlines [ (1, "#000000", 0, 0) ]
                    if selected_order:
                        for i, item in enumerate(selected_order, 1):
                            text "[i]. [item]" outlines [ (2, "#000000", 0, 0) ] color"#c49227" size 35 xalign 0.5
                    else:
                        text "Ничего не выбрано!" size 26 

            frame:
                xalign 0.5
                background Frame("gui/frame.png", 10, 10)
                xpadding 40 ypadding 20
                vbox:
                    xalign 0.5
                    text "Доступно:" outlines [ (1, "#000000", 0, 0) ] size 35 xalign 0.5 yalign 0.1
                    
                    hbox:
                        spacing 10
                        xalign 0.5
                        
                        for item in available_items:
                            button:
                                xsize 150
                                ysize 50
                                background None
                                hover_background None
                                action [Function(AddToSet, selected_order, item), Function(RemoveFromSet, available_items, item)]
                                text str(item):
                                    xalign 0.5
                                    yalign 0.5
                                    outlines [ (1, "#000000", 0, 0) ] 
                                    size 26
                                    hover_color "#7e4525"
            
            null height 20
            
            vbox:
                spacing 20
                xalign 0.5
                
                button:
                    xsize 200
                    ysize 50
                    background None
                    hover_background None
                    text "Сбросить":
                        xalign 0.5
                        yalign 0.5
                        outlines [(1, "#000000", 0, 0)] 
                        size 35    
                        hover_color "#7e4525"
                    action [SetScreenVariable("selected_order", []), SetScreenVariable("available_items", list(items if items else []))]

                button:
                    xsize 200
                    ysize 50
                    background None
                    hover_background None
                    text "Подтвердить":
                        xalign 0.5
                        yalign 0.5
                        outlines [(1, "#000000", 0, 0)] 
                        size 35    
                        hover_color "#7e4525"
                    action Return(",".join(selected_order))

            text "\n{a=jump:leave_lvl}Отмена{/a}" outlines [ (2, "#000000", 0, 0) ] size 35 color "#c49227" xalign 0.5                

init python:
    def AddToSet(lst, item):
        if item not in lst:
            lst.append(item)
        return
    
    def RemoveFromSet(lst, item):
        if item in lst:
            lst.remove(item)
        return



# ========== SLIDER ==========
screen puzzle_slider(task_text="", min_val=0, max_val=100, hint=""):
    default current_value = (min_val + max_val) // 2
    
    frame:
        xalign 0.5 yalign 0.5
        xpadding 100 ypadding 90
        background Frame("gui/frame.png", 10, 10)
        
        vbox:
            spacing 20
            xalign 0.5
            
            text task_text:
                size 35
                xalign 0.5
                outlines [(1, "#000", 0, 0)]
            
            # if hint:
            #     text hint:
            #         size 26
            #         color "#aaa"
            #         xalign 0.5
            #         italic True
            
            null height 20
            
            frame:
                xalign 0.5
                background None
                xpadding 30 ypadding 20
                
                vbox:
                    spacing 15
                    text "Выберите значение" outlines [(2, "#000", 0, 0)] size 50 xalign 0.5 
                    
                    hbox:
                        spacing 10
                        xalign 0.5
                        
                        # МИНУС
                        button:
                            xsize 80 ysize 80
                            background None
                            hover_background None
                            text "<<<":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value - 10 >= min_val, SetScreenVariable("current_value", current_value - 10))
                        
                        button:
                            xsize 70 ysize 70
                            background None
                            hover_background None
                            text "<<":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value - 5 >= min_val, SetScreenVariable("current_value", current_value - 5))
                            
                        button:
                            xsize 40 ysize 50
                            background None
                            hover_background None
                            text "<":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value - 1 >= min_val, SetScreenVariable("current_value", current_value - 1))
                        
                        # Текущее значение
                        text "[current_value]":
                            size 64
                            xalign 0.5
                            yalign 0.5
                            outlines [(2, "#000", 0, 0)]
                            color "#7e4525"
                            xminimum 150
                            text_align 0.5
                        
                        # ПЛЮС
                        button:
                            xsize 40 ysize 50
                            background None
                            hover_background None
                            text ">":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value + 1 <= max_val, SetScreenVariable("current_value", current_value + 1))
                        
                        button:
                            xsize 70 ysize 70
                            background None
                            hover_background None
                            text ">>":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value + 5 <= max_val, SetScreenVariable("current_value", current_value + 5))
                            
                        button:
                            xsize 80 ysize 80
                            background None
                            hover_background None
                            text ">>>":
                                xalign 0.5
                                size 35
                                outlines [(2, "#000", 0, 0)]
                                hover_color "#7e4525"
                            action If(current_value <= max_val and current_value >= min_val and current_value + 10 <= max_val, SetScreenVariable("current_value", current_value + 10))
                    
                    fixed:
                        xalign 0.5
                        xsize 400
                        ysize 30
                        bar:
                            xsize 400
                            ysize 20
                            yalign 0.5
                            value current_value
                            range max_val - min_val
                            left_bar "#3c1f14"
                            right_bar "#7e4525"
                        
                        # Маркер
                        if max_val != min_val:
                            $ percent = (current_value - min_val) / (max_val - min_val)
                            $ marker_x = percent * 400
                            text "▼":
                                xpos marker_x - 10
                                ypos 20
                                size 20
                                color "#000"
            
            null height 20
            
            vbox:
                spacing 20
                xalign 0.5
                
                button:
                    xalign 0.5
                    xsize 180 ysize 50
                    background None
                    hover_background None
                    text "Подтвердить":
                        xalign 0.5 
                        size 35
                        outlines [(1, "#000", 0, 0)]
                        hover_color "#7e4525"
                    action Return(str(current_value))

                button:
                    xalign 0.5
                    xsize 180 ysize 50
                    background None
                    hover_background None
                    text "Сбросить":
                        xalign 0.5
                        size 35
                        outlines [(1, "#000", 0, 0)]
                        hover_color "#7e4525"
                    action SetScreenVariable("current_value", (min_val + max_val) // 2)
            
                text "\n{a=jump:leave_lvl}Отмена{/a}" outlines [ (2, "#000000", 0, 0) ] size 35 color "#c49227" xalign 0.5
                
                