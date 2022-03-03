import tkinter, numpy, threading, time, random


nb_room = int(input("Combien veut-tu de classe ?"))
room_list = []

width = 100 + nb_room * 400
height = 700

root = tkinter.Tk()
root.title('Représentation ppm')
root.geometry(f"{width}x{height}")

background = 'white'
canvas_width = width
canvas_height = height
my_canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height, bg=background)
my_canvas.pack()

augmentation_ppm = 29
time_mutiplicator = 0.05 # mean 200 ms ig === 1 min irl with a refresh every 10 ms
augmentation_ppm *= time_mutiplicator

closed_door_exchange = 1
open_door_exchange = 3
closed_max_ppm_flow = 300
open_max_ppm_flow = 1000

def door_ppm_exchanger(door_open, room_num):
   room1 = room_list[room_num]
   room2 = room_list[room_num + 1]

   room1_ppm = room1.ppm
   room2_ppm = room2.ppm
   difference_ppm = room1_ppm - room2_ppm
   if door_open == False:
      exchange = closed_door_exchange
      ppm_change = (min(abs(difference_ppm), closed_max_ppm_flow) * exchange) * time_mutiplicator
   else:
      exchange = open_door_exchange
      ppm_change = (min(abs(difference_ppm), open_max_ppm_flow) * exchange) * time_mutiplicator

   # print(ppm_change)
   if difference_ppm >= 0:
      room1.ppm_add(-ppm_change)
      room2.ppm_add(ppm_change)
   else:
      room1.ppm_add(ppm_change)
      room2.ppm_add(-ppm_change)

      



class Classroom():
   def __init__(self, room_num):

      self.room_num = room_num
      self.decalage = room_num * 400
      global nb_room
      if room_num != nb_room - 1:
         self.second_door = bool(random.getrandbits(1))
      else:
         self.second_door = False

      # Base classroom
      my_canvas.create_line( 50 + self.decalage, 50, 100 + self.decalage, 50, fill="red")
      my_canvas.create_line( 200 + self.decalage, 50, 450 + self.decalage, 50, fill="red")
      my_canvas.create_line( 50 + self.decalage, 450, 300 + self.decalage, 450, fill="red")
      my_canvas.create_line( 400 + self.decalage, 450, 450 + self.decalage, 450, fill="red")


      # Window
      self.window_open = False
      self.window1 = my_canvas.create_line( 100 + self.decalage, 50, 100 + self.decalage, 100, fill="white")
      self.window2 = my_canvas.create_line( 200 + self.decalage, 50, 200 + self.decalage, 100, fill="white")
      self.window3 = my_canvas.create_line( 100 + self.decalage, 50, 201 + self.decalage, 50, fill="black")
      tkinter.Button(root, text ="Open / Close window", command = self.move_window).place(x= 100 + self.decalage, y=10)

      #  Door
      self.door_open = False
      self.door1 = my_canvas.create_line( 300 + self.decalage, 450, 300 + self.decalage, 350, fill="white")
      self.door2 = my_canvas.create_line( 300 + self.decalage, 450, 400 + self.decalage, 450, fill="black")
      tkinter.Button(root, text ="Open / Close door", command = self.move_door).place(x= 170 + self.decalage, y= 400)

      # Second Door
      if self.second_door == True:
         self.second_door_open = False
         my_canvas.create_line( 450 + self.decalage, 50, 450 + self.decalage, 100, fill="red")
         my_canvas.create_line( 450 + self.decalage, 200, 450 + self.decalage, 450, fill="red")
         self.s_door1 = my_canvas.create_line( 350 + self.decalage, 200, 450 + self.decalage, 200, fill="white")
         self.s_door2 = my_canvas.create_line( 450 + self.decalage, 100, 450 + self.decalage, 200, fill="black")
         tkinter.Button(root, text ="Open / Close door", command = self.move_second_door).place(x= 300 + self.decalage, y= 150)
      else:
         my_canvas.create_line( 450 + self.decalage, 50, 450 + self.decalage, 450, fill="red")



      # jauge
      self.green = my_canvas.create_rectangle(70 + self.decalage, 320, 130 + self.decalage, 420, fill='green', outline='green')
      self.yellow = my_canvas.create_rectangle(70 + self.decalage, 250, 130 + self.decalage, 320, fill='yellow', outline='yellow')
      self.orange = my_canvas.create_rectangle(70 + self.decalage, 200, 130 + self.decalage, 250, fill='orange', outline='orange')
      self.red = my_canvas.create_rectangle(70 + self.decalage, 170, 130 + self.decalage, 200, fill='red', outline='red')
      self.black = my_canvas.create_rectangle(70 + self.decalage, 140, 130 + self.decalage, 170, fill='black', outline='black')
      
      self.white = my_canvas.create_rectangle(70 + self.decalage, 140, 130 + self.decalage, 370, fill= background, outline= background)

      # ppm
      self.ppm = 500       # ppm at begening
      self.ppm_start = 0
      self.t = 0
      self.jauge()
      self.display_ppm = my_canvas.create_text(250 + self.decalage, 250, anchor="center", text=int(self.ppm))



   def move_window(self):
      if not self.window_open:
         self.window1 = my_canvas.create_line( 100 + self.decalage, 50, 200 + self.decalage, 50, fill="white")
         self.window2 = my_canvas.create_line( 100 + self.decalage, 50, 100 + self.decalage, 100, fill="black")
         self.window3 = my_canvas.create_line( 200 + self.decalage, 50, 200 + self.decalage, 100, fill="black")
      else:
         self.window1 = my_canvas.create_line( 100 + self.decalage, 50, 100 + self.decalage, 100, fill="white")
         self.window2 = my_canvas.create_line( 200 + self.decalage, 50, 200 + self.decalage, 100, fill="white")
         self.window3 = my_canvas.create_line( 100 + self.decalage, 50, 201 + self.decalage, 50, fill="black")
      self.window_open = not self.window_open


   def move_door(self):
      if not self.door_open:
         my_canvas.itemconfig(self.door1, fill="black")
         my_canvas.itemconfig(self.door2, fill="white")
      else:
         my_canvas.itemconfig(self.door1, fill="white")
         my_canvas.itemconfig(self.door2, fill="black")
      self.door_open = not self.door_open

   def move_second_door(self):
      if not self.second_door_open:
         my_canvas.itemconfig(self.s_door1, fill="black")
         my_canvas.itemconfig(self.s_door2, fill="white")
      else:
         my_canvas.itemconfig(self.s_door1, fill="white")
         my_canvas.itemconfig(self.s_door2, fill="black")
      self.second_door_open = not self.second_door_open

   def jauge (self):
      ppm_mean = int(self.ppm/10 + 0.5) # starts at 500 ppm
      ppm_mean = max(min(300, ppm_mean), 0)  # limit number between 0 & 300 px equal to 3000 ppm

      my_canvas.coords( self.white, 70 + self.decalage, 140, 130 + self.decalage, 420 - ppm_mean)
      root.update()

   def ppm_func(self, corridor):
      global time_mutiplicator
      ppm_before = self.ppm

      if self.window_open and self.door_open:
         if self.ppm_start == 0:
            self.ppm_start = self.ppm
         self.t += 1 * time_mutiplicator
         self.ppm = (self.ppm_start * numpy.exp(-6.5 * self.t /60)) + (950 * (1 - numpy.exp(-6.5 * self.t /60)))

         ppm_modif = self.ppm - ( ppm_before + augmentation_ppm)
         ppm_modif = int((ppm_modif + 0.005)*100)/100

         if ppm_modif < 0:
            corridor.ppm_add(abs(ppm_modif))

      else:
         self.t = 0   # reset time
         self.ppm_start = 0
         self.ppm += augmentation_ppm   # 20ppm/min

         if self.window_open:
            self.ppm -= augmentation_ppm / 2

         if self.door_open:
            self.ppm -= augmentation_ppm / 2
            corridor.ppm_add(augmentation_ppm / 2)

         if self.ppm >= 3000:     # ppm limit
            self.ppm = 3000

      if self.second_door:
         door_ppm_exchanger(self.second_door_open, self.room_num)
      self.jauge()
      my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))

   def ppm_add(self, value):
      self.ppm += value
      print(f"Adding {value} to {self.room_num}")






class Corridor():
   def __init__(self, nb_room):
      self.decalage = nb_room * 400

      my_canvas.create_line( 50 , 650, 50 + self.decalage, 650, fill="red")
      my_canvas.create_line( 50 + self.decalage, 450, 50 + self.decalage, 650, fill="red")
      my_canvas.create_line( 50, 450, 50, 501, fill="red")
      my_canvas.create_line( 50, 600, 50, 650, fill="red")
      


      #  Door
      self.door_open = False
      self.door1 = my_canvas.create_line( 50, 600, 50, 500, fill="black")
      self.door2 = my_canvas.create_line( 50, 600, 150, 600, fill="white")
      tkinter.Button(root, text ="Open / Close door", command = self.move_door).place(x= 80, y= 520)



      self.ppm = 500
      self.display_ppm = my_canvas.create_text( 50 + (self.decalage / 2) , 550, anchor="center", text=self.ppm)

   def move_door(self):
      if not self.door_open:
         self.door1 = my_canvas.create_line( 50, 600, 50, 500, fill="white")
         self.door2 = my_canvas.create_line( 50, 600, 150, 600, fill="black")
      else:
         self.door1 = my_canvas.create_line( 50, 600, 50, 500, fill="black")
         self.door2 = my_canvas.create_line( 50, 600, 150, 600, fill="white")
      self.door_open = not self.door_open

   def ppm_add(self, add):
      self.ppm += add / 4
      my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))

   def ppm_func(self):
      if self.ppm == 1500:
         self.ppm = 1500
      else: 
         if self.door_open:
            if self.ppm > 700:
               self.ppm -= 20 * time_mutiplicator
            elif self.ppm < 700 and self.ppm > 690:
               self.ppm = 700
            my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))





my_canvas.create_line( 50 , 50, 50 , 450, fill="red")
for num in range(nb_room):
   room_list.append(Classroom(num))

corridor = Corridor(nb_room)


def room_update(room, corridor):
   while True:

      start = time.time()

      room.ppm_func(corridor)

      end = time.time()

      time.sleep(int(abs(0.01 - (end - start)) * 10000000) / 10000000)   # reload every 10 ms minus the execution times of the function rounded to 0.0000001 seconds

def corridor_update(corridor):
   while True:

      start = time.time()

      corridor.ppm_func()

      end = time.time()

      time.sleep(int(abs(0.01 - (end - start)) * 10000000) / 10000000)   # reload every 10 ms minus the execution times of the function rounded to 0.0000001 seconds


def launch_update_thread():
   for room in room_list:
      threading.Thread(target=room_update, args=(room, corridor, ) ).start()

threading.Thread(target=corridor_update, args=(corridor, ) ).start()
threading.Thread(target=launch_update_thread).start()



root.mainloop()