import tkinter
import numpy
import threading
import time



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




class Classroom():
   def __init__(self, room_num):

      self.decalage = room_num * 400

      # Base classroom
      my_canvas.create_line( 50 + self.decalage, 50, 50 + self.decalage, 450, fill="red")
      my_canvas.create_line( 450 + self.decalage, 50, 450 + self.decalage, 450, fill="red")
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
         self.door1 = my_canvas.create_line( 300 + self.decalage, 450, 400 + self.decalage, 450, fill="white")
         self.door2 = my_canvas.create_line( 300 + self.decalage, 450, 300 + self.decalage, 350, fill="black")
      else:
         self.door1 = my_canvas.create_line( 300 + self.decalage, 450, 300 + self.decalage, 350, fill="white")
         self.door2 = my_canvas.create_line( 300 + self.decalage, 450, 400 + self.decalage, 450, fill="black")
      self.door_open = not self.door_open


   def jauge (self):
      ppm_mean = int( self.ppm/10 + 0.5) # starts at 500 ppm
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

      self.jauge()
      my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))







class Corridor():
   def __init__(self, nb_room):
      self.decalage = nb_room * 400

      my_canvas.create_line( 50 , 650, 50 + self.decalage, 650, fill="red")
      my_canvas.create_line( 50 + self.decalage, 450, 50 + self.decalage, 650, fill="red")
      my_canvas.create_line( 50, 450, 50, 501, fill="red")
      my_canvas.create_line( 50, 600, 50, 650, fill="red")
      


      #  Door
      self.door_open_c = False
      self.door1_c = my_canvas.create_line( 50, 600, 50, 500, fill="black")
      self.door2_c = my_canvas.create_line( 50, 600, 150, 600, fill="white")
      tkinter.Button(root, text ="Open / Close door", command = self.move_door_c).place(x= 80, y= 520)



      self.ppm = 500
      self.display_ppm = my_canvas.create_text( 50 + (self.decalage / 2) , 550, anchor="center", text=self.ppm)

   def move_door_c(self):
      if not self.door_open_c:
         self.door1_c = my_canvas.create_line( 50, 600, 50, 500, fill="white")
         self.door2_c = my_canvas.create_line( 50, 600, 150, 600, fill="black")
      else:
         self.door1_c = my_canvas.create_line( 50, 600, 50, 500, fill="black")
         self.door2_c = my_canvas.create_line( 50, 600, 150, 600, fill="white")
      self.door_open_c = not self.door_open_c

   def ppm_add(self, add):
      self.ppm += add / 4
      my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))

   def ppm_func_c(self):
      if self.door_open_c:
         if self.ppm > 700:
            self.ppm -= 20 * time_mutiplicator
         elif self.ppm < 700 and self.ppm > 690:
            self.ppm = 700
         my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))






for num in range(nb_room):
   room_list.append(Classroom(num))

corridor = Corridor(nb_room)


def room_update(room, corridor):
   while True:

      start = time.time()

      room.ppm_func(corridor)

      end = time.time()

      time.sleep(int(abs(0.01 - (end - start)) * 10000000) / 10000000 )   # reload every 10 ms minus the execution times of the function rounded to 0.0000001 seconds

def corridor_update(corridor):
   while True:

      start = time.time()

      corridor.ppm_func_c()

      end = time.time()

      time.sleep(int(abs(0.01 - (end - start)) * 10000000) / 10000000 )   # reload every 10 ms minus the execution times of the function rounded to 0.0000001 seconds


def launch_update_thread():
   for room in room_list:
      threading.Thread(target=room_update, args=(room, corridor, ) ).start()

threading.Thread(target=corridor_update, args=(corridor, ) ).start()
threading.Thread(target=launch_update_thread).start()



root.mainloop()