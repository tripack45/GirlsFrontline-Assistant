import image
import api

im = image.loadImage('test\\resource\\auto1_2_select_team.png')
t = api.loadImageByKey('TeamSelection', 'tag2Selected')

center, v = image.matchTemplateExact(im, t)
tsize = image.getImageSize(t)
pt1 = (center[0] - tsize[0] // 2,
       center[1] - tsize[1] // 2)
pt2 = (center[0] + tsize[0] // 2,
       center[1] + tsize[1] // 2)
rst = image.drawBox(im, pt1, pt2)
image.showImage(rst)
image.waitKeyboard()
image.releaseAllWindows()
print(center)
print(v)
