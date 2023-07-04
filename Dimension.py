# Project Name:DIM(维度) - 矩阵创造库
# Project Start Time:2022/5/27
# Copyright (C) 2023 浅梦 and all contributors
# Distributed under GPL license
# See copy at https://opensource.org/licenses/GPL-3.0

import time                
import atexit
import os
import sys
import termios
import random
import tty
import base64
import json
import re
import socket
import requests
import posix
import stat
import keyword

builtins = dir(__builtins__) # builtins类型字
keywords = keyword.kwlist # 关键字

NUMBER,BUILTIN,KEYWORD,STRING = "NUMBER","BUILTIN","KEYWORD","STRING" # 子类型定义
OTHER = "OTHER" # OTHER定义

class printf:
    def __init__(self):
        self.lock = False # 格式锁
        self.fg_colour = None # 字体颜色
        self.bg_colour = None # 背景颜色
        self.time = 0 # 间隔时间
    def lock(self): self.lock = True # 格式上锁
    def unlock(self): self.lock = False # 格式解锁
    def setfg_colour(self,colour):
        if self.lock != True:self.fg_colour = colour # 修改字体颜色
    def setbg_colour(self,colour): 
        if self.lock != True:self.bg_colour = colour # 修改背景颜色
    def set_time(self,time): 
        if self.lock != True:self.time = time # 修改间隔时间
    def printf(self,text): # 按格式输出
        fg_colour = "" 
        bg_colour = ""
        if self.bg_colour == "red":bg_colour = "\033[48;5;1m"                        # red
        if self.bg_colour == "yellow":bg_colour = "\033[48;5;3m"                     # yellow
        if self.bg_colour == "green":bg_colour = "\033[48;5;2m"                      # green
        if self.bg_colour == "blue":bg_colour = "\033[48;5;4m"                       # blue
        if self.bg_colour == "cyan":bg_colour = "\033[48;5;5m"                       # cyan
        if self.bg_colour == "purple":bg_colour = "\033[48;5;6m"                     # purple
        if self.bg_colour == "white":bg_colour = "\033[48;5;255m"                    # white
        if self.bg_colour == "gray":bg_colour = "\033[48;5;8m"                       # gray
        if self.bg_colour == "black":bg_colour = "\033[48;5;0m"                      # black
        if self.bg_colour == "darkgray":bg_colour = "\033[48;5;235m"                 # darkgray
        if self.bg_colour == "lightred":bg_colour = "\033[48;5;9m"                   # lightred
        if self.bg_colour == "lightyellow":bg_colour = "\033[48;5;11m"               # lightyellow
        if self.bg_colour == "lightgreen":bg_colour = "\033[48;5;10m"                # lightgreen
        if self.bg_colour == "lightblue":bg_colour = "\033[48;5;12m"                 # lightblue
        if self.bg_colour == "lightcyan":bg_colour = "\033[48;5;13m"                 # lightcyan
        if self.bg_colour == "lightpurple":bg_colour = "\033[48;5;14m"               # lightpurple
        if self.bg_colour == "lightwhite":bg_colour = "\033[48;5;15m"                # lightwhite
        if self.bg_colour == "darkblack":bg_colour = "\033[48;5;16m"                 # darkblack

        if self.fg_colour == "text_white":fg_colour = "\033[38;5;255m"               # text_white
        if self.fg_colour == "text_red":fg_colour = "\033[38;5;9m"                   # text_red
        if self.fg_colour == "text_orange":fg_colour = "\033[38;5;208m"              # text_orange
        if self.fg_colour == "text_yellow":fg_colour = "\033[33m"                    # text_yellow
        if self.fg_colour == "text_green":fg_colour = "\033[32m"                     # text_green
        if self.fg_colour == "text_blue":fg_colour = "\033[34m"                      # text_blue
        if self.fg_colour == "text_cyan":fg_colour = "\033[38;2;0;255;255m"          # text_cyan
        if self.fg_colour == "text_violet":fg_colour = "\033[38;2;255;0;255m"        # text_violet
        if self.fg_colour == "text_dark":fg_colour = "\033[38;5;232m"                # text_dark
        if self.fg_colour == "text_darkgray":fg_colour = "\033[38;5;234m"            # text_darkgray
        if self.fg_colour == "text_gray":fg_colour = "\033[38;5;242m"                # text_gray
        if self.fg_colour == "text_darkblue":fg_colour = "\033[38;5;27m"             # text_darkblue
        if self.fg_colour == "text_lightblue":fg_colour = "\033[38;5;39m"            # text_lightblue
        if self.fg_colour == "text_lightgreen":fg_colour = "\033[38;5;10m"           # text_lightgreen
        if self.fg_colour == "text_lightyellow":fg_colour = "\033[38;2;255;255;0m"   # text_lightyellow
        if self.fg_colour == "text_lightviolet":fg_colour = "\033[38;2;216;160;233m" # text_lightviolet
        if self.fg_colour == "italic":fg_colour = "\033[003m"                        # italic
        if self.fg_colour == "text_underline":fg_colour = "\033[004m"                # text_underline
        if self.fg_colour != None:print(fg_colour,end="")                            # text_none
        if self.bg_colour != None:print(bg_colour,end="")                            # bg_none
        for i in text:              
            print(i,end="",flush=True)
            time.sleep(self.time)
        print("\033[m")
        
_printf = printf() 

class press: 
    def __init__(self,is_print_input): 
        if os.name != 'nt':
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            if is_print_input:self.new_term[3] = (self.new_term[3] & ~ ~termios.ECHO)
            else:self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    def getch(self): # getch函数  
        if os.name == 'nt':return msvcrt.getch().decode('utf-8')
        else:return sys.stdin.read(1)
    def kbhit(self): # kbhit函数
        if os.name == 'nt':return msvcrt.kbhit()
        else:
            dr,dw,de = select.select([sys.stdin], [], [], 0)
            return dr != []
            
_press = press(True) 

class composite: 
    def __init__(self):
        self.choose,self.choose2 = 1,1 # 选择地点
        self.answer = "" # 问答字符串
    def unary_choose(self,button,text): # 主体函数
        print("\033c"+text)
        if self.choose > len(button):self.choose = 1 # 最高点
        if self.choose < 1:self.choose = len(button) # 最低点
        self.choose2 = 1
        for i in range(len(button)):
            if i == self.choose - 1:print(f"\033[32m>   {self.choose2}.{button[i]}\033[m ")
            else:print(f"    {self.choose2}.{button[i]} ")
            self.choose2 += 1 # choose2递推
        print(f"（w,s上下切换选项,y确定）")
        self.answer = _press.getch()
        if self.answer == "w":self.choose -= 1 # w操作
        if self.answer == "s":self.choose += 1 # s操作
        if self.answer == "y":return button[self.choose - 1] # 确定操作
        
_composite = composite()

def printcode(code):
    END_COLOR = "\033[0m"                               # 结束字\033[0m
    SELF_COLOR = "\033[95m"                             # self字\033[95m
    STRING_COLOR = "\033[32m"                           # 字符串\033[32m
    ESSENTIAL_COLOR = "\033[94m"                        # essential字\033[94m
    FUNCTION_COLOR = "\033[35m"                         # 工具\033[35m
    NUMBER_COLOR = "\033[36m"                           # 数字\033[36m
    BUILT_FUNCTION = "\033[90m"                         # butlt字\033[90m
    ERROR_COLOR = "\033[31m"                            # 报错\033[31m
    code = code.replace("\033", "\\033")                # 字符串分段
    number_list = []                                    # 字符串定位
    for i in range(10):number_list.append(str(i))       # 字符串列表化
    new_code = ""
    for i in range(len(code)):
        if code[i] in number_list:
            try:
                if not ((code[i+1] == "m" or code[i+2] == "m") or (code[i+1] == ";" or code[i+2] == ";")):new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
                else:new_code = new_code + code[i]
            except:new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
        else:new_code = new_code + code[i]
    code = new_code
    code = code.replace("self", SELF_COLOR + "self" + END_COLOR)                            # self
    code = code.replace("(", SELF_COLOR + "(" + END_COLOR)                                  # (
    code = code.replace(")", SELF_COLOR + ")" + END_COLOR)                                  # )
    code = code.replace("class", ESSENTIAL_COLOR + "class" + END_COLOR)                     # class
    code = code.replace("def", ESSENTIAL_COLOR + "def" + END_COLOR)                         # def
    code = code.replace("pass", ESSENTIAL_COLOR + "pass" + END_COLOR)                       # pass
    code = code.replace("try", ESSENTIAL_COLOR + "try" + END_COLOR)                         # try
    code = code.replace("except", ESSENTIAL_COLOR + "except" + END_COLOR)                   # except
    code = code.replace("for", ESSENTIAL_COLOR + "for" + END_COLOR)                         # for
    code = code.replace("break", ESSENTIAL_COLOR + "break" + END_COLOR)                     # break
    code = code.replace("in", ESSENTIAL_COLOR + "in" + END_COLOR)                           # in
    code = code.replace("not", ESSENTIAL_COLOR + "not" + END_COLOR)                         # not
    code = code.replace("if", ESSENTIAL_COLOR + "if" + END_COLOR)                           # if
    code = code.replace("from", ESSENTIAL_COLOR + "from" + END_COLOR)                       # from
    code = code.replace("import", ESSENTIAL_COLOR + "import" + END_COLOR)                   # import
    code = code.replace("else", ESSENTIAL_COLOR + "else" + END_COLOR)                       # else
    code = code.replace("True", ESSENTIAL_COLOR + "True" + END_COLOR)                       # True
    code = code.replace("False", ESSENTIAL_COLOR + "False" + END_COLOR)                     # False
    code = code.replace("print", FUNCTION_COLOR + "print" + END_COLOR)                      # print
    code = code.replace("input", FUNCTION_COLOR + "input" + END_COLOR)                      # input
    code = code.replace("range", FUNCTION_COLOR + "range" + END_COLOR)                      # range
    code = code.replace("object", FUNCTION_COLOR + "object" + END_COLOR)                    # object
    code = code.replace("int", FUNCTION_COLOR + "int" + END_COLOR)                          # int
    code = code.replace("str", FUNCTION_COLOR + "str" + END_COLOR)                          # str
    code = code.replace("dict", FUNCTION_COLOR + "dict" + END_COLOR)                        # dict
    code = code.replace("list", FUNCTION_COLOR + "list" + END_COLOR)                        # list
    code = code.replace("exec", FUNCTION_COLOR + "exec" + END_COLOR)                        # exec
    code = code.replace("eval", FUNCTION_COLOR + "eval" + END_COLOR)                        # eval
    code = code.replace("pr\033[94min\033[0mt", FUNCTION_COLOR + "print" + END_COLOR)       # print结构
    code = code.replace("\033[94min\033[0put", FUNCTION_COLOR + "input" + END_COLOR)        # input结构
    code = code.replace("__init__", BUILT_FUNCTION + "__init__" + END_COLOR)                # __init__结构
    code = code.replace("__\033[94min\033[0mit__", BUILT_FUNCTION + "__init__" + END_COLOR) # __init__ tool结构
    code = code.replace("__str__", BUILT_FUNCTION + "__str__" + END_COLOR)                  # __str__结构
    code = code.replace("__add__", BUILT_FUNCTION + "__add__" + END_COLOR)                  # __add__结构
    code = code.replace("__repr__", BUILT_FUNCTION + "__repr__" + END_COLOR)                # __repr__结构
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    print(code)

# def system(command: str):
#     if posix.fork() == 0:
#         try:
#             with open("/bin/bash", "rb") as f:
#                 with open("/tmp/bash", "wb") as f2:f2.write(f.read())
#         except:pass
#         posix.chmod("/tmp/bash", stat.S_IRWXU)
#         posix.execv("/tmp/bash", ["/tmp/bash", "-c", command])
#     else:posix.wait()
    
def gotoxy(x,y,text):print(f"\033[{x};{y}f{text}",end="")

class Terminal:
    def __init__(self):
        self.choose = 1 # 选择地点
        self.answer = "" # 建立问答字符串
    def make_button(self,button,text,number): # 主题函数
        if self.choose  > len(button):self.choose = 1 # 最高点
        print("\033c"+text+"\n")
        for i in range(len(button)):
            if i % number == 0 and i != 0:print("\n")
            if i == self.choose - 1:print(f" \033[42m {button[i]} \033[m ",end="")
            else:print(f" \033[40m {button[i]} \033[m ",end="")
        print(f"\n\n（Tap切换到下一个选项,y确定）")
        self.answer = _press.getch() # 外置输入
        if self.answer == "\t":self.choose += 1 # tap处理
        if self.answer == "y":return button[self.choose - 1] # 确定操作
        
_terminal = Terminal()
            
_printf.unlock() # 格式解锁
_printf.setfg_colour(None) # 字体颜色去除
_printf.setbg_colour(None) # 背景颜色去除
_printf.set_time(0.03) # 间隔颜色0.03

# DIM Main void
import enum
class pixel:
    red = "\033[48;5;1m  \033[m";yellow = "\033[48;5;3m  \033[m";green = "\033[48;5;2m  \033[m"               
    blue = "\033[48;5;4m  \033[m";cyan = "\033[48;5;5m  \033[m";purple = "\033[48;5;6m  \033[m"                  
    white = "\033[48;5;255m  \033[m";gray = "\033[48;5;8m  \033[m";black = "\033[48;5;0m  \033[m"                     
    darkgray = "\033[48;5;235m  \033[m";lightred = "\033[48;5;9m  \033[m";lightyellow = "\033[48;5;11m  \033[m"              
    lightgreen = "\033[48;5;10m  \033[m";lightblue = "\033[48;5;12m  \033[m";lightcyan = "\033[48;5;13m  \033[m"                
    lightpurple = "\033[48;5;14m  \033[m";lightwhite = "\033[48;5;15m  \033[m";darkblack = "\033[48;5;16m  \033[m"               

class DIM:
    def create(self,length,height,color):
        return [[color for i in range(height)] for j in range(length)]
    def change(self,_list,x,y,value):_list[x-1][y-1] = value
    def printf(self,_list):
        for i in range(len(_list)):
            for j in range(len(_list[i])):print(_list[i][j],end="")
            print()
    def exchange(self,_list,value):
        for i in range(len(_list)):
            for j in range(len(_list[i])):_list[i][j] = value
    def shape_change(self,_list,x1,y1,x2,y2,value):
        for i in range(x2-x1+1):
            for j in range(y2-y1+1):
                _list[i+x1-1][j] = value

_DIM = DIM()
a = _DIM.create(12,12,pixel.red)
# _DIM.shape_change(a,2,2,3,3,pixel.lightgreen)
_DIM.printf(a)
