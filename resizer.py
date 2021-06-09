from PIL import Image


def resize_save_white_back(img, final_side_length, out_filename):
    first_side_length = max(img.size[0], img.size[1])
    if img.size[0] != img.size[1]:
        bg = Image.new('RGB', (first_side_length, first_side_length), (255, 255, 255))
        offset = (int(round(((first_side_length - img.size[0]) / 2), 0)),
                  int(round(((first_side_length - img.size[1]) / 2), 0)))

        bg.paste(img, offset)

        bg = bg.resize((final_side_length, final_side_length))

        bg.save(out_filename)
        return
    img = img.resize((final_side_length, final_side_length))
    img.save(out_filename)


if __name__ == '__main__':
    for i in range(14208):
        img_filename = str(i).zfill(5) + '.jpg'
        src = './rebag-imgs/' + img_filename
        dest = './resized-imgs/' + img_filename
        im = Image.open(src)
        resize_save_white_back(im, 256, dest)
        if i % 200 == 0:
            print(str(i + 1) + '/' + str(14208) + " images processed")

    for i in range(24161):
        img_filename = str(i).zfill(5) + '.jpg'
        src = './realreal-imgs/rr-' + img_filename
        dest = './resized-imgs/rr-' + img_filename
        im = Image.open(src)
        resize_save_white_back(im, 256, dest)
        if i % 200 == 0:
            print(str(i + 1) + '/' + str(14208) + " images processed")
