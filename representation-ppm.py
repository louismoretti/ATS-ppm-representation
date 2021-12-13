import tkinter
import numpy
import threading
import time



num_room = int(input("Combien veut-tu de classe ?"))
room_list = []

root = tkinter.Tk()
root.title('Représentation ppm')
root.geometry(f"{100 + num_room * 400}x500")

background = 'white'
canvas_width = 100 + num_room * 400
canvas_height = 500
my_canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height, bg=background)
my_canvas.pack()

time_mutiplicator = 0.05




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
      tkinter.Button(root, text ="Open / Close door", command = self.open_door).place(x= 300 + self.decalage, y= 460)

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


   def open_door(self):
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

   def ppm_func(self):
      global time_mutiplicator

      if self.window_open and self.door_open:
         if self.ppm_start == 0:
            self.ppm_start = self.ppm
         self.t += 1 * time_mutiplicator
         self.ppm = (self.ppm_start * numpy.exp(-6.5 * self.t /60)) + (950 * (1 - numpy.exp(-6.5 * self.t /60)))

      else:
         self.t = 0   # reset time
         self.ppm_start = 0
         self.ppm += 29 * time_mutiplicator   # 20ppm/min

         if self.window_open or self.door_open:
            self.ppm -= 10 * time_mutiplicator

         if self.ppm >= 3000:     # ppm limit
            self.ppm = 3000

      self.jauge()
      my_canvas.itemconfig(self.display_ppm, text= int(self.ppm))

















for num in range(num_room):
   room_list.append(Classroom(num))



def update(room):
   while True:

      start = time.time()

      room.ppm_func()

      end = time.time()

      time.sleep(int(abs(0.01 - (end - start)) * 10000000) / 10000000 )   # reload every 10 ms minus the execution times of the function rounded to 0.0000001 seconds


def launch_update_thread():
   for room in room_list:
      threading.Thread(target=update, args=(room,) ).start()

threading.Thread(target=launch_update_thread).start()



root.mainloop()