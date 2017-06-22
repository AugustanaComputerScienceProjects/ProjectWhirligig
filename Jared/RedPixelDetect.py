import cv2

imageFileName = r'H:\Summer Research 2017\Whirligig Beetle pictures and videos\marked_frames\large1_frame0001_markedJH.png'
textFileName = imageFileName.replace('.png', '') + '.txt'

img = cv2.imread(imageFileName)

height, width, channels = img.shape

with open(textFileName, 'w') as fout:
    counter = 0
    for y in reversed(range(height)):
        for x in range(width):
            if (img.item(y,x,2) ==237) and (img.item(y,x,1) ==28) and (img.item(y,x,0) ==36):
                fout.write(str(x) + ' ' + str(y) + '\n')
                counter +=1


print("# of red pixels: ", counter)