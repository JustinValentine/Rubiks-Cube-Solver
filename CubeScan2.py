import cv2
import numpy as np

def KMeanCluster(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = img.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    # define stopping criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)
    # number of clusters (K)
    k = 1
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    
    
    # convert back to 8 bit values
    centers = np.uint8(centers)

    # flatten the labels array
    labels = labels.flatten()
    # convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]
    # reshape back to the original image dimension
    segmented_image = segmented_image.reshape(img.shape)
    # show the image
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)
    print(centers)
    cv2.imshow('test', segmented_image)
    cv2.imshow('test2', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return centers.tolist()

def ClassifyColor(rgb):
    colors = {"Green": (0, 255, 0),
              "white" : (255,255,255),
              "blue": (0, 0, 255),
              "yellow" : (0,255,0),
              "orange": (255, 161, 0),
              "red" : (255,0,0),
              }
    pass

def DrawGrid(cube, size, face, img):
    height, width, channels = img.shape
    faces = ['green', 'white', 'blue', 'yellow', 'orange', 'red']
    cellSize = int(height*0.7)//size
    Xoffset, Yoffset = int(width//2 - cellSize * size/2),int(height//2 - cellSize * size/2)

    font, title = cv2.FONT_HERSHEY_DUPLEX, 'Scan the ' + faces[face] + ' face'
    cv2.rectangle(img, (Xoffset, 0), 
                  (Xoffset+cellSize*(size), 60), (255,255,255), -1)

    cv2.putText(img, title, (width//2-180,40), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    colors = []

    for i in range(size):
        for j in range(size):
            crop_img = img[Yoffset+i*cellSize:Yoffset+(i+1)*cellSize, 
                           Xoffset+j*cellSize:Xoffset+(j+1)*cellSize] 

            RGB = KMeanCluster(crop_img)[0]
            print(RGB)
            colors.append(RGB)

            cv2.rectangle(img, 
                         (Xoffset+j*cellSize,Yoffset+i*cellSize), 
                         (Xoffset+(j+1)*cellSize,Yoffset+(i+1)*cellSize), 
                         (0,0,0), 6)

    for i in range(size):
        for j in range(size):
            cv2.rectangle(img, 
                         (Xoffset+j*cellSize,Yoffset+i*cellSize), 
                         (Xoffset+(j+1)*cellSize,Yoffset+(i+1)*cellSize), 
                         (0,0,0), 6)


def main():
    cap = cv2.VideoCapture(1)
    KeysPressed, CubeSizeGet, DoDrawGrid = [], False, False

    while True:
        ret, img = cap.read()
        k = cv2.waitKey(33)

        if k == 27: # esc to quit
            break 

        elif k == 127 and len(KeysPressed) != 0: # Backspace is pressed
            KeysPressed.pop()

        elif k == 13 and len(KeysPressed) != 0: # Enter is pressed 
            CubeSizeGet,DoDrawGrid = True, True
            size = int(''.join(KeysPressed))
            cube = [[[6] * size for _ in range(size)] for i in range(6)]
            
        elif k in range(48,58): # Number is pressed
            KeysPressed.append(str(k%48))

        if CubeSizeGet == False:
            font, title = cv2.FONT_HERSHEY_DUPLEX, 'Enter Cube Size: '+''.join(KeysPressed)
            cv2.rectangle(img, (0, 0), (35*len(title), 60), (255,255,255), -1)
            cv2.putText(img, title, (10,50), font, 2, (0, 0, 0), 2, cv2.LINE_AA)

        elif DoDrawGrid == True:
            DrawGrid(cube, size, 0, img)

        cv2.imshow("Scanning Cube", img)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()