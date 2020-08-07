import optparse
import os

from PIL import Image


def main(file_input, initial_name, target_name):
    # First, we check names if we can actually glue them.
    check_for_names_correctness(initial_name, target_name)
    file, width, height = open_file(file_input)
    # Detect the amount of cuts.
    amount_of_cuts = len(initial_name)
    # Detect the cut height. Must be integer because division return float.
    cut_height = int(height / amount_of_cuts)
    # Path to folder to save temporary files.
    path_to_folder = os.path.dirname(file_input)
    # Get image paths for original image.
    image_paths = cut_image(file, height, width, cut_height, path_to_folder)
    # Get image paths in order, looking at target name.
    images_in_order = get_image_order(image_paths, initial_name, target_name)
    # Glue the images.
    glue_images(images_in_order, path_to_folder)
    # Delete all temporary files.
    clean_up(image_paths)


# Check if we can actually glue images based on names.
def check_for_names_correctness(initial_name, target_name):
    can_glue = True
    symbol_reason = ''

    # Check if all symbols in target name can be found in initial name.
    for x in target_name:
        if x not in initial_name and can_glue:
            can_glue = False
            symbol_reason = x
            break

    if not can_glue:
        raise Exception(f'Can\'t glue images because initial name {initial_name} and target name '
                        f'{target_name} could not be matched due to symbol \'{symbol_reason}\'')


def open_file(file):
    im = Image.open(file)
    width, height = im.size
    return im, width, height


def cut_image(image, height, width, cut_height, path):
    # Array for image paths.
    images_paths = []
    # Counter.
    k = 0
    for i in range(0, height, cut_height):
        # Creating a box to crop with.
        box = (0, i, width, i + cut_height)
        a = image.crop(box)
        # Saving file.
        path = f'{path}'"IMG-%s.png" % k
        a.save(os.path.join(path))
        images_paths.append(path)
        k += 1
    return images_paths


def get_image_order(image_paths, initial_name, target_name):
    # Initial = lev, target = vel. Therefore, indexes will be [2,1,0], image paths will follow.
    new_image_paths = []
    indexes = []

    for x in target_name:
        indexes.append(initial_name.find(x))

    for x in indexes:
        new_image_paths.append(image_paths[x])

    return new_image_paths


def glue_images(image_paths, path):
    # Opening images.
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))

    total_height = sum(heights)
    max_width = max(widths)

    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    # Glue the images.
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]

    path = f'{path}/result.jpg'

    # Save file.
    new_im.save(path)
    print(f'Image saved as {path}')


def clean_up(image_paths):
    # Delete all temporary files.
    for x in image_paths:
        os.remove(x)


parser = optparse.OptionParser()

parser.add_option('-p', '--path',
                  action="store", dest="path",
                  help="path to file")

parser.add_option('-i', '--initial_name',
                  action="store", dest="initial_name",
                  help="initial name")

parser.add_option('-t', '--target_name',
                  action="store", dest="target_name",
                  help="target name")

options, args = parser.parse_args()

main(options.path, options.initial_name, options.target_name)
