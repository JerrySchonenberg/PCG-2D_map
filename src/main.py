import matplotlib.pyplot as plt
import numpy as np

from PCG import Map
from utility import HSV_to_RGB

# Show generated map with pyplot
def show_map(map: np.ndarray) -> None:
  RGB_map = HSV_to_RGB(map)
  plt.imshow(RGB_map)
  plt.axis("off")
  plt.show()

# Start of script
if __name__ == "__main__":
  try:
    res_X = int(input("Width of to be generated map >> "))
    res_Y = int(input("Height of to be generated map >> "))

    if res_X <= 0 and res_Y <= 0: # Only positive (excl. 0) resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)

  M = Map(res_X, res_Y)
  M.generate()     # Generate the map with the procedures
  show_map(M.get_map())  # Show the map with pyplot