import matplotlib.pyplot as plt
import numpy as np

from PCG import Map
from utility import HSV_to_RGB

# Show generated map with pyplot
def show_map(map: np.ndarray, output: str) -> None:
  print("Converting HSV to RGB ...")
  RGB_map = HSV_to_RGB(map)
  plt.imshow(np.clip(RGB_map, 0, 1))
  plt.axis("off")
  plt.savefig(output, bbox_inches="tight")  # Save image to file
  print("\nMap saved to", output)

# Start of script
if __name__ == "__main__":
  print("=== PROCEDURAL CONTENT GENERATION ===")
  try:
    print("Both resolutions are constrained by the perlin noise (see README)\n")
    res_X = int(input("Width of to be generated map >> "))
    res_Y = int(input("Height of to be generated map >> "))
    output = input("Output-file where generated map is saved >> ")

    if res_X <= 0 and res_Y <= 0: # Only positive (excl. 0) resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)

  print("\n")
  M = Map(res_X, res_Y)
  M.generate()                   # Generate the map with the procedures
  show_map(M.get_map(), output)  # Show the map with pyplot
