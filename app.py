from PIL import Image
import pytesseract
from pprint import pprint

# Set path for pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\David\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def remove_colors(image: Image, chosen_colours: list) -> Image:
    """Input an image and a list of colours. The function will scan all pixels and will set any pixels within the threshold of the colours given to black (3, 3, 3), and all other pixels to white.

    Args:
        image: Image object from PIL
        chosen_colours (list of tuples): Colours to pass through (R, G, B)

    Returns:
       Image object with valid pixels in black, all else white
    """

    # Creates a new image with the same size as the image to be tested
    new_image = Image.new("RGB", image.size)

    # Threshold, RGB values must match within +/- threshold

    threshold = 40

    # Iterates through each colour at a time
    for chosen_colour in chosen_colours:
        for x in range(image.width):
            for y in range(image.height):
                pixel_rgb = image.getpixel((x, y))

                # Checks test image pixel for match, or if new_image pixel has been set to valid (3, 3, 3)
                if all(
                    (
                        chosen_colour[0] - threshold
                        <= pixel_rgb[0]
                        <= chosen_colour[0] + threshold,
                        chosen_colour[1] - threshold
                        <= pixel_rgb[1]
                        <= chosen_colour[1] + threshold,
                        chosen_colour[2] - threshold
                        <= pixel_rgb[2]
                        <= chosen_colour[2] + threshold,
                    )
                ) or new_image.getpixel((x, y)) == (3, 3, 3):
                    new_image.putpixel((x, y), (3, 3, 3))
                else:
                    new_image.putpixel((x, y), (255, 255, 255))

    return new_image


# List of colours to be checked
chosen_colors = [(225, 30, 30), (63, 72, 204), (50, 170, 80)]

# Open image to be tested
image = Image.open("test.jpg")

processed_image = remove_colors(image, chosen_colors)
image.close()

processed_image.show()
processed_image.save("processed_image.jpg")

text1 = pytesseract.image_to_string(processed_image)

print(text1)

processed_image.close()
