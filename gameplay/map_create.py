import pygame
import boundary

def create_map(boundary_list, MAP, block_types, arena):
    image = block_types[0]
    match MAP:
        case 'map1':
            image = block_types[0]
            for i in range(16):
                b = boundary.Boundary(50 + 25 * i, 450, image)
                boundary_list.append(b)
            
            for i in range (3):
                b = boundary.Boundary(100 + 25 * i, 375, image)
                boundary_list.append(b)

            for i in range (6):
                b = boundary.Boundary(225 + 25 * i, 375, image)
                boundary_list.append(b)
            
            for i in range (2):
                b = boundary.Boundary(375 + 25 * i, 300, image)
                boundary_list.append(b)

            for i in range (4):
                b = boundary.Boundary(150 + 25 * i, 225, image)
                boundary_list.append(b)
            
            for i in range (2):
                b = boundary.Boundary(275 + 125 * i, 150, image)
                boundary_list.append(b)
            
            if arena == True:
                makeArena(boundary_list, MAP, image)
    
        case 'map2':
            image = block_types[0]

        case 'map3':
            image = block_types[1]
            for i in range(10):
                b = boundary.Boundary(125 + 25 * i, 450, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(100, 425 - 25 * i, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(375, 425 - 25 * i, image)
                boundary_list.append(b)
        case 'map4':
            image = block_types[1]
            # layer 1
            for i in range(2):
                b = boundary.Boundary(125 + 25 * i, 450, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(225 + 25 * i, 450, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(350 + 25 * i, 450, image)
                boundary_list.append(b)
            # layer 2
            for i in range(2):
                b = boundary.Boundary(0 + 25 * i, 375, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(150 + 25 * i, 375, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(300 + 25 * i, 375, image)
                boundary_list.append(b)
            
            # layer 3
            for i in range(2):
                b = boundary.Boundary(100 + 25 * i, 300, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(100 + 25 * i, 300, image)
                boundary_list.append(b)
            for i in range(2):
                b = boundary.Boundary(375 + 25 * i, 300, image)
                boundary_list.append(b)
            
            #layer 4
                b = boundary.Boundary(75, 225, image)
                boundary_list.append(b)
                b = boundary.Boundary(100, 200, image)
                boundary_list.append(b)
                b = boundary.Boundary(175, 225, image)
                boundary_list.append(b)
                b = boundary.Boundary(225, 225, image)
                boundary_list.append(b)
                b = boundary.Boundary(275, 200, image)
                boundary_list.append(b)
                b = boundary.Boundary(375, 225, image)
                boundary_list.append(b)
                #b = boundary.Boundary(350, 250, image)
                #boundary_list.append(b)
                b = boundary.Boundary(125, 150, image)
                boundary_list.append(b)
                b = boundary.Boundary(125, 275, image)
                boundary_list.append(b)
                b = boundary.Boundary(150, 200, image)
                boundary_list.append(b)
                b = boundary.Boundary(25, 125, image)
                boundary_list.append(b)
                b = boundary.Boundary(325, 100, image)
                boundary_list.append(b)
                b = boundary.Boundary(100, 50, image)
                boundary_list.append(b)
                b = boundary.Boundary(375, 75, image)
                boundary_list.append(b)
                b = boundary.Boundary(200, 25, image)
                boundary_list.append(b)

    if arena == True or MAP == 'map2':
        makeArena(boundary_list, MAP, image)


def makeArena(boundary_list, MAP, block_image):
    # ground
    for i in range (20):
        b = boundary.Boundary(25 * i, 475, block_image)
        boundary_list.append(b)    

    # left wall
    for i in range (19):
        b = boundary.Boundary(0, 25 * i, block_image)
        boundary_list.append(b)
    
    # right wall
    for i in range (19):
        b = boundary.Boundary(475, 25 * i, block_image)
        boundary_list.append(b)
    
    # top
    for i in range (18):
        b = boundary.Boundary(25 + 25 * i, 0, block_image)
        boundary_list.append(b)
    return