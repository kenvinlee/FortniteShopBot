import aiofnbr
import asyncio
import urllib

api_key = '6f83f56f-4fb8-4e36-9f5f-eb5b888f2e9e'
loop = asyncio.get_event_loop()


def print_shop():
    request = aiofnbr.Shop(api_key)
    response = loop.run_until_complete(request.send())
    if response.status == 200 and response.type == aiofnbr.constants.SHOP_TYPE:
        shop = response.data

        print('Daily items:')
        for item in shop.daily:
            print('\t{0}: {1}, {2}'.format(item.name, item.price, item.icon))

        print('Featured items:')
        for item in shop.featured:
            print('\t{0}: {1}, {2}'.format(item.name, item.price, item.icon))
            # for property, value in vars(item).items():
            #     print(property, ": ", value)

    else:
        print('Error getting shop')


def download_icon(item_name, item_type):
    item_limit = 15  # integer between 1 and 15
    headers = {
        'x-api-key': '6f83f56f-4fb8-4e36-9f5f-eb5b888f2e9e',

    }
    request = aiofnbr.Images(api_key, search=item_name, type=item_type, limit=item_limit)
    response = loop.run_until_complete(request.send())
    if response.status == 200 and response.type == aiofnbr.constants.IMAGE_TYPE:
        print('Results:')
        image_data = response.data
        for item in image_data.results:
            f = open('icons/{0}.png'.format(item.name), 'wb')
            f.write(urllib.request.urlopen(item.icon).read(), headers)
            f.close()
    else:
        print('Error searching images')



def create_shop(date):
    request = aiofnbr.Shop(api_key)
    response = loop.run_until_complete(request.send())

    shop_image_name = '{0}.png'.format(date)

    if response.status == 200 and response.type == aiofnbr.constants.SHOP_TYPE:
        shop = response.data

        print('Daily items:')
        for item in shop.daily:
            download_icon(item.name, item.icon)

        print('Featured items:')
        for item in shop.featured:
            download_icon(item.name, item.icon)

    else:
        print('Error getting shop')


def create_icon(name, price, rarity, icon_url):
    '''Make an image icon for each item.'''

    icon = '{0}.png'.format(name)

    return icon
