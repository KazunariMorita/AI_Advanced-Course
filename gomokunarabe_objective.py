# -*- coding: utf-8 -*-
import os
import numpy as np
import random
import glob
import sys
#2018/06/19
#made by Kazunari Morita


class Gomokunarabe:

    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.Blank = 0
        self.White = 1
        self.Black = 2
        self.screen_n_rows = 15
        self.screen_n_cols = 15
        self.enable_actions = np.arange(self.screen_n_cols*self.screen_n_rows)
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

    def reset(self):
        """ 盤面の初期化 """
        # reset ball position
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

    #勝った方のラベル返す(いたら)
    def winner(self):
        #横の判定  
        for i in range(15):
            p_judge=0
            e_judge=0        
            for j in range(15):
                if self.screen[i][j]==1:
                    p_judge+=1
                    e_judge=0
                if self.screen[i][j]==2:
                    e_judge+=1
                    p_judge=0
                if self.screen[i][j]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0
                if p_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    print ('\n\n')
                    print ('You Win a')
                    print ('\n\n')
                    return 1
                
                if e_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    
                    print('\n\n')
                    print('You Lose a')
                    print('\n\n')
                    return 2


        #縦の判定
        for i in range(15):
            p_judge=0
            e_judge=0
            for j in range(15):
                if self.screen[j][i]==1:
                    p_judge+=1
                    e_judge=0
                if self.screen[j][i]==2:
                    e_judge+=1
                    p_judge=0
                if self.screen[j][i]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0
        
                if p_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    
                    print ('\n\n')                    
                    print ('You Win b')
                    print ('\n\n')
                    return 1
                
                if e_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    print ('\n\n')
                    print ('You Lose b')
                    print ('\n\n')
                    return 2

        #斜め(右下)の判定
        for i in range(11):
            for j in range(11):
                p_judge=0
                e_judge=0
                for k in range(5):
                    if self.screen[i+k][j+k]==1:
                        p_judge+=1
                        e_judge=0
                    if self.screen[i+k][j+k]==2:
                        e_judge+=1
                        p_judge=0

                    if self.screen[i+k][j+k]==0:
                        #もし, 連続していなかったら0
                        p_judge=0
                        e_judge=0

                    if p_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Win c')
                        print ('\n\n')
                        return 1
                    
                    if e_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('\n\n')                        
                        print ('You Lose c')
                        print ('\n\n')
                        return 2

        #斜め(左下)の判定    
        for i in range(11):
            for j in range(4,15):
                p_judge=0
                e_judge=0
                for k in range(5):
                    if self.screen[i+k][j-k]==1:
                        p_judge+=1
                        e_judge=0
                    if self.screen[i+k][j-k]==2:
                        e_judge+=1
                        p_judge=0
                    if self.screen[i+k][j-k]==0:
                        #もし, 連続していなかったら0
                        p_judge=0
                        e_judge=0

                    if p_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Win d')
                        print ('\n\n')
                        return 1
                    
                    if e_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Lose d')
                        print ('\n\n')
                        return 2

        #引き分け判定
        if 0 not in self.screen:
            #盤面の描画
            # self.display_screen()
                    
            print ('Draw')
            print ('\n\n')
            return 0

        return False



        

    def get_cells(self, i):
        r = int(i / self.screen_n_cols)
        c = int(i - ( r * self.screen_n_cols))
        return self.screen[r][c]  


    def get_enables(self,color):
        result = []
        #おける座標のリストを返す
        for action in self.enable_actions:
            if self.get_cells(action) == 0:
                """ 空白の位置 """
                result.insert(0,action)

        return result



    def update(self, action, color):

        pos_y = int(action / self.screen_n_cols)
        pos_x = int(action-( pos_y * self.screen_n_cols))
        self.screen[pos_y][pos_x] = color


        # print(self.screen)
        n =  self.count_my_ball(color,action)
        return n


    def count_my_ball(self,color,action):
        pos_y = action//15    
        pos_x = action/15

        pos_y = int(action / self.screen_n_cols)
        pos_x = int(action-( pos_y * self.screen_n_cols))

   
        right_margin = pos_x-14
        left_margin = pos_x
        top_margin = pos_y
        under_margin = pos_y-14


        # print (min(right_margin,left_margin))
        # exit(-1)
        ball_num = [0]*6



        #右側
        if right_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y]==color:
                    ball_num[0]+=1
                else:
                    ball_num[0]-=1

        else:
            for i in range(right_margin):
                if self.screen[pos_x+i][pos_y]==color:
                    ball_num[0]+=1
                else:
                    ball_num[0]-=1                
        
        #下側
        if under_margin>5:
            for i in range(5):
                if self.screen[pos_x][pos_y+i]==color:
                    ball_num[1]+=1
                else:
                    ball_num[1]-=1    
        else:
            for i in range(under_margin):
                if self.screen[pos_x][pos_y+i]==color:
                    ball_num[1]+=1
                else:
                    ball_num[1]-=1       
        #左側
        if left_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y]==color:
                    ball_num[2]+=1
                else:
                    ball_num[2]-=1
        else:
            for i in range(left_margin):
                if self.screen[pos_x-i][pos_y]==color:
                    ball_num[2]+=1
                else:
                    ball_num[2]-=1        
        #上側
        if top_margin>5:
            for i in range(5):
                if self.screen[pos_x][pos_y-i]==color:
                    ball_num[3]+=1
                else:
                    ball_num[3]-=1
        else:
            for i in range(top_margin):
                if self.screen[pos_x][pos_y-i]==color:
                    ball_num[3]+=1
                else:
                    ball_num[3]-=1
        #右斜上側
        if right_margin>5 and top_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[4]+=1
                else:
                    ball_num[4]-=1
        else:
            for i in range(min(right_margin,top_margin)):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[4]+=1
                else:
                    ball_num[4]-=1    
        #左斜上側
        if left_margin>5 and top_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y-i]==color:
                    ball_num[5]+=1
                else:
                    ball_num[5]-=1
        else:
            for i in range(min(left_margin,top_margin)):
                if self.screen[pos_x-i][pos_y-i]==color:
                    ball_num[5]+=1
                else:
                    ball_num[5]-=1        
        #左斜下側
        if left_margin>5 and under_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y+i]==color:
                    ball_num[6]+=1
                else:
                    ball_num[6]-=1
        else:
            for i in range(min(left_margin,under_margin)):
                if self.screen[pos_x-i][pos_y+i]==color:
                    ball_num[6]+=1
                else:
                    ball_num[6]-=1        
        #右斜下側
        if right_margin>5 and under_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[7]+=1
                else:
                    ball_num[7]-=1
        else:
            for i in range(min(right_margin,under_margin)):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[7]+=1
                else:
                    ball_num[7]-=1


        # print (str(right_margin))
        # print (left_margin))
        # print (top_margin))
        # # print (under_margin))
        # print ('玉数:'+str(max(ball_num)))
        # print (str(color))
        # print (max(ball_num))
        return max(ball_num)
    







    def isEnd(self):
        # e1 = self.get_enables(self.White)
        # e2 = self.get_enables(self.Black)

        # self.winner()
            # return True

        # for action in self.enable_actions:
            # if self.get_cells(action) == self.Blank:
        # self.display_screen()
        return self.winner() 
        
        # return True    
        



    #プレイヤーのターン
    def player_turn(self):
        print ('Your Turn')
        
        p_x_pos = input('select ball x pos > ')
        p_y_pos = input('select ball y pos > ')
        while self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 1 or  self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 2 or int(p_x_pos)<1 or int(p_x_pos)>15 or  int(p_y_pos)<1 or int(p_y_pos)>15: 

            print ('please retry')
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')
        self.screen[int(p_y_pos)-1][int(p_x_pos)-1] = 1

    #敵のターン
    def enemy_turn(self):
        print ('Enemy Turn')
        
        #敵(ランダム)で配置
        e_x_pos = random.randint(0,14)
        e_y_pos = random.randint(0,14)
        
        #もし, プレイヤーの玉なければ配置, あれば乱数再生成
        while self.screen[e_y_pos][e_x_pos] == 1 or  self.screen[e_y_pos][e_x_pos] == 2:
        
            #乱数再生成
            e_x_pos = random.randint(0,14)
            e_y_pos = random.randint(0,14)

        self.screen[e_y_pos][e_x_pos] = 2  


    #盤面の表示
    def display_screen(self):
        for i in range(15):
            for j in range(15):
                # if i==0 and j==0:
                #     for k in range(1,16):
                #         print (str(k)+'　', end='')
                #     print ('\n',end='')

                if  self.screen[i][j]==0:
                    print (pycolor.WHITE+'+'+ pycolor.END, end='')

                elif self.screen[i][j]==1:
                    print (pycolor.RED+'●'+pycolor.END, end='')

                elif self.screen[i][j]==2:
                    print (pycolor.BLUE+'■'+pycolor.END, end='')

            print ('\n', end='')
            
        print ('[You]'+pycolor.RED+'●'+pycolor.END, '\t[Enemy]'+pycolor.BLUE+'■'+pycolor.END)
        print ('\n\n')


class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

#メイン文
if __name__ == '__main__':

    env = Gomokunarabe()

    end_flag = False
    # screen = np.zeros([15,15])
    while not end_flag:

        #盤面の描画
        env.display_screen()

        #プレイヤーのターン
        env.player_turn()

        #勝敗判定
        env.winner()

        #敵のターン
        env.enemy_turn()
