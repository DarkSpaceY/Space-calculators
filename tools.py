import time
import numpy as np

#******************** 帮助 ********************
class __help__:
    
    def ProgressBar():
        print('''use the progress bar like this:

    progress_bar = ProgressBar()
    progress_bar.show(0,100)
    for i in range(100):
        ...
        progress_bar.show(i+1,100)''')
        print('\nprogress bar with title and tail:')
        progress_bar = ProgressBar(refresh_time = 0.5, eta_refresh_time=0.5)
        tt_times = 100
        progress_bar.show(0,tt_times)
        print('')
        for i in range(tt_times):
            progress_bar.show(i+1,tt_times)
            if i == 27: print('')
            time.sleep(0.05)
        print('\nprogress bar without title and tail:')
        progress_bar = ProgressBar(refresh_time = 0.5, eta_refresh_time=0.5)
        tt_times = 100
        progress_bar.show(0,tt_times,' title','tail')
        print('')
        for i in range(tt_times):
            progress_bar.show(i+1,tt_times,' title','tail')
            if i == 27: print('')
            time.sleep(0.05)

#******************** 进度条 ********************
class ProgressBar():
    
    def __init__(self, refresh_time=0.1, eta_refresh_time=0.1):
        self.__version__ = '1.2.0-202207032329'
        time_nowTime = time.time()
        self.refresh_time = refresh_time
        self.eta_refresh_time = eta_refresh_time
        self.time_startTime = time_nowTime #进度条开始时间
        self.time_lastRefreshTime = time_nowTime #进度条上一次刷新时间
        self.eta = '  ETA: ##' #预计剩余时间
        self.eta_lastRefreshTime = time_nowTime #eta上一次刷新时间
        self.loadingListIndex = 0 #加载标志的Index(|/-\)
    
    #秒的单位转化
    def sec_in_units(self,sec):
        '''
Make the unit of time(second) better.

Parameters
----------
sec : int
    The time (second)

Returns
-------
out : string
    The string of the time with a better unit

----------------------------------------------------------------

改进时间单位（秒）。

参数
----------
sec : int
    时间（秒）

返回值
-------
out : 字符串
    用更好的单位表示时间的字符串
    '''
        if sec <1e-11: sec = '<0.01ns'
        elif sec < 1e-9: sec = '%.02f'%(sec*1e9)
        elif sec < 1e-6: sec = '%dns'%(sec*1e9)
        elif sec < 1e-3: sec = '%dus'%(sec*1e6)
        elif sec < 1: sec = '%dms'%(sec*1e3)
        elif sec < 60: sec = '%ds'%sec
        elif sec < 3600: sec = '%02d:%02ds'%(sec//60,sec%60)
        elif sec < 86400: sec = '%02d:%02d:%02ds'%(sec//3600,sec%3600//60,sec%60)
        else: sec = '%dDay %02d:%02d:%02ds'%(sec//86400,sec%86400//3600,sec%3600//60,sec%60)
        return sec
    
    #进度条
    def show(self,times,total_times,title='',tail=''):
        '''
Print a progress bar.

Parameters
----------
times : int
    How many times the loop or other is run.
total_times : int
    How many times the loop or other runs in total.
title : string
    The title of the progress bar.
tail : string
    The tail of the progress bar.

Examples
--------
use the progress bar like this:

>>> progress_bar = ProgressBar()
>>> progress_bar.show(0,100)
>>> for i in range(100):
        ...
        progress_bar.show(i+1,100)

----------------------------------------------------------------

打印进度条。

参数
----------
times : int
    循环运行的次数。
total_times : int
    循环运行的总次数。
title : string
    进度条的标题。
tail : string
    进度条的尾部。

示例
--------
像这样使用进度条：

>>> progress_bar = ProgressBar()
>>> progress_bar.show(0,100)
>>> for i in range(100):
        ...
        progress_bar.show(i+1,100)
'''
        
        # raise error
        if (type(times) != int) or (times < 0): raise TypeError("'times' must be a positive integer.")
        if (type(total_times) != int) or (total_times < 0): raise TypeError("'total_times' must be a positive integer.")
        if type(title) != str: raise TypeError("'title' must be a string.")
        if type(tail) != str: raise TypeError("'tail' must be a string.")
        if times > total_times: raise ValueError(f"'times' must be no greater than 'total_times', but {times} > {total_times}")
        
        
        #初始化参数
        time_nowTime = time.time()
        barList = ['  ','▏','▎','▍','▌','▋','▊','▉','█']
        loadingList = ['|','/','-','\\']
        refresh_time = self.refresh_time
        eta_refresh_time = self.eta_refresh_time
        
        #次数为0时，初始化进度条
        if times == 0:
            self.time_startTime = time_nowTime #初始化时间
            self.time_lastRefreshTime = time_nowTime #同上
            self.eta = '  ETA:----' #绘制ETA
            bar = '[▏                  ]' #绘制bar
            per = f' 0.00%(0/{total_times})' #绘制百分比
            print('\r|'+title+bar+tail+per+self.eta+'          '*2,end='') #打印进度条
        
        #当运行结束时，结束并绘制进度条
        if times == total_times:
            each_use_time = self.sec_in_units((time_nowTime-self.time_startTime)/total_times) #每次运行的时间
            self.eta = '  total:'+self.sec_in_units(time_nowTime-self.time_startTime)+'/each:'+each_use_time #绘制总计
            bar = '[██████████]' #绘制bar
            per = f' 100.00%({total_times}/{total_times})' #绘制百分比
            print('\r*'+title+bar+tail+per+self.eta+'          ')
        
        else:
            
            #当前次数与上一次eta刷新时间间隔大于设定的eta刷新时间时，计算eta
            if  (time_nowTime - self.eta_lastRefreshTime >= eta_refresh_time) and (times != 0): 
                self.eta = '  ETA:'+self.sec_in_units(int((total_times-times)/times * (time.time()-self.time_startTime)))
                self.eta_lastRefreshTime = time_nowTime #更新eta上一次刷新时间
            
            #当前时间与进度条上一次刷新时间间隔大于设定的刷新时间时，刷新进度条
            if time_nowTime - self.time_lastRefreshTime >= refresh_time: 
                
                #绘制进度条（bar）
                if (int((times/total_times)//0.1)+int((times/total_times)%0.1//0.0125)) == 0: #避免第0次时进度条没有显示
                    bar = '[▏                  ]'
                else: 
                    bar = '['+int((times/total_times)//0.1)*'█'+barList[int((times/total_times)%0.1//0.0125)]+(9
                                                                            -int((times/total_times)//0.1))*'  '+']'
                
                #绘制百分比 e.g. 7.03%(213/3029)
                per = ' %.02f'%(times/total_times*100)+'%'+f'({times}/{total_times})'
                #绘制加载标志
                self.loadingListIndex += 1
                if self.loadingListIndex >3: self.loadingListIndex = 0
                
                self.time_lastRefreshTime = time_nowTime #更新进度条上一次刷新时间
                print('\r'+loadingList[self.loadingListIndex]+title+bar+tail+per+self.eta+'          ',end='') #打印进度条
class Orbit:
    def __init__(self):
        R_earth = 6371000.0 #地球半径
        g_earth = 9.8 #地表重力加速度
        M_earth = 5.972e24 #地球质量
        G = 6.67408e-11 #万有引力常数
        M_sun = 1.98892e30 #太阳质量
        D_sun_earth = 149597870000.0 #地日距离
    def acceleration_gravity(self,r=6371000.0,M=5.972e24,G=6.67408e-11):# inputs:r轨道半径,M环绕天体质量
        """
Print a number(the acceleration of gravity)
acceleration_gravity(self,r=self.R_earth,M=self.M_earth,G=self.G)
Parameters
----------
r : float
    The radius of an object's orbit around a celestial body
M : float
    The mass of a celestial body orbited by an object
G : float
    Gravitational constant.

------------------------------------------------

打印一个数字（重力加速度）

参数
----------
r : float
    物体绕天体运行的半径
M : float
    天体围绕天体运行的质量
G : float
    引力常数。
    """
        gr = G*(M/r**2)
        return gr
    
    def speed_object(self,r,g=9.8,R=6371000.0):
        """
Print a number(the speed of the object)
speed_object(self,r=R_earth,g=g_earth,R=R_earth)
Parameters
----------
r : float
    The radius of an object's orbit around a celestial body
g : float
    Gravitational acceleration on the celestial body's surface
R : float
    Radius of celestial body.

----------------------------------------------------------------

打印一个数字（物体的速度）

参数
----------
r : float
    物体绕天体运行的半径
g : float
    天体表面的重力加速度
R : float
    天体的半径。
    """
        v = ((g*R**2)/r)**0.5
        return v
    def object_orbital_period(self,v,pi=np.pi,r=6371000.0):
        """
Print a number(object's orbital period)
object_orbital_period(self,v,pi=np.pi,r=R_earth)
Parameters
----------
v : float
    the speed of the object
pi : float
    PI,constant
r : float
    The radius of an object's orbit around a celestial body

----------------------------------------------------------------

打印一个数字（物体的轨道周期）

参数
----------
v : float
    物体的速度
pi : float
    PI,常数
r : float
    物体绕天体运行的半径
    """     
        Tr = (2*pi*r)/v
        return Tr
    
    def first_cosmic_velocity(self,g=9.8,R=6371000.0):
        """
Print a number(first cosmic velocity)
first_cosmic_velocity(self,g=g_earth,R=R_earth)
Parameters
----------
g : float
    Gravitational acceleration on the celestial body's surface
R : float
    Radius of celestial body.

----------------------------------------------------------------

打印一个数字（第一宇宙速度）

参数
----------
g : float
    天体表面的重力加速度
R : float
    天体半径。
    """     
        v1 = (g*R)**0.5
        return v1

    def second_cosmic_velocity(self,g=9.8,R=6371000.0):
        """
Print a number(second cosmic velocity)
second_cosmic_velocity(self,g=g_earth,R=R_earth)
Parameters
----------
g : float
    Gravitational acceleration on the celestial body's surface
R : float
    Radius of celestial body.

----------------------------------------------------------------

打印一个数字（第二宇宙速度）

参数
----------
g : float
    天体表面的重力加速度
R : float
    天体半径。
    """     
        v2 = (2*g*R)**0.5
        return v2

    def launch_speed(self,r,v2,R=6371000.0):
        """
Print a number
(The velocity required to ascend from the surface to an orbit of radius r)
launch_speed(self,r,v2,R=R_earth)
Parameters
----------
r : float
    The radius of an object's orbit around a celestial body
v2 : float
    second cosmic velocity
R : float
    Radius of celestial body.

----------------------------------------------------------------

打印一个数字
(从表面上升到半径为r的轨道所需的速度）

参数
----------
r : float
    天体轨道的半径
v2 : float
    第二宇宙速度
R : float
    天体半径。
    """     
        v = v2*(1-R/(2*r))**0.5
        return v
    
    def stellar_gravitational_acceleration(self,M_star=1.98892e30,M_planet=5.972e24,g=9.8,R=6371000.0,D=149597870000.0):
        """
Print a number
(The stellar gravitational acceleration)
stellar_gravitational_acceleration(self,M_star=M_sun,M_planet=M_earth,g=g_earth,R=R_earth,D=D_sun_earth)
Parameters
----------
M_star : float
    The mass of the star.
M_planet : float
    The mass of the planet.
g : float
    Gravitational acceleration on the planet's surface
R : float
    Radius of the planet.
D : float
    Distance between planet and star.

----------------------------------------------------------------

打印一个数字
(恒星重力加速度）

参数
----------
M_star : float
    恒星的质量。
M_planet : float
    行星的质量。
g : float
    行星表面的重力加速度。
R : float
    行星的半径。
D : float
    行星与恒星之间的距离。
    """     
        g_star = g_planet*(M_star/M_planet)*(R/D)**2
        return g_star
    def kinetic_energy(self,v,m=1):
        """
Print a number
(kinetic_energy)
kinetic_energy(self,v,m=1)
Parameters
----------
v : float
    The speed.
m : float
    The mass.

----------------------------

打印一个数字
(动能)

参数
----------
v : float
    速度。
m : float
    质量。
    """     
        return v**2*m/2
    def momentum(self,v,m=1):
        """
Print a number
(momentum)
momentum(self,v,m=1)
Parameters
----------
v : float
    The speed.
m : float
    The mass.

----------------------------

打印一个数字
(动量)

参数
----------
v : float
    速度。
m : float
    质量。
    """     
        return m*v
    def third_cosmic_velocity(self,v2,M_star=1.98892e30,M_planet=5.972e24,R=6371000.0,D=149597870000.0):
        """
Print a number(Third cosmic velocity)
third_cosmic_velocity(self,v2,M_star=M_sun,M_planet=M_earth,R=R_earth,D=D_sun_earth)
Parameters
----------
v2 : float
    third cosmic velocity
M_star : float
    The mass of the star.
M_planet : float
    The mass of the planet.
R : float
    Radius of the planet.
D : float
    Distance between planet and star.

----------------------------------------------------------------

打印一个数字(第三宇宙速度)
third_cosmic_velocity(self,v2,M_star=M_sun,M_planet=M_earth,R=R_earth,D=D_sun_earth)
参数
----------
v2 : float
    第三宇宙速度
M_star : float
    恒星的质量。
M_planet : float
    行星的质量。
R : float
    行星的半径。
D : float
    行星与恒星之间的距离。
    """     
        v3 = v2*(1+(M_star/M_planet)*(R/D)*((2-2**0.5)/2)**2)**0.5
        return v3
