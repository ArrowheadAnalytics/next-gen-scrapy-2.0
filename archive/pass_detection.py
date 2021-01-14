"""
Authors: Sarah Mallepalle and Kostas Pelechrinis (updated by Ethan Douglas to work in Python 3)
For every pass chart image in 'Cleaned_Pass_Charts', extract the locations of complete passes, 
incomplete passes, interceptions, and touchdowns relative to the line of scrimmage.
"""

import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from collections import Counter
import pandas as pd
import math
import os
import scipy.misc


def map_pass_locations(centers, col, pass_type, n_empty = 0):
    """
    Function to map pixel location of passes to real field location of passes,
    with the y-axis at the center of the field, and the x-axis at the line of scrimmage.
    All images show either 55 yards or 75 yards in front of the line of scrimmage,
    10 yards behind the line of scrimmage, and a standard field width of 53.33 yards.
    
    Input:
        centers: list of pass locations in pixels
        col: width of image from which the pass locations were extracted
        pass_type: "COMPLETE", "INCOMPLETE", "INTERCEPTION", or "TOUCHDOWN"
    Return:
        pass_locations: Pandas DataFrame of all pass locations on the field and pass type
    """

    col_names = ["pass_type", "x", "y"]
    pass_locations = pd.DataFrame(columns = col_names)

    if ((len(centers) == 0) and (n_empty == 0)): return pass_locations

    sideline = 40 # pixels
    width = 53.33 # standard width of football field
    center_x = col/2

    if col > 1370:
        _75_yd_line = 0
        LOS = 596

        _1_yd_x = float(col - sideline*2)/width
        _1_yd_y = float(LOS - _75_yd_line)/75

    else:
        _55_yd_line = 5
        LOS = 572
        _1_yd_x = float(col - sideline*2)/width
        _1_yd_y = float(LOS - _55_yd_line)/55

    for c in centers:
        y = c[0]
        x = c[1]
        y_loc = float(LOS - y)/_1_yd_y
        x_loc = float(x - center_x)/_1_yd_x
        df = pd.DataFrame([[pass_type, x_loc, y_loc]], columns = col_names)
        pass_locations = pass_locations.append(df, ignore_index=True)

    if (n_empty != 0):
        df = pd.DataFrame([[pass_type, None, None]]*n_empty, 
            columns = col_names)
        pass_locations = pass_locations.append(df, ignore_index=True)
    return pass_locations

def completions(image, n):
    """
    Function to obtain the locations of the complete passes from the image
    of the pass chart using k-means.
    
    Input: 
        image: image from the folder 'Cleaned_Pass_Charts'
        n: number of incompletions, from the corresponding data of the image
    Return:
        call to map_pass_locations:
            centers: list of pass locations in pixels
            col: width of image from which the pass locations were extracted
            pass_type: "COMPLETE"
    """

    image = cv2.imread(image)
    row, col = image.shape[0:2]

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of green color in HSV
    lower_green = np.array([40,100, 100])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    x = np.where(res != 0)[0]
    y = np.where(res != 0)[1]
    pairs = list(zip(x,y))
    X = list(map(list, pairs))

    kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
    centers = kmeans.cluster_centers_

    return map_pass_locations(centers, col, "COMPLETE")

def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)**2

def dist2(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def incompletions(image, n):
    """
    Function to obtain the locations of the incomplete passes from the image
    of the pass chart using k-means, and DBSCAN to account for discrepancies
    in given number of incompletions from the data vs. number of incompletions
    shown on the field.
    
    Input: 
        image: image from the folder 'Cleaned_Pass_Charts'
        n: number of incompletions, from the corresponding data of the image
    Return:
        call to map_pass_locations:
            centers: list of pass locations in pixels
            col: width of image from which the pass locations were extracted
            pass_type: "INCOMPLETE"
    """

    image = cv2.imread(image)
    row, col = image.shape[0:2]

    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])

    mask = cv2.inRange(image, lower_white, upper_white)
    res = cv2.bitwise_and(image, image, mask=mask)
    res = cv2.fastNlMeansDenoisingColored(res)

    x = np.where(res != 0)[0]
    y = np.where(res != 0)[1]
    pairs = list(zip(x,y))
    X = np.array(list(map(list, pairs)))

    kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
    centers = kmeans.cluster_centers_

    wcvs = np.zeros(n)
    for i in range(n):
        y = int(round(centers[i][0]))
        x = int(round(centers[i][1]))
        c_points = X[np.where(kmeans.labels_ == i)]
        wcv = sum([dist(x, y, p[1], p[0]) for p in c_points])
        wcvs[i] = wcv/len(c_points)

    mean_ = np.mean(wcvs)
    median_ = np.median(wcvs)

    center = centers[centers[:,1].argsort()]
    dists = np.zeros(n-1)
    for j in range(n-1):
        y1 = center[j][0]
        x1 = center[j][1]
        y2 = center[j+1][0]
        x2 = center[j+1][1]

        dists[j] = dist2(x1, y1, x2, y2)

    close_i = np.argwhere(dists < 15)
    new_n = n
    for i in close_i:
        c1 = np.where(centers == center[i])[0][0]
        c2 = np.where(centers == center[i+1])[0][0]
        if (mean_ < 30 and median_ < 30 and wcvs[c1] + wcvs[c2] < 45):
            new_n -= 1
        elif (wcvs[c1] + wcvs[c2] < 50):
            new_n -= 1

    kmeans = KMeans(n_clusters=new_n, random_state=0).fit(X)
    centers = kmeans.cluster_centers_
    n_empty = n - new_n

    return map_pass_locations(centers, col, "INCOMPLETE", n_empty)
 
def interceptions(image, n):
    """
    Function to obtain the locations of the intercepted passes from the image
    of the pass chart using k-means.
    
    Input: 
        image: image from the folder 'Cleaned_Pass_Charts'
        n: number of interceptions, from the corresponding data of the image
    Return:
        call to map_pass_locations:
            centers: list of pass locations in pixels
            col: width of image from which the pass locations were extracted
            pass_type: "INTERCEPTION"
    """

    image = cv2.imread(image)
    row, col = image.shape[0:2]

    # define range of red 
    lower_red = np.array([0, 0, 150])
    upper_red = np.array([30, 30, 255])

    mask = cv2.inRange(image, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)
    res = cv2.fastNlMeansDenoisingColored(res, h = 10)

    x = np.where(res != 0)[0]
    y = np.where(res != 0)[1]
    pairs = list(zip(x,y))

    if (len(pairs) == 0): 
        return map_pass_locations([], col, "INTERCEPTION", n)

    X = list(map(list, pairs))

    kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
    centers = kmeans.cluster_centers_

    return map_pass_locations(centers, col, "INTERCEPTION")

def touchdowns(image, n):
    """
    Function to obtain the locations of the touchdown passes from the image
    of the pass chart using k-means, and DBSCAN to account for difficulties in 
    extracting touchdown passes, since they have the are the same color as both the line of 
    scrimmage and the attached touchdown trajectory lines. 
    
    Input: 
        image: image from the folder 'Cleaned_Pass_Charts'
        n: number of toucndowns, from the corresponding data of the image
    Return:
        call to map_pass_locations:
            centers: list of pass locations in pixels
            col: width of image from which the pass locations were extracted
            pass_type: "TOUCHDOWN"
    """

    im = Image.open(image)
    pix = im.load()
    col, row = im.size

    img = Image.new('RGB', (col, row), 'black') 
    p = img.load() 

    for i in range(col):
        for j in range(row):
            r = pix[i,j][0]
            g = pix[i,j][1]
            b = pix[i,j][2]
            if (col < 1370) and (j < row-105) and (j > row-111):
                if (b > 2*g) and (b > 60): 
                    p[i,j] = (0,0,0)
            elif (col > 1370) and (j < row-81) and (j > row-86):
                if (b > 2*g) and (b > 60): 
                    p[i,j] = (0,0,0)
            else: p[i,j] = pix[i,j]
            r = p[i,j][0]
            g = p[i,j][1]
            b = p[i,j][2]
            f = ((r-20)**2 + (g-80)**2+ (b-200)**2)**0.5
            if f < 32 and b > 100: 
                p[i,j] = (255, 255,0)

    scipy.misc.imsave('temp.jpg', img)
    imag = cv2.imread('temp.jpg')
    os.remove('temp.jpg')
    hsv = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)
    lower = np.array([20,100, 100])
    upper = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(imag, imag, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_HSV2RGB)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    res = cv2.fastNlMeansDenoising(res, h = 10)
    x = np.where(res != 0)[0]
    y = np.where(res != 0)[1]
    pairs = list(zip(x,y))
    X = list(map(list, pairs))

    if (len(pairs) != 0):
        db = DBSCAN(eps=10, min_samples=n).fit(X)
        labels = db.labels_
        coords = pd.DataFrame([x, y, labels]).T
        coords.columns = ['x', 'y','label']
        clusters = Counter(labels).most_common(n)
        td_labels = np.array([clust[0] for clust in clusters])
        km_coords = coords.loc[coords['label'].isin(td_labels)]
        km = list(map(list, zip(km_coords.iloc[:,0], km_coords.iloc[:,1])))

        kmeans = KMeans(n_clusters=n, random_state=0).fit(km)
        centers = kmeans.cluster_centers_ 

        return map_pass_locations(centers, col, "TOUCHDOWN")
        
    else:
        return map_pass_locations([], col, "TOUCHDOWN", n)



