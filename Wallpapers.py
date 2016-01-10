import os
import urllib2
import re
import time
import socket

class Wallpapers():
    __dest_folder = ""

    def __init__(self, folder):
        self.__dest_folder = folder

    def parse_images(self, page_data):
        # print(page_data)

        anchor_start = '<div class="badge-post-container post-container ">'
        anchor_end = '</div>'

        images_urls = list()
        counter = 0

        # while page contains needed anchor cut the data
        while True:
            pos_start = page_data.find(anchor_start)

            # anchor not found
            if pos_start == -1:
                break
            pos_end = page_data.find(anchor_end, pos_start)
            counter+=1

            block = page_data[pos_start:pos_end]    # block with image url (non-gif)
            page_data = page_data[pos_end:]         # remove previous block

            # find urls in block of data and add they to list
            urls = re.findall(r'<img class="badge-item-img" src="(.+)" alt=', block)
            for url in urls:
                if len(url) == 0:
                    continue
                images_urls.append(url)

        # print(counter)
        # print(images_urls)
        return images_urls

    # load images by url and save they into files
    def save_images(self, images_urls):
        saved = 0
        for url in images_urls:
            file_name = url[url.rfind("/")+1 : ]
            fullpath = self.__dest_folder + file_name
            # print(file_name)

            if os.path.exists(fullpath):
                # print("File '" + file_name + "' already exists")
                continue

            img_page = urllib2.urlopen(url)
            img_data = img_page.read()

            # print(fullpath)
            file = open(fullpath, "w")
            file.write(img_data)
            file.close()

            saved += 1

        return saved

    def main_loop(self):
        sections = (
            "http://9gag.com/funny",
            "http://9gag.com/geeky",
            "http://9gag.com/meme",
            "http://9gag.com/comic",
            "http://9gag.com/design"
        )


        while True:
            # check every section
            saved_images = 0
            for section in sections:
                # load page
                response = urllib2.urlopen(section)
                rawdata = response.read()

                # parse images urls
                images_urls = self.parse_images(rawdata)

                # save found images to pointed folder
                saved_images += self.save_images(images_urls)

            print("[" + time.strftime("%H:%M:%S") + "] Saved " + str(saved_images) + " images")
            time.sleep(150)  #sleep for 150 seconds


def main():
    wallpapers = Wallpapers("/media/skident/Work/Media/Images/9gag/")
    wallpapers.main_loop()

main()