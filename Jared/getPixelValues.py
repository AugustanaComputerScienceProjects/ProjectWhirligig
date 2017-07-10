from PIL import Image
im = Image.open(r"S:\CLASS\CS\ProjectWhirligig\first_frames\large1_frame0001.png") #Can be many different formats.
pix = im.load()
print (im.size) #Get the width and hight of the image for iterating over
print (pix[560,525]) #Get the RGBA Value of the a pixel of an image

#pix[1,1] = value # Set the RGBA Value of the image (tuple)
#im.save(S:\CLASS\CS\ProjectWhirligig\first_frames) # Save the modified pixels as png

