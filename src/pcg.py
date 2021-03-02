import numpy as np
import matplotlib.pyplot as plt
import random
import typing

from utility import HSV_to_RGB

#initialize blank map
#hue and value are set to 0, while saturation is set to 100
def init_map(res_X: int, res_Y: int) -> np.ndarray:
  map = np.full((res_Y, res_X, 3), 0.0, dtype=float) #contains HSV-values
  for y in range(res_Y):
    for x in range(res_X):
      map[y][x][1] = 100.0 #saturation set to 100%
      map[y][x][2] = 50.0  #set value to 50%
  return map


#calls all function which will in turn alter the map
def generate_map(res_X: int, res_Y: int) -> np.ndarray:
  map = init_map(res_X, res_Y)

  return map


#show generated map with pyplot
def show_map(map: np.ndarray) -> None:
  RGB_map = HSV_to_RGB(map)

  plt.imshow(RGB_map)
  plt.show()


#start of script
if __name__ == "__main__":
  try:
    res_X = 16 #TODO int(input("Width of to be generated map >> "))
    res_Y = 16 #TODO int(input("Height of to be generated map >> "))

    if res_X <= 0 and res_Y <= 0: #only positive (excl. 0) resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)
  
  show_map(generate_map(res_X, res_Y))