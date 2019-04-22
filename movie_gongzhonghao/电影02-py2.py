#*-*-coding:utf-8 -*-
import io
import werobot
robot = werobot.WeRoBot(token='ljmoistlin')

f = io.open("kaifa02.txt",'r',encoding='utf-8')
@robot.handler
def articles(message):
        z=[]
        f.seek(0)
        sum=0
        flag=0
        for list in f:
                a=str(list)
                if message.content in a:
                        a = a.split(',')
                        z.append(a)
                        sum = sum+1
                        if(sum>5):
                                flag=1
                                return z
        if(flag==0 and sum!=0):
                return z
        elif sum==0:
                return "非常抱歉，没有找到您要的资源，请确认输入的电影名是否正确!\n如：超时空同居"
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
f.close()