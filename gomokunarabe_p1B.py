#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:07:17 2018

@author: yamaguchi
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import numpy as np
import random

import argparse
#from gomokunarabe_p1B import Gomokunarabe
from dqn_agent import DQNAgent


def getNearestValue(lis, num):
    """
    概要: リストからある値に最も近い値のインデックスを返却する
    """
    idx = np.abs(np.asarray(lis) - num).argmin()
   
    return idx


class Gomokunarabe:

    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.Blank = 0
        self.White = -1
        self.Black = 1
        
        self.screen_n_rows = 15
        self.screen_n_cols = 15
        self.enable_actions = np.arange(self.screen_n_cols*self.screen_n_rows)
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols), dtype=np.int8)
        self.last_x_pos = 0
        self.last_y_pos = 0
        self.win_flag = 0
        
        
        self.img=np.zeros((self.screen_n_rows*30, self.screen_n_cols*30,3), dtype=np.uint8)
        self.mode=self.Black
        
        
    def reset(self):
        """ 盤面の初期化 """
        # reset ball position
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

    #勝った方のラベル返す(いたら)
    def winner(self):
        #横と縦と斜め右下と斜め左下の判定
        for i in range(5):
            width = np.sum(self.screen[self.last_y_pos, self.last_x_pos-4+i:self.last_x_pos+1+i])
            height = np.sum(self.screen[self.last_y_pos-4+i:self.last_y_pos+1+i, self.last_x_pos])
            right_diagonal = np.sum(np.diag(self.screen[self.last_y_pos-4+i:self.last_y_pos+1+i, self.last_x_pos-4+i:self.last_x_pos+1+i]))
            left_diagonal = np.sum(np.diag(self.screen[self.last_y_pos-i:self.last_y_pos+5-i, self.last_x_pos-4+i:self.last_x_pos+1+i][:, ::-1]))       
            #if (width == 5) or (height == 5) or (right_diagonal == 5) or (left_diagonal == 5):
            if (width >= 5) or (height >= 5) or (right_diagonal >= 5) or (left_diagonal >= 5):
                #print ('\n\n')
                #print ('You Win')
                #print ('\n\n')
                cv2.putText(self.img, 'YOU WIN', (50, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255),4,lineType=cv2.LINE_AA) 
                
                return self.Black   
            if (width == -5) or (height == -5) or (right_diagonal == -5) or (left_diagonal == -5):
                #print ('\n\n')
                #print ('You Lose')
                #print ('\n\n') 
                cv2.putText(self.img, 'YOU LOSE', (50, 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0),4,lineType=cv2.LINE_AA)
                
                #self.win_flag = self.Black
                return self. White       
        #引き分け判定
        if 0 not in self.screen:
            #盤面の描画
            # self.display_screen()
                    
            #print ('Draw')
            #print ('\n\n')
            cv2.putText(env.img, 'DRAW', (50, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0),4,lineType=cv2.LINE_AA)

            return 2

        
        return False



        

    def get_cells(self, i):
        r = int(i / self.screen_n_cols)
        c = int(i - ( r * self.screen_n_cols))
        return self.screen[r][c]  


    def get_enables(self):
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
        #
        self.last_x_pos = pos_x
        self.last_y_pos = pos_y

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
        if self.win_flag == self.White or self.win_flag == self.Black or self.win_flag == 2:
            return True    
        else:
            return False



     
        
        
    def player_turn(self,event,x,y,flags,param):      
        #クリックした位置にコマを配置
        #while(1):
        if event == cv2.EVENT_LBUTTONDOWN:    
            x=getNearestValue(rows_line, x)
            y=getNearestValue(cols_line, y)

        
                
            if self.screen[y][x]==0:
                self.screen[y][x]=self.Black
                self.last_x_pos=int(x)
                self.last_y_pos=int(y)
                print('player x:'+str(self.last_x_pos))
                print('player y:'+str(self.last_y_pos))
                

                cv2.circle(self.img,(self.last_x_pos*30+15,self.last_y_pos*30+15), 13, (0,0,0), -1)
                self.win_flag = self.winner()
                if self.win_flag==0:
                    self.mode = self.White 
                else:
                    self.mode = 0
                    
                
                
            else:
                cv2.setMouseCallback('img',self.player_turn)
                


    def enemy_turn(self):
        #ランダムにコマを配置       
    
        ###############エネミーが置く場所決定
        """
        
        e_x_pos=int(random.randrange(self.screen_n_rows))
        e_y_pos=int(random.randrange(self.screen_n_cols))
            
        
        
        
        while self.screen[e_y_pos][e_x_pos] == self.White or self.screen[e_y_pos][e_x_pos] == self.Black:
        
            #乱数再生成
            e_x_pos=int(random.randrange(self.screen_n_rows))
            e_y_pos=int(random.randrange(self.screen_n_cols))
            
        """
        



        # parser = argparse.ArgumentParser()
        # parser.add_argument("-m", "--model_path")
        # parser.add_argument("-s", "--save", dest="save", action="store_true")
        # parser.set_defaults(save=False) 
        # args = parser.parse_args()
        enables = self.get_enables()        
        qvalue, action_t = agent.select_enable_action(self.screen, enables)
        print('>>>  {:}'.format(action_t))              
        env.update(action_t, self.White)
        
        e_y_pos = int(action_t / env.screen_n_cols)
        e_x_pos = int(action_t-( e_y_pos * env.screen_n_cols))  
        
            
        ##################
        
        self.last_x_pos=e_x_pos
        self.last_y_pos=e_y_pos
        
        print("enemy x:" + str(self.last_x_pos))
        print("enemy y:" + str(self.last_y_pos))
        self.screen[self.last_y_pos][self.last_x_pos]=self.White
        cv2.circle(self.img,(self.last_x_pos*30+15,self.last_y_pos*30+15), 13, (255,255,255), -1)

         
        self.win_flag = self.winner()

        
        if self.win_flag==0:
            self.mode = self.Black
        else:
            self.mode = 0
            
    def display_screen(self):
        cv2.imshow('img',self.img)
        
   

        
if __name__ == '__main__':
   
    #AI読み込み
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-s", "--save", dest="save", action="store_true")
    parser.set_defaults(save=False) 
    args = parser.parse_args()

    env = Gomokunarabe()
    agent = DQNAgent(env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols)
    #agent.load_model(args.model_path)
    agent.load_model("models/gomokunarabe_objective.ckpt")

    rows_line= [i*30+15 for i in range(env.screen_n_rows)]
    cols_line= [i*30+15 for i in range(env.screen_n_cols)]
    

    for i in range(len(env.img)):
        for j in range(len(env.img[0])):
            if i in rows_line or j in cols_line:
                env.img[i][j][0]=0
                env.img[i][j][1]=0
                env.img[i][j][2]=0
            else:
                env.img[i][j][0]=155
                env.img[i][j][1]=200
                env.img[i][j][2]=245


    print('a')
    cv2.startWindowThread()
    
    print('b')

    while(1):
        
        #cv2.imshow('img',env.img)
        env.display_screen()
     
        if env.mode==env.Black:
            print("player turn")
            cv2.setMouseCallback('img',env.player_turn)
        
             
        elif env.mode==env.White:
            print("enemy turn")
            env.enemy_turn()          

        elif env.mode==0:
            env.mode=0
            env.display_screen()
            break
        print("loop")
        key = cv2.waitKey(100)  
        # qが押された場合は終了する
        if key == ord('q'):
            break

    print('c')
   
    while(1):
        key = cv2.waitKey(1)  
        # qが押された場合は終了する
        if key == ord('q'):
            break
  
    cv2.waitKey(1)
    cv2.destroyAllWindows()  
    cv2.waitKey(1)

    print('d')


    print(env.screen)