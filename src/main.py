import matplotlib.pyplot as plt
import numpy as np

from PCG import Map
from utility import HSV_to_RGB

# Show generated map with pyplot
def show_map(map: np.ndarray) -> None:
  print("Converting HSV to RGB ...")
  RGB_map = HSV_to_RGB(map)
  plt.imshow(RGB_map)
  plt.axis("off")
  plt.show()

# Start of script
if __name__ == "__main__":
  print("=== PROCEDURAL CONTENT GENERATION ===")
  try:
    res_X = 1280 #TODO int(input("Width of to be generated map >> "))
    res_Y = 720  #TODO int(input("Height of to be generated map >> "))

    if res_X <= 0 and res_Y <= 0: # Only positive (excl. 0) resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)

  M = Map(res_X, res_Y, 42)  # TODO: remove when handing in assignment
  M.generate()     # Generate the map with the procedures
  show_map(M.get_map())  # Show the map with pyplot