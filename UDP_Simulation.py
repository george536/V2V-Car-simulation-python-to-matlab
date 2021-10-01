import time
import random
import keyboard
import socket


class Car:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.ppl=[]
        self.line=False;
        self.another_car=False
        self.anoth_car_w=[((self.width/2)-5)-1,((self.width/2)-5)-2,((self.width/2)-5)-3,((self.width/2)-5)-4,((self.width/2)-5)-5,((self.width/2)-5)-6,((self.width/2)-5)-7,((self.width/2)-5)-8,((self.width/2)-5)-9,((self.width/2)-5)-10,((self.width/2)-5)-11]
        self.anoth_car_h=[-2,-1,0,1]
        self.car_w=[((self.width/2)-5)-1,((self.width/2)-5)-2,((self.width/2)-5)-3,((self.width/2)-5)-4,((self.width/2)-5)-5,((self.width/2)-5)-6,((self.width/2)-5)-7,((self.width/2)-5)-8,((self.width/2)-5)-9,((self.width/2)-5)-10,((self.width/2)-5)-11]
        self.car_h=[self.height-1,self.height-2,self.height-3]
        self.location="left"
        self.speed=50

    def AnotherCar(self):
        poss=random.randint(0,6)
        if poss==3:
            if self.another_car==False:
                if self.location=="left":
                    self.anoth_car_w=[((self.width/2)-5)+19,((self.width/2)-5)+18,((self.width/2)-5)+17,((self.width/2)-5)+16,((self.width/2)-5)+15,((self.width/2)-5)+14,((self.width/2)-5)+13,((self.width/2)-5)+12,((self.width/2)-5)+11,((self.width/2)-5)+10,((self.width/2)-5)+9]

                if self.location=="right":
                    self.anoth_car_w=[((self.width/2)-5)-1,((self.width/2)-5)-2,((self.width/2)-5)-3,((self.width/2)-5)-4,((self.width/2)-5)-5,((self.width/2)-5)-6,((self.width/2)-5)-7,((self.width/2)-5)-8,((self.width/2)-5)-9,((self.width/2)-5)-10,((self.width/2)-5)-11]
                
                self.another_car=True

    def Another_car_movment(self):
        for i in range(0,len(self.anoth_car_h)):
                self.anoth_car_h[i]+=1
        if self.anoth_car_h[0]>self.height:
            self.another_car=False
            self.anoth_car_h=[-2,-1,0,1]   

    def input(self):
        if keyboard.is_pressed('a'):
            if self.location=="right":
                for i in range(0,len(self.car_w)):
                    self.car_w[i]-=20
                self.location="left"

        if keyboard.is_pressed('d'):
            if self.location=="left":
                for i in range(0,len(self.car_w)):
                    self.car_w[i]+=20
                self.location="right"

    def velocity(self):
        if keyboard.is_pressed('w'):
            self.speed+=5

        if keyboard.is_pressed('s'):
            if self.speed>5:
                self.speed-=5

    def people(self):
        possibality=random.randint(1, 10)
        if possibality >4 and possibality <10 and len(self.ppl)<self.height-1:
            while True:
                y=random.randint(0,self.height)
                if y not in self.ppl:
                    self.ppl.append(y)
                    break;
        else:
            if len(self.ppl)!=0:
                self.ppl.pop(len(self.ppl)-1)

    def draw(self):
        def cls():
            print("\n"*50)
        cls()
        for z in range(0,self.width+2):
            print("█",end ="")
        print("\n")
        for i in range (0,self.height):
            for j in range (0,self.width):
                if j==0:
                    print("█",end ="")

                elif i%2==0 and j==self.width/2 and self.line==False:
                    print("█",end="")

                elif i%2!=0 and j==self.width/2 and self.line==True:
                    print("█",end="")

                elif i in self.car_h and j in self.car_w:
                    print ("Θ",end="")

                elif i in self.anoth_car_h and j in self.anoth_car_w and self.another_car==True:
                    print("*",end="")

                elif j==self.width-1:
                     print("█",end ="")
                     if i in self.ppl:
                         print("Pedestrian",end="")
                else:
                    print (" ",end ="")
            print("\n")
        for d in range(0,self.width+2):
           print("█",end ="")
        print("\n")

        if self.line==False:
            self.line=True
        else:
            self.line=False

    def info(self):
        print("The car is on the "+self.location+" side of the road")
        print("There are ",len(self.ppl)," people on the right side of the road")
        print("the car's speed is: ",self.speed," km/h")
        if self.another_car==True:
            print("there is another car close by on the road")
        else:
            print("there are no other cars on the road")
        print("data sent to IP 127.0.0.1")

    def send(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        address1=("127.0.0.1",4444)
        address2=("127.0.0.1",4443)
        address3=("127.0.0.1",4442)
        address4=("127.0.0.1",4441)
        if self.location=="left":
            loc="left "
        else: loc=self.location
        sock.sendto(bytes("The car is on the "+loc+" side of the road","utf-8"),address1)
        if len(self.ppl)<10:
            ppl_num=" "+str(len(self.ppl))
        else:
            ppl_num=str(len(self.ppl))
        sock.sendto(bytes("There are "+ppl_num+" people on the right side of the road","utf-8"),address2)
        if self.speed<10:
            car_spd=" "+str(self.speed)
        else:
            car_spd=str(self.speed)
        sock.sendto(bytes("the car's speed is: "+car_spd+" km/h","utf-8"),address3)
        if self.another_car==True:
            sock.sendto(bytes("there is another car close by on the road","utf-8"),address4)
        else:
            sock.sendto(bytes("there's no other car close by on the road","utf-8"),address4)

    def run(self):
        while True:
            self.input()
            self.people()
            self.velocity()
            self.AnotherCar()
            self.Another_car_movment()
            self.draw()
            #self.info()
            self.send()
            print("data sent to IP 127.0.0.1")
            time.sleep(0.75)

def main():
    car=Car(40,10)
    car.run()


main()
