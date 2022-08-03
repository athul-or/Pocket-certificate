import random, datetime
from PIL import Image

class IMG_xor:
    def __init__(self):
        self.rnd =""
        self.static_path=r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\\"

    def enc(self,path):                 ########################### ENCRYPTION #####################
        """ input: 
                    path : full path of image to be encrypted
            output:
                    pth : encrypted path
                    r_rnd : random no. for red
                    g_rnd : random no. for green
                    b_rnd : random no. for blue """

        photo=Image.open(path)
        self.r_rnd= random.randint(100, 255)
        self.g_rnd = random.randint(100, 255)
        self.b_rnd = random.randint(100, 255)
        px=photo.load()
        w,h=photo.size

        for y in range(0,h):
            row=""
            for x in range(0,w):
                R,G,B=px[x,y]
                a1 = R                              #left shift R value by 4bits
                b1 = a1 & 15
                c1 = a1 & 240
                d1 = (b1 << 4) | (c1 >> 4)

                a2 = G                              #left shift G value by 4bits
                b2 = a2 & 15
                c2 = a2 & 240
                d2 = (b2 << 4) | (c2 >> 4)

                px[x,y]=(d1^self.r_rnd,d2^self.g_rnd,B^self.b_rnd)
        dd = datetime.datetime.now()
        dt = str(dd).replace(" ", "_").replace("-", "_").replace(":", "_")
        pth="enc_"+dt+".bmp"
        path = self.static_path+"encrypted\\"+pth
        photo.save(path)
        return pth,self.r_rnd,self.g_rnd,self.b_rnd

    def dec(self,path,r_rand,g_rand,b_rand):                 ########################### DECRYPTION #####################
        """ input: 
                path : encrypted path
                r_rand : random no. for red
                g_rand : random no. for green
                b_rand : random no. for blue
            output:
                pth : full path of image to be encrypted
                     """
        photo=Image.open(self.static_path+"encrypted\\"+path)
        px=photo.load()
        w,h=photo.size
        r = int(r_rand)
        g = int(g_rand)
        b = int(b_rand)

        for y in range(0,h):
            row=""
            for x in range(0,w):
                R,G,B=px[x,y]
                R1,G1,B1=(R^r,G^g,B^b)

                a1 = R1                             # left shift R value by 4bits
                b1 = a1 & 15
                c1 = a1 & 240
                d1 = (b1 << 4) | (c1 >> 4)

                a2 = G1                             # left shift G value by 4bits
                b2 = a2 & 15
                c2 = a2 & 240
                d2 = (b2 << 4) | (c2 >> 4)
                px[x,y]=(d1,d2,B1)
        dd = datetime.datetime.now()
        dt = str(dd).replace(" ", "_").replace("-", "_").replace(":", "_")
        pth = "dec_" + dt + ".bmp"
        photo.save(self.static_path+"decrypted\\"+pth)
        return pth


class re_size:
    def resize_image(self,input_image_path,
                     output_image_path,
                     size):
        print("sj")
        original_image = Image.open(input_image_path)
        width, height = original_image.size
        print('The original image size is {wide} wide x {height} '
              'high'.format(wide=width, height=height))

        resized_image = original_image.resize(size)
        width, height = resized_image.size
        print('The resized image size is {wide} wide x {height} '
              'high'.format(wide=width, height=height))
        #resized_image.show()
        resized_image.save(output_image_path)