import os
import urllib.request

class utils():
    MANGADIR = "/efs/mangas/en"

    @staticmethod
    def save_image_from_url(url, filename):
        local_filename = "{}/{}".format(utils.MANGADIR, filename)
        dirname = os.path.dirname(local_filename)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.exists(local_filename):
            print("Saving image from url to: " + local_filename)

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, local_filename)

        return True


