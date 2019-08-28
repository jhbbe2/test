#경로 그리기
import turtle
import random

t = turtle.Turtle()
t.shape("turtle")
color_list = ["yellow","green","blue","red"]    
choice = turtle.textinput("경로 종류","1.입력경로 2.랜덤경로 3.고정경로 : 번호 입력")

def inputPath():
    path = turtle.textinput("경로 입력","경로 입력(l:왼쪽, r:오른쪽, f:직진, b:후진) : ")
    for i in range(len(path)): 
        move = turtle.textinput(path,"경로 %s 의 %d 번째 입력:" %(path,i+1))

        if move != path[i]:
            t.penup()
            t.hideturtle()
            t.goto(t.xcor(),t.ycor()+200)
            t.pencolor("black")
            t.write("입 력 오 류 !",font=50)
            break

        if move == path[i]:
            if move == 'l':
                t.left(90)
                t.pencolor(color_list[0])
                t.forward(30)
            if move == 'r':
                t.right(90)
                t.pencolor(color_list[1])
                t.forward(30)
            if move == 'f':
                t.pencolor(color_list[2])
                t.forward(30)
            if move == 'b':
                t.pencolor(color_list[3])
                t.backward(30)

            if i == len(path)-1:
                t.penup()
                t.hideturtle()
                t.goto(-100,200)
                t.pencolor("black")
                t.write("- '%s' 경로 완료 -" %(path),font=50)


def randomPath(): 
    moveKey = ['l','r','f','b']
    final = ""
    length = int(turtle.textinput("경로 길이","경로길이의 범위를 입력하시오:"))
    path_len = random.randint(1,length)
    for i in range(path_len): 
        rpath = random.choice(moveKey)
        rmove = turtle.textinput("경로 이동","총 %d길이인 경로의 %d번째 값인 %s 로 이동하시오." %(path_len,i+1,rpath))
        final = final + rpath

        if rmove != rpath:
            t.penup()
            t.hideturtle()
            t.goto(t.xcor(),t.ycor()+200)
            t.pencolor("black")
            t.write("입 력 오 류 !",font=50)
            break

        if rmove == rpath:
            if rmove == 'l':
                t.left(90)
                t.pencolor(color_list[0])
                t.forward(30)
            if rmove == 'r':
                t.right(90)
                t.pencolor(color_list[1])
                t.forward(30)
            if rmove == 'f':
                t.pencolor(color_list[2])
                t.forward(30)
            if rmove == 'b':
                t.pencolor(color_list[3])
                t.backward(30)

            if i == path_len-1:
                t.penup()
                t.hideturtle()
                t.goto(-100,200)
                t.pencolor("black")
                t.write("- '%s' 경로 완료 -  " %(final),font=50)


def fixPath():
    fpath = "frfrrbl"
    for i in range(len(fpath)):
        fmove = turtle.textinput("경로 이동","경로 %s의 %d번째 값을 입력하시오."%(fpath,i+1))
        if fmove != fpath[i]:
            t.penup()
            t.hideturtle()
            t.goto(t.xcor(),t.ycor()+200)
            t.pencolor("black")
            t.write("입 력 오 류 !",font=50)
            break

        if fmove == fpath[i]:
            if fmove == 'l':
                t.left(90)
                t.pencolor(color_list[0])
                t.forward(30)
            if fmove == 'r':
                t.right(90)
                t.pencolor(color_list[1])
                t.forward(30)
            if fmove == 'f':
                t.pencolor(color_list[2])
                t.forward(30)
            if fmove == 'b':
                t.pencolor(color_list[3])
                t.backward(30)

            if i == len(fpath)-1:
                t.penup()
                t.hideturtle()
                t.goto(-100,200)
                t.pencolor("black")
                t.write("- '%s' 경로 완료 -  " %(fpath),font=50)


if choice == '1':
    inputPath()

if choice == '2':
    randomPath()

if choice == '3':
    fixPath()

    

