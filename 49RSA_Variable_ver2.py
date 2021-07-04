# -*- coding: utf-8 -*-
"""

RSA

Created on Tue Jun 22 09:46:41 2021

@author: Shun

公開鍵暗号方式
C≡P^e(mod n) 暗号化

P≡C^d(mod n)　復号化

ディジタル署名
C≡P^d(mod n) 暗号化

P≡C^e(mod n)　復号化

n=p*q

L=LCM(p-1,q-1)=p-1*q-1/gcd(p,q)

Max{p,q}<e<L and L e が互いに素な数
gcd(l,e)=1

# MAX{p,q}<e<Lに必要

暗号文C =平文^e mod N
平文P   =暗号文^d mod N

Nを可変ではなく　ASC2にのっとって作成　str_listに直接　P,Cを書き込める　時間の短縮が可能になる。(文字入力の)

平文       N     d 
暗号文     N   e
公開鍵     N L e d 
秘密鍵     N L e d

"""
#from rsa import Rsa
import sympy
import sys
def main():
    
    print("RSA")
    #N 1024bit~4096bit　推奨　https://ja.wikipedia.org/wiki/RSA%E6%9A%97%E5%8F%B7#n_%E3%82%92%E6%B3%95%E3%81%A8%E3%81%99%E3%82%8B%E5%86%AA%E5%89%B0%E4%BD%99%E3%81%AE%E8%A8%88%E7%AE%97
    bit = int(input("1024bit　推奨 \n bit:"))
    #bit = pow(2,bit)
    #p
    #p = sympy.randprime(bit-1,bit) 素数が存在しないだと...l48 そりゃそうだな　if 3bitの時 7,8だから範囲内に素数はできない。
    p = sympy.randprime(pow(2,bit-1),pow(2,bit))
    #q
    q = sympy.randprime(pow(2,bit-1),pow(2,bit))
    
    while(1):
        if p==q:
            p = sympy.randprime(pow(2,bit-1),pow(2,bit))
        else:
            break    
    #n
    n = p*q
    
    #L
    L = int(sympy.lcm(p-1,q-1))
    
    #e
    #max_num = (p,q) tuple型であるため　整数などの反復不可能なデータ型ではエラーをおこす。 https://www.digitalocean.com/community/tutorials/how-to-convert-data-types-in-python-3-ja
    if p > q :
        max_num = p
    else:
        max_num = q
        
    while(1):
        e = sympy.randprime(max_num,L)
        if sympy.gcd(max_num,L) and max_num < e < L:
            break
    
    
    while(1):#bit,p,q,L,e
        try:
            print("動作モードを選択してください")
            mode = (int(input("公開鍵:1,秘密鍵:2,暗号化:3,復号化:4,終了:5 \n input:")))
            if mode == 1:
                print("公開鍵n:\n",n,"\n公開鍵e:\n",e)
            elif mode ==2:
                d = secret_key(e,L)
                print("公開鍵n:\n",n,"\n公開鍵e:\n",e)
                print("秘密鍵p:\n",p,"\n秘密鍵q:\n",q,"\n秘密鍵L:\n",L,"\n秘密鍵d:\n",d)
            elif mode ==3:
                #P　平文
                P = (input("文字列を入力　95種類　大文字　小文字　数字 etc \n"))
                P = char_to_int(P)
                C = encrypt(P,e,n)
                C = int_to_char(C)
                print("暗号文:",C)
                            
            elif mode ==4:
                d = secret_key(e,L)
                mode_cryptogram = int(input("以前の暗号を利用するなら:0を入力してください。以外なら:1 \n C:"))
                if mode_cryptogram==0:
                    C = char_to_int(C)
                    P = dencrypt(C,d,n)
                    P = int_to_char(P)
                    print("P平文:",P)
                elif mode_cryptogram==1:
                    C = (input("文字列を入力　95種類　大文字　小文字　数字 etc \n"))
                    C = char_to_int(C)
                    P = dencrypt(C,d,n)
                    P = int_to_char(P)
                    print("P平文:",P)
                else:
                    raise ValueError
            elif mode ==5:
                break
            else:
                raise ValueError
                sys.exit()
                
        except ValueError:
             print('入力値が不正です')  
      

def secret_key(e,L):#受信者
    x,y,t = sympy.gcdex(e,L) #modをこれに入れることができるのでは　プログラムコピーして作って　rsa もう一度
    #d
    d = int(x) % L
    return d

def encrypt(P,e,n):#暗号化
    C = pow(P,e,n)
    return C

def dencrypt(C,d,n):#復号化
    P = pow(C,d,n)
    return P
    
     
def char_to_int(P_C: str)->int:
    print(list(P_C))

    P_C_list = list(P_C)#1文字ずつ格納
    P_C_size = len(P_C_list)
    total = 0
    num_list = []
    print(P_C_list)
    for i in range(0,P_C_size):
        num_list.append(ord(P_C_list[i])-32)
    num_list.reverse()
    
    for i in range(0,len(num_list)):
        total += num_list[i]*pow(95,i)#文字　数字　etc 95種類
        print(total) 
    return total
    
def int_to_char(P_C_int: int) ->chr: #数字から文字 N=95
    qlist = []#商の保存先 quotient
    rlist = []#余り remainder
    while(P_C_int>=95):
        q = P_C_int // 95
        r = P_C_int % 95
        qlist.append(q)#商と余りを式の番号ごとに保存
        rlist.append(r)
        P_C_int = q
    if P_C_int // 95 < 95:
        r = P_C_int % 95
        rlist.append(r)    
    rlist.reverse()
    
    char_list = []
    for i in range (0,len(rlist)):
        char_list.append(chr(rlist[i]+32))
    P_C_char = "".join(char_list)
    
    return P_C_char


if __name__ == "__main__":
    main()
