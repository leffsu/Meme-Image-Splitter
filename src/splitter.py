import optparse
import os

from PIL import Image


def main(file_input, initial_name, target_name, orientation):
    # First, we check names if we can actually glue them. 
    check_for_names_correctness(initial_name, target_name)
    file, width, height = open_file(file_input)
    # Detect the amount of cuts.
    amount_of_cuts = len(initial_name)
    cut_length = 0
    # Detect the cut height. Must be integer because division return float. 
    if orientation is 'v':
        cut_length = int(height / amount_of_cuts)
    else:
        cut_length = int(width / amount_of_cuts)
    # Path to folder to save temporary files.
    path_to_folder = os.path.dirname(file_input)
    # Get image paths for original image.
    image_paths = cut_image(file, height, width, cut_length, path_to_folder, orientation)
    # Get image paths in order, looking at target name.
    images_in_order = get_image_order(image_paths, initial_name, target_name)
    # Glue the images.
    glue_images(images_in_order, path_to_folder, orientation)
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


def cut_image(image, height, width, cut_height, path, orientation):
    # Array for image paths.
    images_paths = []
    # Counter.
    k = 0
    if orientation is 'v':
        for i in range(0, height, cut_height):
            # Creating a box to crop with.
            box = (0, i, width, i + cut_height)
            a = image.crop(box)
            # Saving file.
            path = f'{path}'"IMG-%s.png" % k
            a.save(os.path.join(path))
            images_paths.append(path)
            k += 1
    else:
        for i in range(0, width, cut_height):
            # Creating a box to crop with.
            box = (i, 0, i + cut_height, height)
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


def glue_images(image_paths, path, orientation):
    # Opening images.
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))

    offset = 0
    # Glue the images.
    if orientation is 'v':
        new_im = Image.new('RGB', (max(widths), sum(heights)))
        for im in images:
            new_im.paste(im, (0, offset))
            offset += im.size[1]
    else:
        new_im = Image.new('RGB', (sum(widths), max(heights)))
        for im in images:
            new_im.paste(im, (offset, 0))
            offset += im.size[0]

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

parser.add_option('-o', '--orientation',
                  action="store", dest="orientation",
                  help="orientation")

options, args = parser.parse_args()

parsed_path = options.path
parsed_initial_name = options.initial_name
parsed_target_name = options.target_name
parsed_orientation = options.orientation

if parsed_orientation is None:
    parsed_orientation = 'v'
elif parsed_orientation is not 'h' and parsed_orientation is not 'v':
    raise Exception(f'Can\'t resolve the orientation. Please, pass only \'v\' for vertical or \'h\' for horizontal.')

main(parsed_path, parsed_initial_name, parsed_target_name, parsed_orientation)
