
//键盘显示窗口大小
display:{
    width: 900
    height:400
}
init: {
    // 背景音乐
    background: {
        // 背景音默认音量
        power: 100
        // 几个单独的弹奏
        channels: 1
        // 如果有多个弹奏，每多少节放到一个弹奏里，轮流放
        channel_unit: 4
        // 按键1的音调
        base: 60
        // 背景乐谱文件，没有则不会有背景音
        fp: null
        // fp: r"D:\rootz\python\gits\musicz_pygm_upd\musicz_pygm\conf\kl.js"
        // 1节的时长
        sec: 2
        // 背景音乐循环
        loop: true
        // 背景音乐结束后运行结束
        stop: true
    }
    // 背景音乐(记录模式)
    record: {
        // 背景音默认音量比例
        power_rate: 1.0
        // 播放速度加速比
        speed_rate: 1.0
        // 背景乐谱文件，没有则不会有背景音
        fp: null
        // fp: r"D:\rootz\python\gits\musicz_pygm_upd\musicz_pygm\conf\kl.js"
        // 背景音乐循环
        loop: true
        // 背景音乐结束后运行结束
        stop: true
    }
    select: {
        channel: 0 // MIDI通道号（0-15），9号通道通常预留给打击乐, 0是钢琴
        bank: 0 //音色库编号（0-16383），GM标准中0为常规乐器，128为打击乐
        preset: 0//音色编号（0-127），对应SoundFont(sf2文件)中的预设程序
    }
    sample_rate: 44100 //采样频率，这个应该要和sf2文件的实际频率保持一致，一般就是44100
    sfile: null // sf2音频文件路径，本地测试用的FluidR3Mono_GM.sf2（不知道和FluidR3_GM.sf2有什么不同，反正都是网上下的免费资源）
    libpath: null //fluidsynth库路径，在windows下没有在PATH配置fluidsynth路径时使用
    fps: 30 // 按键监听fps
}
saves: {
    filepath: "%Y%m%d%H%M%S.json"
    work: false
}
// 按shift后正常按键实际输出到原本按键输出的映射
transforms: {
    '!':1,'@':2,'#':3,'$':4,'%':5,'^':6,'&':7,'*':8,'(':9,')':10,'_':'-','+':'='
    Q=q,W:w,E:e,R:r,T:t,Y:y,U:u,I:i,O:o,P:p,'{':'[','}':']','|':'\\'
    A:a,S=s,D:d,F:f,G:g,H:h,J:j,K:k,L:l,':':';','"':"'"
    Z=z,X=x,C=c,V=v,B=b,N=n,M=m,'<'=',','>'='.','?'='/'
}
keys: {
    soundfix: {
        // 按键音声音大小调整，相同声音大小下，低音听起来声音更大，引入修改量，低音到高音对应 min到max
        min: -15//-55
        max: 0//10
    }
    mode: 1 //按键模式，1是按键松开后继续播放按键声音，0是松开后立刻停止按键声音
    left: {
        keys: {
            q=0,w=1,e=2,r=3,t=4,1=5,2=6,3=7,4=8,5=9,y=10,6=11
            z=12,x=13,c=14,v=15,b=16,a=17,s=18,d=19,f=20,g=21,tab=22,h=23
        }
        // keys: [1,2,3,4,5,6,q,w,e,r,t,y,a,s,d,f,g,h,z,x,c,v,b,tab]
        base: {
            val: 48
            vals: [12,24,36,48,60,72]
            up: shift_l
            down: ctrl_l
            move_val: 12
            move: alt_l
            //down: [shift_l, ctrl_l]//alt_l
        }
        power: {
            val: 120
            vals: [70,80,90,100,110,120]
            up: right
            down: left
        }
    }
    right:{
        keys: {
            n=0,m=1,','=2,'.'=3,'/'=4,j=5,k=6,l=7,';'=8,"'"=9,"\\"=10,enter=11
            u=12,i=13,o=14,p=15,'['=16,7=17,8=18,9=19,0=20,'-'=21,']'=22,'='=23,backspace=24
        }
        // keys: [n,m,',','.','/',j,k,l,';',"'",u,i,o,p,'[',']',7,8,9,0,'-','=','\\','enter','backspace']
        base: {
            val: 72
            vals: [36,48,60,72,84]
            up:shift_r
            down: ctrl_r //alt_r
            move_val: 12
            move: alt_r
        }
        power: {
            val: 100
            vals: [70,80,90,100,110,120]
            up: up
            down: down
        }
    }
    // base: {
    //     //左右按键基础音
    //     q=0,w=1,e=2,r=3,t=4,1=5,2=6,3=7,4=8,5=9,y=10,6=11
    //     z=12,x=13,c=14,v=15,b=16,a=17,s=18,d=19,f=20,g=21,tab=22,h=23

    //     n=0,m=1,','=2,'.'=3,'/'=4,j=5,k=6,l=7,';'=8,"'"=9,'\\'=10,enter=11
    //     u=12,i=13,o=14,p=15,'['=16,7=17,8=18,9=19,0=20,'-'=21,']'=22,'='=23,backspace=24
    // }
    //瞬间停止声音播放
    stop: space
    // 当前配置是按下shift+'`'（也就是'~'）退出程序
    quit: '~'
    change_mode: '`'
}