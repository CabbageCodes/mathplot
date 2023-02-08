import pygame
from mathfunc import *

mainenv = PlotEnv([1800,1200],[0,0,0])
mainenv.set_plot_limits([-8,8],[-4,5])
mainenv.axescolor = [150,150,150]

color_blue = [103,167,214]


MyFunc1 = MathFunc("cos(x)",0)
MyFunc1.setderivlist(["cos(x)","-sin(x)","-cos(x)","sin(x)","cos(x)"])
MyFunc1.snaps = [0,pi/2,pi,2*pi,3*pi/2,5*pi/2,-pi/2,-3*pi/2,-5*pi/2,-pi,-2*pi]

# MyFunc1 = MathFunc("exp(x)")
# MyFunc1.evalmax = 4
# MyFunc1.setderivlist(["exp(x)","exp(x)","exp(x)","exp(x)","exp(x)","exp(x)"])

mainenv.add_func(MyFunc1)
MyFunc1.do_drawtext = 1
MyFunc1.drawtextmode = "up right"
MyFunc1.text = MyFunc1.formula

MyFunc1.add_button(Button("add taylor",[MyFunc1,mainenv],text = "Add Taylor polynomial"),mainenv)
MyFunc1.add_button(Button("change func",[MyFunc1,mainenv],text = "Change formula"),mainenv)

# MyFunc2 = MathFunc("x",0)
# MyFunc2.type = "non-static"

# MyTaylor1 = Taylor(MyFunc1,3,mainenv)
# mainenv.add_taylor(MyTaylor1)
# poly_deg = 3
###

# MyTaylor = Poly(GiveTaylorList(MyFunc1,0,poly_deg))
# MyFunc2.setfunc(MyTaylor.giveformula(),mainenv)
# MyFunc2.setgraphparam(color_green,1)
# MyFunc2.text = GiveTaylorText(MyFunc1,0,3)
# MyTaylor.linecolor = MyFunc2.color

adjust_coef_mode = 0
move_coef_slider = 0

# MyFunc2.do_drawtext = 1
# MyFunc2.drawtextmode = "up right"

# MySlider1 = GraphSlider(MyFunc1)
# mainenv.add_slider(MySlider1)

myrange = np.linspace(mainenv.plotlimitX[0],mainenv.plotlimitX[1],1000)
mainenv.setallpoints()

open_func_menu = 0
func_menu_choice = MyFunc1

move_plotrect_mode = 0

running = 1
move_slider_mode = 0
# chosen_slider = MySlider1

prev_time = Time.time()
FPS = 120


# text_found = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     MyFunc1.reset_graph(mainenv)
        if mainenv.typing_mode:
            if event.type == pygame.KEYDOWN:
                mainenv.redraw = 1
                if event.key == pygame.K_RETURN:
                    mainenv.typing_mode = 0
                    mainenv.text_target_func.setfunc(mainenv.add_text,mainenv)
                    for t in mainenv.text_target_func.taylor_targets:
                        t.update_point(t.center,mainenv)
                elif event.key == pygame.K_BACKSPACE:
                    mainenv.add_text = mainenv.add_text[:-1]
                elif event.unicode:
                    mainenv.add_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            found = 0
            for t in mainenv.taylors:
                if t.slider.isontop(mainenv,mpos):
                    chosen_slider = t.slider
                    move_slider_mode = 1
                    found = 1
                    break
            if not found:
                i = 0
                found_taylorpick = 0
                for tay1 in mainenv.taylors:
                    for box in tay1.taylorpoly.clickhitboxes:
                        if isInRect(mpos,box):
                            found = 1
                            if not adjust_coef_mode:
                                adjust_coef_mode = 1
                                adjust_coef_taylor_choice = tay1
                                tay1.coefslider.coef_pick = i
                                tay1.coefslider.Sval = tay1.taylorpoly.coefs[tay1.coefslider.coef_pick][0]
                                tay1.adjust_coefs = 1
                            elif tay1.coefslider.coef_pick != i:
                                tay1.coefslider.coef_pick = i
                                tay1.coefslider.Sval = tay1.taylorpoly.coefs[tay1.coefslider.coef_pick][0]
                            else:
                                adjust_coef_mode = 0
                                move_coef_slider = 0
                                mainenv.redraw = 1
                                tay1.adjust_coefs = 0
                            found_taylorpick = 1
                            break
                        i += 1
                    if found_taylorpick:
                        break
            if not found and adjust_coef_mode:
                box = [adjust_coef_taylor_choice.coefslider.screenpos[0],adjust_coef_taylor_choice.coefslider.screenpos[1],adjust_coef_taylor_choice.coefslider.width,adjust_coef_taylor_choice.coefslider.length]
                if isInRect(mpos,box):
                    found = 1
                    if isInRect(mpos,adjust_coef_taylor_choice.coefslider.Srect,[0,5]):
                        move_coef_slider = 1
            if not found:
                for func in mainenv.funcs:
                    if isInRect(mpos,func.hitbox):
                        open_func_menu = 1
                        func_menu_choice = func
                        found = 1
                        mainenv.redraw = 1
                        break
                for tay in mainenv.taylors:
                    if isInRect(mpos,tay.func.hitbox):
                        open_func_menu = 1
                        func_menu_choice = tay.func
                        found = 1
                        mainenv.redraw = 1
                        break
            if not found and open_func_menu:
                for b in func_menu_choice.fmenu.buttons:
                    if isInRect(mpos,b.rect):
                        mainenv.redraw = 1
                        open_func_menu = 0
                        found = 1
                        b.get_pressed()
                        break
            if not found:
                if adjust_coef_mode:
                    adjust_coef_mode = 0
                    adjust_coef_taylor_choice.adjust_coefs = 0
                move_coef_slider = 0
                mainenv.redraw = 1
                if open_func_menu:
                    open_func_menu = 0
                    func_menu_choice.fmenu.visible = 0

                if isInRect(mpos,mainenv.plotrect):
                    move_plotrect_mode = 1
                    start_pos = [mpos[0],mpos[1]]
                    old_lims = [mainenv.plotlimitX[0],mainenv.plotlimitX[1],mainenv.plotlimitY[0],mainenv.plotlimitY[1]]
        elif event.type == pygame.MOUSEBUTTONUP:
            if move_slider_mode == 1:
                move_slider_mode = 0
                chosen_slider.snap()

                for t in chosen_slider.func.taylor_targets:
                    t.update_point(chosen_slider.pos,mainenv)

                # MyTaylor1.taylorpoly.setparams(GiveTaylorList(MyFunc1,chosen_slider.pos,poly_deg))
                # MyTaylor1.func.setfunc(MyTaylor1.taylorpoly.giveformula(),mainenv)
                mainenv.redraw = 1
            if move_coef_slider:
                move_coef_slider = 0
                adjust_coef_taylor_choice.coefslider.snap()
                adjust_coef_taylor_choice.taylorpoly.coefs[adjust_coef_taylor_choice.coefslider.coef_pick][0] = adjust_coef_taylor_choice.coefslider.Sval
                adjust_coef_taylor_choice.func.setfunc(adjust_coef_taylor_choice.taylorpoly.giveformula(),mainenv)
                adjust_coef_taylor_choice.coefslider.set_Spos()
                mainenv.redraw = 1
            if move_plotrect_mode:
                move_plotrect_mode = 0
    if move_slider_mode:
        mpos = pygame.mouse.get_pos()
        wpos = mainenv.screen_to_point(mpos)
        chosen_slider.pos = wpos[0]
        # MyFunc2.text = GiveTaylorText(MyFunc1,wpos[0],3)

        for t in chosen_slider.func.taylor_targets:
            t.update_point(chosen_slider.pos,mainenv)

        # MyTaylor1.taylorpoly.setparams(GiveTaylorList(MyFunc1,chosen_slider.pos,poly_deg))
        # MyTaylor1.func.setfunc(MyTaylor1.taylorpoly.giveformula(),mainenv)
        mainenv.redraw = 1
    if adjust_coef_mode:
        adjust_coef_taylor_choice.coefslider.screenpos[0] = adjust_coef_taylor_choice.taylorpoly.clickhitboxes[adjust_coef_taylor_choice.coefslider.coef_pick][0]
        mainenv.redraw = 1
        if move_coef_slider:
            mpos = pygame.mouse.get_pos()
            adjust_coef_taylor_choice.coefslider.Sval = adjust_coef_taylor_choice.coefslider.screen_to_val(mpos)

            adjust_coef_taylor_choice.taylorpoly.coefs[adjust_coef_taylor_choice.coefslider.coef_pick][0] = adjust_coef_taylor_choice.coefslider.Sval
            adjust_coef_taylor_choice.func.setfunc(adjust_coef_taylor_choice.taylorpoly.giveformula(),mainenv)
        adjust_coef_taylor_choice.coefslider.set_Spos()
    if open_func_menu:
        func_menu_choice.fmenu.visible = 1
    else:
        func_menu_choice.fmenu.visible = 0
    if move_plotrect_mode:
        mpos = pygame.mouse.get_pos()
        mainenv.translate_pos(mpos,start_pos,old_lims)
        mainenv.redraw = 1
    if mainenv.redraw:
        mainenv.redraw = 0
        mainenv.drawme()
        # if adjust_coef_mode:
        #     MyTaylor1.coefslider.draw(mainenv)
        pygame.display.flip()
    curr_time = Time.time()
    diff = curr_time - prev_time
    delay = max(1.0 / FPS - diff,0)
    Time.sleep(delay)

pygame.quit()