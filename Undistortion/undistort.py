import cv2
import numpy as np

def loadUndistortedImage(fileName):
    # load image
    image = cv2.imread(fileName)
    #print(image)

    # set distortion coeff and intrinsic camera matrix (focal length, centerpoint offset, x-y skew)
    cameraMatrix = np.array([[894.96803896,0,470.38713516],[0,901.32629374,922.41232898], [0,0,1]])
    distCoeffs = np.array([[-0.340671222,0.110426603,-.000867987573,0.000189669273,-0.0160049526]])

    # setup enlargement and offset for new image
    y_shift = 60    #experiment with
    x_shift = 70    #experiment with    
    imageShape = image.shape  #image.size
    print(imageShape)
    imageSize = (int(imageShape[0])+2*y_shift, int(imageShape[1])+2*x_shift)
    print(imageSize)

    # create a new camera matrix with the principal point offest according to the offset above
    newCameraMatrix, validPixROI = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize,
    1)
    #newCameraMatrix = cv2.getDefaultNewCameraMatrix(cameraMatrix, imageSize, True) # imageSize, True

    # create undistortion maps
    R = np.array([[1,0,0],[0,1,0],[0,0,1]])
    map1, map2 = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, R, newCameraMatrix, imageSize,
    cv2.CV_16SC2)

    # remap
    outputImage = cv2.remap(image, map1, map2, INTER_LINEAR)
    #save output image as file with "FIX" appened to name - only works with .jpg files at the moment
    index = filename.find('.jpg')
    fixed_filename = filename[:index] +'_undistorted'+fileName[index:]
    cv2.imwrite(fixed_filename, outputImage)
    cv2.imshow('fix_img',outputImage)
    cv2.imwrite('coords/T1AD-Undis.png', outputImage)
    cv2.waitKey(0)
    return

#Undistort the images, then save the restored images
loadUndistortedImage(r'C:\Users\User\OneDrive - g.bracu.ac.bd\Documents\Codes\KIBO\coords\T1AD-mes1.png')
