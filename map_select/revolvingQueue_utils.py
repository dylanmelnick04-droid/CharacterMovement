import pygame
import numpy as np

class RevolvingQueue:
    def __init__(self, surface, x_pos, y_pos, scale_const):
        self.surface = surface
        self.x = x_pos
        self.y = y_pos
        self.scale_x = scale_const
        self.scale_y = scale_const
        self.corners = None
        self.position = -1

    def draw(self, screen, sheared_surface, corners):
        screen.blit(self.surface, (self.x, self.y))

        if self.corners is not None:
            pygame.draw.polygon(
                screen,
                (34, 34, 34),
                self.corners + np.array([self.x, self.y]),
                2
            )


def shearImage(array, shear_x, shear_y):
    H, W = array.shape[:2]

    # 1. Shear matrix
    shear_matrix = np.array([[1, shear_x],
                             [shear_y, 1]])
    inv_shear = np.linalg.inv(shear_matrix)

    # 2. Original corners
    corners = np.array([
        [0, 0],
        [W, 0],
        [W, H],
        [0, H]
    ])

    # 3. Transform corners
    sheared_corners = corners @ shear_matrix.T

    min_x, min_y = sheared_corners.min(axis=0)
    max_x, max_y = sheared_corners.max(axis=0)

    sheared_corners -= [min_x, min_y]

    # 4. New image size
    new_W = int(np.ceil(max_x - min_x))
    new_H = int(np.ceil(max_y - min_y))

    # 5. Grid in new space
    xx, yy = np.meshgrid(np.arange(new_W), np.arange(new_H))
    coords = np.stack([xx + min_x, yy + min_y], axis=-1).reshape(-1, 2)

    # 6. Map back
    new_coords = coords @ inv_shear.T
    x_new = np.round(new_coords[:, 0]).astype(int)
    y_new = np.round(new_coords[:, 1]).astype(int)

    # 7. Valid mask
    valid = (
        (x_new >= 0) & (x_new < W) &
        (y_new >= 0) & (y_new < H)
    )

    # 8. Output image (parallelogram space)
    sheared_array = np.zeros((new_H, new_W, 3), dtype=array.dtype)

    flat = sheared_array.reshape(-1, 3)
    flat[valid] = array[y_new[valid], x_new[valid]]

    return sheared_array, sheared_corners


def shear_and_scale(image, SHEAR_X, SHEAR_Y, SCALE_INT):
    img_array = pygame.surfarray.array3d(image)
    img_array = np.transpose(img_array, (1, 0, 2))

    sheared_array, corners = shearImage(img_array, SHEAR_X, SHEAR_Y)
    sheared_surface = pygame.surfarray.make_surface(np.transpose(sheared_array, (1, 0, 2)))
    scaled_sheared = pygame.transform.scale(sheared_surface, (SCALE_INT, SCALE_INT))

    scale_x = SCALE_INT / sheared_surface.get_width()
    scale_y = SCALE_INT / sheared_surface.get_height()

    scaled_corners = corners * [scale_x, scale_y]

    return scaled_sheared, scaled_corners

def render_maps(screen, map_image_list, object_list, my_font, shiftDirection):
    # Clear previous objects
    object_list.clear()

    # Prepare a list for images by index
    image_list = [None] * 5  # indices 0-4

    # Populate images that are in range 0-4
    for map_item in map_image_list:
        idx = map_item["idx"]
        if 0 <= idx <= 4:
            image_list[idx] = map_item["image"]

    # Object positions and shear values
    object_positions = [
        (40, 220, 125, -0.18),   # idx 0
        (80, 200, 150, -0.1),    # idx 2
        (162.5, 190, 175, 0),     # idx 4
        (270, 200, 150, 0.1),    # idx 3
        (335, 220, 125, 0.18)   # idx 1
        
    ]
    centerPosition = 0
    for idx, img in enumerate(image_list):
        if img is not None:
            x, y, scale, shear = object_positions[idx]
            sheared_surface, corners = shear_and_scale(img, 0, shear, scale)
            sheared_surface.set_colorkey((0, 0, 0))

            obj = RevolvingQueue(sheared_surface, x, y, scale)
            obj.corners = corners
            obj.sheared_surface = sheared_surface
            obj.corners_for_draw = corners

            if object_positions[idx] == (162.5, 190, 175, 0):
                centerObject = obj
            else:
                object_list.append(obj)

    # Draw each object using **both arguments** as required
    if len(object_list) == 2:
        edgeCase = True
    else:
        edgeCase = False
    while object_list:
        if len(object_list) == 2:
            secondObject = object_list[shiftDirection]
        obj = object_list.pop(shiftDirection)
        obj.draw(screen, obj.sheared_surface, obj.corners_for_draw)

        if object_list:
            if len(object_list) == 2:
                secondObject = object_list[-1 if shiftDirection == 0 else 0]
            obj = object_list.pop(-1 if shiftDirection == 0 else 0)
            obj.draw(screen, obj.sheared_surface, obj.corners_for_draw)
    if edgeCase:
        secondObject.draw(screen, secondObject.sheared_surface, secondObject.corners_for_draw)
    centerObject.draw(screen, centerObject.sheared_surface, centerObject.corners_for_draw)
    
    # Render text for the center object (idx 2) if it exists
    center_map = next((m for m in map_image_list if m["idx"] == 2), None)
    if center_map:
        text_surface = my_font.render(center_map["name"], True, (0, 0, 0))
        screen.blit(text_surface, (200, 375))

def shift_left(map_image_list):
    if (map_image_list[0]["idx"] == 2):
        return
    for map in map_image_list:
        map["idx"] += 1

def shift_right(map_image_list):
    if (map_image_list[4]["idx"] == 2):
        return
    for map in map_image_list:
        map["idx"] -= 1