import numpy as np
import colorsys
import pygame

class Image:
    """
    A container for image. This class
    also support animation.
    """

    def __init__(self, fname, angle, size, cd, loop, hue=0):
        self.img = pygame.transform.rotate(
                pygame.image.load(fname).convert_alpha(), angle)
        self.max_cd = cd
        self.loop = loop
        self.cd = 0

        #self.rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
        #self.hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

        if size != None:
            # 900*80/(100*80)
            self.nCells = self.img.get_width()*size[1]/ \
                (size[0]*self.img.get_height())
            self.size = size
            self.curCell = 0
            self.img = pygame.transform.scale(self.img,
                (self.img.get_width()*size[1]/self.img.get_height(),
                    size[1]))
        else:
            self.size = (self.img.get_width(), self.img.get_height())
            self.nCells, self.curCell = 1, 0

        if hue != 0:
            self.shift_hue(pygame.surfarray.pixels3d(self.img),
                hue/360.)

    def shift_hue(self, arr, hout):
        # WTF?
        hsv = self.rgb_to_hsv(arr/255.).astype('float')
        hsv[...,0] += hout
        #print hsv[...,0].mean()
        #print hsv[...,1].mean()
        #print hsv[...,2].mean()
        arr[...] = self.hsv_to_rgb(hsv)*255

    def get(self):
        val = self.img.subsurface(self.curCell*self.size[0], 0, self.size[0], self.size[1])
        if self.max_cd != 0:
            self.cd = (self.cd + 1) % self.max_cd
            if self.cd == 0:
                if self.loop == False and self.curCell == self.nCells-1:
                    pass
                else: self.curCell = (self.curCell + 1)%self.nCells
        return val

    def rgb_to_hsv(self, rgb):
        # Translated from source of colorsys.rgb_to_hsv
        hsv=np.empty_like(rgb)
        hsv[...,3:]=rgb[...,3:]
        r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
        maxc = np.max(rgb[...,:2],axis=-1)
        minc = np.min(rgb[...,:2],axis=-1)
        hsv[...,2] = maxc   
        hsv[...,1] = (maxc-minc) / maxc
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        hsv[...,0] = np.select([r==maxc,g==maxc],[bc-gc,2.0+rc-bc],default=4.0+gc-rc)
        hsv[...,0] = (hsv[...,0]/6.0) % 1.0
        idx=(minc == maxc)
        hsv[...,0][idx]=0.0
        hsv[...,1][idx]=0.0
        return hsv

    def hsv_to_rgb(self, hsv):
        # Translated from source of colorsys.hsv_to_rgb
        rgb=np.empty_like(hsv)
        rgb[...,3:]=hsv[...,3:]    
        h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]   
        i = (h*6.0).astype('uint8')
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        conditions=[s==0.0,i==1,i==2,i==3,i==4,i==5]
        rgb[...,0]=np.select(conditions,[v,q,p,p,t,v],default=v)
        rgb[...,1]=np.select(conditions,[v,v,v,q,p,p],default=t)
        rgb[...,2]=np.select(conditions,[v,p,t,v,v,q],default=p) 
        #print '*'*10
        #print rgb[...,0].mean()
        #print rgb[...,1].mean()
        #print rgb[...,2].mean()
        #print '*'*10
        return rgb
