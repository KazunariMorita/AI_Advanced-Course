# -*- coding: utf-8 -*-
import numpy as np
import random
import glob
import sys
#2018/06/19
#made by Kazunari Morita


#横の判定    
def check_row():
    
    for i in range(15):
        p_judge=0
        e_judge=0        
        for j in range(15):
            if bord[i][j]==1:
                p_judge+=1
            if bord[i][j]==2:
                e_judge+=1
            if bord[i][j]==0:
                #もし, 連続していなかったら0
                p_judge=0
                e_judge=0
            if p_judge>=5:
                #盤面の描画
                display_bord()
                print '\n\n'
                print 'You Win'
                print '\n\n'
                exit(-1)
            
            if e_judge>=5:
                #盤面の描画
                display_bord()
                
                print '\n\n'
                print 'You Lose'
                print '\n\n'
                exit(-1)


#縦の判定
def check_colmun():

    for i in range(15):
        p_judge=0
        e_judge=0

        for j in range(15):
            if bord[j][i]==1:
                p_judge+=1
            if bord[j][i]==2:
                e_judge+=1
            if bord[j][i]==0:
                #もし, 連続していなかったら0
                p_judge=0
                e_judge=0
    
            if p_judge>=5:
                #盤面の描画
                display_bord()
                
                print '\n\n'                    
                print 'You Win'
                print '\n\n'
                exit(-1)
                break
            
            if e_judge>=5:
                #盤面の描画
                display_bord()
                print '\n\n'
                print 'You Lose'
                print '\n\n'
                exit(-1)
                break

#斜め(右下)の判定
def check_slanting_right():

    for i in range(11):
        p_judge=0
        e_judge=0
        for j in range(11):
            for k in range(5):
                if bord[i+k][j+k]==1:
                    p_judge+=1
                if bord[i+k][j+k]==2:
                    e_judge+=1
                if bord[i+k][j+k]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0

                if p_judge>=5:
                    #盤面の描画
                    display_bord()
                
                    print 'You Win'
                    print '\n\n'
                    exit(-1)
                    break
                
                if e_judge>=5:
                    #盤面の描画
                    display_bord()
                
                    print '\n\n'                        
                    print 'You Lose'
                    print '\n\n'
                    exit(-1)
                    break



def check_slanting_left():
   #斜め(左下)の判定    
    for i in range(11):
        p_judge=0
        e_judge=0
        for j in range(4,15):
            for k in range(5):
                if bord[i+k][j-k]==1:
                    p_judge+=1
                if bord[i+k][j-k]==2:
                    e_judge+=1
                if bord[i+k][j-k]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0

                if p_judge>=5:
                    #盤面の描画
                    display_bord()
                
                    print 'You Win'
                    print '\n\n'
                    exit(-1)
                
                if e_judge>=5:
                    #盤面の描画
                    display_bord()
                
                    print 'You Lose'
                    print '\n\n'
                    exit(-1)

#引き分け判定
def check_draw():
    
    if 0 not in bord:
        #盤面の描画
        display_bord()
                
        print 'Draw'
        print '\n\n'
        exit(-1)


#プレイヤーのターン
def player_turn():
    print 'Your Turn'
    
    p_x_pos = input('select ball x pos > ')
    p_y_pos = input('select ball y pos > ')
    while bord[p_y_pos-1][p_x_pos-1] == 1 or  bord[p_y_pos-1][p_x_pos-1] == 2 or p_x_pos<1 or p_x_pos>15 or  p_y_pos<1 or p_y_pos>15: 

        print 'please retry'
        p_x_pos = input('select ball x pos > ')
        p_y_pos = input('select ball y pos > ')
    bord[p_y_pos-1][p_x_pos-1] = 1

#敵のターン
def enemy_turn():
    print 'Enemy Turn'
    
    #敵(ランダム)で配置
    e_x_pos = random.randint(0,14)
    e_y_pos = random.randint(0,14)
    
    #もし, プレイヤーの玉なければ配置, あれば乱数再生成
    while bord[e_y_pos][e_x_pos] == 1 or  bord[e_y_pos][e_x_pos] == 2:
    
        #乱数再生成
        e_x_pos = random.randint(0,14)
        e_y_pos = random.randint(0,14)

    bord[e_y_pos][e_x_pos] = 2  


#盤面の表示
def display_bord():
    for i in range(15):
        for j in range(15):
            if  bord[i][j]==0:
                print pycolor.WHITE+'+'+ pycolor.END,

            elif bord[i][j]==1:
                print pycolor.RED+'●'+pycolor.END,

            elif bord[i][j]==2:
                print pycolor.BLUE+'■'+pycolor.END,

        print '\n',
    print '[You]'+pycolor.RED+'●'+pycolor.END, '\t[Enemy]'+pycolor.BLUE+'■'+pycolor.END,
    print '\n\n'

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

    end_flag = False
    bord = np.zeros([15,15])
    while not end_flag:

        #盤面の描画
        display_bord()

        #プレイヤーのターン
        player_turn()

        #縦横斜めの勝利判定
        check_colmun()
        check_row()
        check_slanting_left()
        check_slanting_right()

        #敵のターン
        enemy_turn()

        #引き分け判定
        check_draw()