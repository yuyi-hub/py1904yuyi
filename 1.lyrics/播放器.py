
import os
import re
import pygame
from pygame.locals import *
import time

class Lyric:
    def __init__(self,second,word):
        self.second = second  # 时间，秒
        self.word = word    # 歌词
    def __str__(self):
        return self.word

    # 对象比较需要重写 < 方法
    def __lt__(self, other):
        return self.second < other.second


class LyricParser:
    def __init__(self,path):
        self.path = path  # 歌词文件路径
        self.lyrics = []   # 歌词列表，保存歌词对象
    # 加载文件
    def load(self):
        if os.path.exists(self.path):
            with open(self.path,encoding='utf-8') as fp:
                data = fp.readlines()
                # 去掉每一句后的换行符，和去掉换行符后的空行
                return [value.strip() for value in data if value.strip()]
        return False  # 如果返回False 文件不存在

    def parse(self):
        data = self.load()
        if data:  # 数据存在
            for i in range(len(data)-1,-1,-1):
                if len([value for value in data[i].split(']') if value]) < 2:
                    data.pop(i)
                else:
                    data[i] = data[i].replace("[",'')
            # 解析
            for line in data:
                line = line.split(']')  # 列表
                for item in line[:-1]:
                    #'00:03.50'
                    # 把时间字符串分割成列表，并把列表元素转换为浮点数
                    second = [float(value) for value in re.split(r':|\.',item)]
                    second = second[0]*60 + second[1]+second[2]/100  # 计算时间对应的秒数
                    obj = Lyric(second,line[-1])  # 生成歌词对象, line[-1]是歌词
                    self.lyrics.append(obj)  # 添加到歌词列表
            # 排序
            self.lyrics.sort()
lp = LyricParser("chuanqi.txt")
lp.parse()
list1 = []
for obj in lp.lyrics:
    list1.append([obj.second,obj.word])


class Button():

    def __init__(self, screen, add, name, place):
        self.screen = screen
        self.add = add  # 路径
        self.name = name  # 按钮功能
        self.place = place  # 按钮绘制位置
        self.mybt = pygame.image.load(r'' + self.add)  # 图片地址
        self.rect = self.mybt.get_rect()  # 获取图案矩形
        self.angle = 1  # 图像旋转角度

    def show_button(self):
        #显示按钮
        self.screen.blit(self.mybt, self.place)

    def ro_img(self):  # 旋转图像
        newimg = pygame.transform.rotozoom(self.mybt, self.angle, 1.0)
        newrect = newimg.get_rect(center=(210, 180))  # 固定图像中心
        self.screen.blit(newimg, newrect)
        self.angle += 1



class Text:
    def __init__(self,screen,word):
        self.text = pygame.font.SysFont('SimHei', 30)
        self.word = word
        self.screen = screen
        self.place = (0,200)
        self.my_ly = self.text.render(self.word, True, (100, 100, 200))

    # 歌词滚屏
    # def get_place(self):
    #     x = 0
    #     y = (600 - self.my_ly.get_height()) / 2
    #     while True:
    #      x -= 0.05
    #     if x < -self.my_ly.get_width():
    #         x = 420 - self.my_ly.get_width()
    #     self.place = (x,y)

    def word_show(self):  #显示歌词
        self.screen.blit(self.my_ly, self.place)

    def word_mv(self):
        pygame.Surface.scroll(self.my_ly,dx=0,dy=0)



def main():
    pygame.init()
    screen = pygame.display.set_mode((420,600))

    screen.fill((0,0,0))
    pygame.display.set_caption("传奇-王菲")
    #添加背景图
    background = pygame.image.load(r'bj.jpg').convert_alpha()
    screen.blit(background, (0, 0))
    pygame.time.Clock().tick(50)
    play_bt = Button(screen=screen, add=r"播放.jpg",name='play_music',place=[185, 475])
    next_bt = Button(screen=screen, add=r"向右.png", name="next_music", place=[310, 475])
    previous_bt = Button(screen=screen, add=r"向左.jpg", name="previous_music", place=[60, 475])
    pause_bt = Button(screen=screen, add=r'暂停.jpg', name="pause_music", place=[185, 475])
    show_bt = Button(screen=screen, add=r"show.png",name='show_picture', place=[150, 300])
    previous_bt.show_button()
    next_bt.show_button()

    #加载音乐
    pygame.mixer.music.load("王菲.wav")
    start_time = time.time()
    pygame.mixer.music.play(-1)  # 重复播放
    running = True  # 运行标志
    pause = False  # 暂停标志
    while running:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if pause == False:
                        pygame.mixer.music.pause()  # 暂停播放

                    else:
                        pygame.mixer.music.unpause() # 回复播放
                    pause = not pause



        time_music = pygame.mixer.music.get_pos()   #歌曲当前进度
        # time.sleep(10)



        if pause:
            play_bt.show_button()# 暂停时候显示播放键


        else:
            pause_bt.show_button()#播放时候显示暂停键
            show_bt.ro_img()  #播放时，圆图进行旋转
            for i in range(len(list1)):
                if list1[i][0] < float('%.2f' % (time_music / 1000)) < list1[i + 1][0]:
                    text = Text(screen=screen, word=str(list1[i][1]))
                    text.word_show()
                    if float('%.2f' % (time_music / 1000)) == list1[i+1][0]:
                        text.word_mv()







        pygame.display.flip()


if __name__ == '__main__':
    main()