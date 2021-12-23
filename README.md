# HandwritingVideoAnimation
 A python project for making text write-in effects.
 
 # Dependencies:
 * Python 3.9.6 (Just the version I used, I don't believe I used many version specific features, but better safe than sorry)
 * OpenCV
 * Numpy

This project may be terrible for your use case. Please understand that this was done out of spite since I realized there were simpler solutions for if I just wanted animated text of any font on screen. https://www.calligrapher.ai/ worked for my use case and is better than this, but if you have a specific font you wish to use, this project may be worth it. There are configurations that need to be handled internally through editing the raidus for each path if your font is big. A full UI is probably impossible since I am using OpenCV. I may update this in the future if I feel like it. gl;hf

Controls:
q - quit

e - render (Your image will stay on screen and may appear to not respond, this is normal as OpenCV's VideoWriter can be slow some times)

spacebar - Split (By default, key points are lerp'd between at a speed ralative to the difference in angle between the last pair of keyframes (this allows us to simulate pen sliding speed). Hitting spacebar will prevent the next point from being connected)
 - Keypoint connectivity is visualized by a line going from one point to the next.
 
left click - Insert a keypoint

right click - Revert last step

ISSUES:
Currently, the way we get a background is by selectin the top left corner pixel's BGR value. This means if you center your text at the top right corner, it may use the font color.
Currently, this application is slow (5-10 seconds to render the text "Insert Text Here") I have yet to test it on longer cases, but for paragraphs I imagine it would take forever to do anyways.
Currently, to use this, you must have your image in the same directory as the script and have it named FirstPart.png I will change this later, I just want to finish the project this application was made for first (a video project) before I actually finish or polish this project.

