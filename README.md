# Procedural Content Generation
### Jerry Schonenberg (s2041022) | 05-03-2021
##### Modern Game AI Algorithms - Assignment 1
This project contains the code for the first assignment of Modern Game AI Algorithms, where a 2D-map has to be generated with procedures which represents a landscape. HSV-values are used for the pixels such that the Hue and Saturation represent the biome and the Value represents the height.

The landscape consists of: relief, water, beaches, 5 biomes, vegetation, villages and roads. The 5 biomes are: `GRASS`, `SAND`, `SAVANNAH`, `JUNGLE` and `MYCELLIUM`. `MYCELLIUM` is taken from the game [Minecraft](https://minecraft.gamepedia.com/Mushroom_Fields), it has a purple ground and brown/red mushrooms. Since the Value-component is reserved for relief, each biome is defined with a Hue and Saturation. Please note that the Hue must be _unique_ for every biome.

## Contents

*   [Generating a landscape](#landscape)
*   [Requirements](#requirements)
*   [Usage](#usage)
*   [Examples](#examples)
*   [Hierarchy](#index)

## Generating a landscape <div id="landscape"></div>
The components of the landscape are generated with the following steps:
1. _Initialize the map_; fill the map with `GRASS` blocks.
2. _Generate relief_; first add relief to every row of the map, then smoothen the relief along the columns. The setting `RELIEF_FACTOR` determines how much relief there can be between two pixels. Consequently, light and dark pixels represent high and low points respectively.
3. _Add biomes to the map_; for every pixel is a probability to become the starting point of a new biome. This probability is defined with the setting `P_BIOME`. Moreover, the probability for every possible biome to be picked is equal.
4. _Add water_; every pixel which has a Value <= `WATER_THRESHOLD` becomes water.
5. _Add beaches surrounding the water_.
6. _Add plants to the biomes_; trees, bushes, cacti and mushrooms (exclusively to `MYCELLIUM`) are added to the landscape. The probability for vegetation to spawn on a pixel is denoted by `P_PLANT`. Then, based on the biome of the pixel, the type of vegetation is determined. Moreover, for cacti the probability to spawn is lower: there is only `P_CACTI` probability that a cacti gets generated after it is decided that a plant should be generated.
7. _Add villages to the landscape_; for every pixel is a probability `P_VILLAGE` that it becomes the origin of a village. Then, if this is case, in a radius of `SIZE_VILLAGE_X` and `SIZE_VILLAGE_Y`, for every pixel is determined whether it becomes a house (probability is `P_HOUSE`). The origin of the village is saved for later. Villages can only generate in or nearby the `GRASS` biome and not on water.
8. _Connect (some of) the villages with roads_; as mentioned in the previous step, the origin of every village is saved. Here, these origins are connected by road with a probability `P_ROAD`. Thereby, if the distance (Euclidian distance) between these origins is larger than `MAX_DIST`, then no road is generated. Then, with the use of the Euclidian distance, the shortest path between the two origins is generated.

The steps mention various settings and probabilities; these are defined in `settings.py` with their definition described. There are also definitions regarding the color of biomes, houses and roads. The current settings are finetuned for a resolution of 128x64, so the results may be worse with different resolutions when leaving the settings untouched (see [example](/img/1024.png)).

## Requirements <div id="requirements"></div>
* Python (tested with v3.8)
* Matplotlib (tested with v3.3.3), only for converting the map into an image
* Numpy (tested with v1.18.5)
* `settings.py` and `utility.py`

## Usage <div id="usage"></div>
In order to generate a landscape, simply run the following command:
```
python3 main.py
```
After this, the script asks for the horizontal and vertical resolution of the map. Then the script will generate the map and show it via pyplot.

It is also possible to import `PCG.py` (which contains the class with which the map is generated) along with `utility.py` and `settings.py`. To create a new class instance of `Map` and generate a new map, simply use the following code:
```
M = Map(res_X, res_Y, seed)
M.generate()
map = M.get_map()
```
This will return the map in HSV-format. If you need the map in RGB-format, simply use the function `HSV_to_RGB` from `utility.py` in order to convert the map to RGB. Note: the seed for creating a `Map` instance is optional and mainly used for debug purposes.


## Examples <div id="examples"></div>
The directory `img` contains multiple examples of generated landscapes. All examples are with a resolution of 128x64, with the exception of `1024.png`, which has a resolution of 1024x1024 and illustrates that the settings must be finetuned in order to get realistic landscapes at different resolutions. Moreover, the directory also contains a subdirectory in which the effect of every step is illustrated with a random seed of 42.

One example landscape (128x64) is given below:
![Example landscape](/img/example1.png)


## Hierarchy <div id="index"></div>
Here, an overview of all files of the project is given:
```
project/
├── README.md
├── report.pdf
├── img
|   ├── progression_seed42
|   |   ├── 1_relief.png
|   |   ├── 2_biomes.png
|   |   ├── 3_water.png
|   |   ├── 4_beaches.png
|   |   ├── 5_vegetation.png
|   |   └── 6_village.png
|   ├── 1024.png
|   ├── example1.png
|   ├── example2.png
|   ├── example3.png
|   ├── example4.png
│   └── example5.png
└── src
    ├── main.py
    ├── PCG.py
    ├── settings.py
    └── utility.py
```
