import aiofnbr
import asyncio
import requests
import shutil
import math
from PIL import Image, ImageDraw, ImageColor, ImageFont

api_key = "6f83f56f-4fb8-4e36-9f5f-eb5b888f2e9e"
loop = asyncio.get_event_loop()


def print_shop():
    request = aiofnbr.Shop(api_key)
    response = loop.run_until_complete(request.send())
    if response.status == 200 and response.type == aiofnbr.constants.SHOP_TYPE:
        shop = response.data

        print("Daily items:")
        for item in shop.daily:
            print("\t{0}: {1}, {2}".format(item.name, item.price, item.icon))

        print("Featured items:")
        for item in shop.featured:
            print("\t{0}: {1}, {2}".format(item.name, item.price, item.icon))
            # for property, value in vars(item).items():
            #     print(property, ": ", value)

    else:
        print("Error getting shop")


def download_icon(item_name, icon_url):
    r = requests.get(icon_url, stream=True)

    if r.status_code == 200:
        with open("icons/{0}.png".format(item_name), "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def create_shop(date):
    request = aiofnbr.Shop(api_key)
    response = loop.run_until_complete(request.send())

    daily_shop = []
    featured_shop = []

    shop_image_name = "{0}.png".format(date)

    if response.status == 200 and response.type == aiofnbr.constants.SHOP_TYPE:
        shop = response.data

        print("Daily items:")
        for item in shop.daily:
            print(item.name)
            download_icon(item.name, item.icon)
            daily_shop.append(create_icon(item.name, item.price, item.rarity))

        print("Featured items:")
        for item in shop.featured:
            print(item.name)
            download_icon(item.name, item.icon)
            featured_shop.append(create_icon(item.name, item.price, item.rarity))

    else:
        print("Error getting shop")

    num_items = len(daily_shop) + len(featured_shop)


def create_icon(name, price, rarity):
    """Make an image icon for each shop item.

    name -- the name of the item
    price -- the price of the item
    rarity -- the rarity of the item

    This function performs the following steps:
    1. Creates an image
    2. Sets the background with its color based on the item"s rarity
    3. Pastes the item"s image icon onto the background
    4. Pastes the item"s text and price on top of the image
    5. Scales down the icon size to 205x248
    """

    image_name = "icons/{0}.png".format(name)

    if rarity == "common":
        # Grey
        outer_color = "#767f93"
        inner_color = "#a6b3c4"
        border_color = "#71798D"
    elif rarity == "uncommon":
        # Green
        outer_color = "#227F1F"
        inner_color = "#71C152"
        border_color = "#61BB30"
    elif rarity == "rare":
        # Blue
        outer_color = "#1D4B8A"
        inner_color = "#73B9EE"
        border_color = "#29B1DA"
    elif rarity == "epic":
        # Purple
        outer_color = "#53298B"
        inner_color = "#BB76EB"
        border_color = "#CA4BDF"
    elif rarity == "legendary":
        # Orange
        outer_color = "#AD501A"
        inner_color = "#FF9B62"
        border_color = "#E7853D"
    else:
        # something"s wrong here
        print("Rarity not provided")
        outer_color = "#000000"
        inner_color = "#000000"
        border_color = "#000000"

    icon = Image.new("RGBA", (512, 619))

    # background
    draw = ImageDraw.Draw(icon, "RGBA")
    draw.rectangle(((0, 0), (512, 619)), fill=border_color)
    gradient = draw_radial_gradient(outer_color, inner_color, (500, 506))
    icon.paste(gradient, (6, 6))

    # icon
    base_icon = Image.open(image_name).convert("RGBA")
    icon.paste(base_icon, (0, 0), base_icon)

    # name text
    text_background = Image.open('text_background.png').convert("RGBA")
    icon.paste(text_background, (6, 412), text_background)

    font_size = 64
    font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=font_size)
    while draw.textsize(name, font=font)[0] > 440:
        font_size -= 1
        font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=font_size)

    name_x = (512 - draw.textsize(name, font=font)[0])/2
    draw.text((name_x, 433), name, fill="#FFFFFF", font=font)

    icon.save(image_name, "PNG")

    return icon


def draw_radial_gradient(outer, inner, dimensions):
    outer_color = ImageColor.getrgb(outer)
    inner_color = ImageColor.getrgb(inner)

    gradient = Image.new("RGB", dimensions)

    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            # Find the distance to the center
            dist_to_center = math.sqrt((x - dimensions[0] / 2) ** 2 + (y - dimensions[1] / 2) ** 2)

            # Make it on a scale from 0 to 1
            dist_to_center = float(dist_to_center) / (math.sqrt(2) * dimensions[0] / 2)

            # Calculate r, g, and b values
            r = outer_color[0] * dist_to_center + inner_color[0] * (1 - dist_to_center)
            g = outer_color[1] * dist_to_center + inner_color[1] * (1 - dist_to_center)
            b = outer_color[2] * dist_to_center + inner_color[2] * (1 - dist_to_center)

            # Place the pixel
            gradient.putpixel((x, y), (int(r), int(g), int(b)))

    return gradient
