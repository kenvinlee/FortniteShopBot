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

    # blank shop image

    shop_image_name = "daily_shop.png"
    shop_width = 750
    shop_height = (math.ceil(len(daily_shop) / 4) + math.ceil(len(featured_shop) / 4)) * 181 + 250

    shop_image = Image.new("RGBA", (shop_width, shop_height))
    draw = ImageDraw.Draw(shop_image, "RGBA")
    draw.rectangle(((0, 0), (shop_width, shop_height)), fill="#3b3a3a")

    # title
    font_size = 32
    font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=font_size)

    title = "Fortnite Daily Shop"
    title_x = (shop_width - draw.textsize(title, font=font)[0]) / 2
    date_x = (shop_width - draw.textsize(date, font=font)[0]) / 2

    draw.text((title_x, 20), title, fill="#FFFFFF", font=font)
    draw.text((date_x, 55), date, fill="#b5b0af", font=font)

    start_x = 67
    start_y = 150

    # draw Daily Itmes
    daily_text = "Daily Items"
    draw.text((start_x, 110), daily_text, fill="#FFFFFF", font=font)
    shop = add_shop_items(start_x, start_y, daily_shop, shop_image)
    shop_image = shop[0]

    start_y = shop[1] + 200

    # draw Featured Items
    featured_text = "Featured Items"
    draw.text((start_x, start_y), featured_text, fill="#FFFFFF", font=font)

    start_y += 40
    shop = add_shop_items(start_x, start_y, featured_shop, shop_image)
    shop_image = shop[0]

    shop_image.save(shop_image_name, "PNG")


def add_shop_items(start_x, start_y, shop_array, shop_image):
    counter = 0
    item_x = start_x
    item_y = start_y

    for item in shop_array:
        base_icon = Image.open(item[1]).convert("RGBA")
        shop_image.paste(base_icon, (item_x, item_y), base_icon)

        item_x += 155
        counter += 1

        if counter > 3:
            counter = 0
            item_y += 186
            item_x = start_x

    return shop_image, item_y


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

    icon_max_width = 512
    icon_max_height = 619

    icon = Image.new("RGBA", (icon_max_width, icon_max_height))

    # background
    draw = ImageDraw.Draw(icon, "RGBA")
    draw.rectangle(((0, 0), (icon_max_width, icon_max_height)), fill=border_color)
    gradient = draw_radial_gradient(outer_color, inner_color, (500, 506))
    icon.paste(gradient, (6, 6))

    # icon
    base_icon = Image.open(image_name).convert("RGBA")
    icon.paste(base_icon, (0, 0), base_icon)

    # name text background
    text_background = Image.open("text_background.png").convert("RGBA")
    icon.paste(text_background, (6, 412), text_background)

    # text for name and price
    font_size = 58
    font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=font_size)
    while draw.textsize(name, font=font)[0] > 440:
        font_size -= 1
        font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=font_size)

    # name
    name_x = (icon_max_width - draw.textsize(name, font=font)[0])/2
    name_y = ((100 - draw.textsize(name, font=font)[1])/2) + 412
    draw.text((name_x, name_y), name, fill="#FFFFFF", font=font)

    # price
    font = ImageFont.truetype("BURBANKSMALL-BLACK.OTF", size=64)
    font_y = int(draw.textsize(price, font=font)[1])
    price_x = (icon_max_width - font_y - draw.textsize(price, font=font)[0])/2
    price_y = ((116 - draw.textsize(price, font=font)[1])/2) + 513

    draw.text((price_x + font_y, price_y), price, fill="#FFFFFF", font=font)
    v_bucks_icon = Image.open("vbucks_icon.png").convert("RGBA")
    v_bucks_icon.thumbnail((font_y, font_y), Image.ANTIALIAS)

    v_bucks_x = int(price_x)
    icon.paste(v_bucks_icon, (v_bucks_x, int(price_y)), v_bucks_icon)

    icon_x = 150
    icon_y = (icon_x / icon_max_width) * icon_max_height
    icon.thumbnail((icon_x, icon_y), Image.ANTIALIAS)
    icon.save(image_name, "PNG")

    return icon, image_name


def draw_radial_gradient(outer, inner, dimensions):
    outer_color = ImageColor.getrgb(outer)
    inner_color = ImageColor.getrgb(inner)

    gradient = Image.new("RGB", dimensions)
    cx = dimensions[0] * 0.5
    cy = dimensions[1] * 0.5
    ext = (dimensions[0] / 2) ** 2 + (dimensions[1] / 2) ** 2

    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            # Find the distance to the center
            d = ((x - cx) ** 2) + ((y - cy) ** 2)
            dist_to_center = min(1, d / ext)
            inv = 1 - dist_to_center

            # Calculate r, g, and b values
            r = outer_color[0] * dist_to_center + inner_color[0] * inv
            g = outer_color[1] * dist_to_center + inner_color[1] * inv
            b = outer_color[2] * dist_to_center + inner_color[2] * inv

            # Place the pixel
            gradient.putpixel((x, y), (int(r), int(g), int(b)))

    return gradient
