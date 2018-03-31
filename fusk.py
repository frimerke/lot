#
# LOT module for fuskator.com
# handles importing form a thumb gallery link.
#
import common

def title(soup):
    try:
        title = "fuskator - " + soup.find("h1").string
        title = common.filter_nonprintable(title)
    except:
        title = "fuskator - " + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

    return title


def filelist(soup):
    meta = soup.findAll(class_="pic_pad")
    to_get = []
    for pic in meta:
        try:
            url = pic.attrs['src']
            url = url.replace("small", "large")
            url = "http://fuskator.com" + url
            to_get.append(url)
        except:
            pass

    return to_get

def down(dl_list, minmax):
    for image in dl_list:
        print(image)
        filename = image.split("/")
        filename = filename[-1]
        common.download(image, filename, minmax)
    print("Download complete!")
