from PIL import Image
import sys
import random

# class for each agricultural plot
class PixelBlock:

	def __init__(self, ul_corner, br_corner, image):
		self.ul = ul_corner
		self.br = br_corner
		self.height = self.br[1] - self.ul[1]
		self.width = self.br[0] - self.ul[0]
		self.ur = (self.ul[0] + self.width, self.ul[1])
		self.bl = (self.br[0] - self.width, self.br[1])
		self.pixels = []
		# transfer pixel indices
		for i in xrange(self.ul[0], self.ur[0]):
			for j in xrange(self.ul[1], self.bl[1]):
				self.pixels.append(image.getpixel((i,j)))

	# returns average color of pixel block	
	def getAvgColor(self):
		totalRGBA = [0,0,0]
		for i in xrange(self.width):
			for j in xrange(self.height):
				for k in xrange(3):
					totalRGBA[k] += self.pixels[i*self.height + j][k]
		for k in xrange(3):
			totalRGBA[k] /= self.width*self.height
		return totalRGBA

	def setBlockColor(self, rgba):
		for p in self.pixels:
			self.pixels = rgba

	def copyCorners(self, other):
		self.ul = other.ul
		self.ur = other.ur 
		self.bl = other.bl 
		self.br = other.br 

	def swapCorners(self, other):
		tul = self.ul
		tur = self.ur
		tbl = self.bl
		tbr = self.br
		self.ul = other.ul
		self.ur = other.ur
		self.br = other.br
		self.bl = other.bl
		other.ul = tul
		other.ur = tur
		other.br = tbr
		other.bl = tbl


# returns color difference between two rgba arrays
def colorDiff(rgba1, rgba2):
	totalDiff = 0
	for i in xrange(3):
		totalDiff += abs(rgba1[i] - rgba2[i])
	return totalDiff

def importImage(name):
	return Image.open(name)

# tilePlots()
# General: splits image into blocks of alike pixels
#
def tile(im, wp, hp, plots):
	plotWidth = im.width/wp
	plotHeight = im.height/hp
	for ip in xrange(hp):
		for jp in xrange(wp):
			ul_corner = ((jp*plotWidth,ip*plotHeight))
			block = PixelBlock(ul_corner, (ul_corner[0]+plotWidth,ul_corner[1]+plotHeight), im)
			for ii in xrange(plotHeight):
				for jj in xrange(plotWidth):
					block.pixels.append(im.getpixel((jp*wp+jj,ip*hp+ii)))
			plots.append(block)


def showTiles(im, wp, hp, plots):
	white = (255, 255, 255, 255)
	for i in xrange(len(plots)):
		if i % 2 == 1:
			for ii in xrange(plots[i].ul[0], plots[i].ur[0]):
				for jj in xrange(plots[i].ul[1], plots[i].bl[1]):
					im.putpixel((ii, jj), white)


# swaps (x1,y1) with (x2,y2)
def swapTiles(im, wp, hp, coord1, coord2, plots):
	# convert to 1d
	p = coord1[1]*wp + coord1[0]
	q = coord2[1]*wp + coord2[0]
	for i in xrange(plots[p].width):
		for j in xrange(plots[p].height):
			color1 = im.getpixel((i+plots[p].ul[0],j+plots[p].ul[1]))
			color2 = im.getpixel((i+plots[q].ul[0],j+plots[q].ul[1]))
			im.putpixel((i+plots[p].ul[0],j+plots[p].ul[1]),color2)
			im.putpixel((i+plots[q].ul[0],j+plots[q].ul[1]),color1)
			# update plots list
			plots[p].swapCorners(plots[q])
			tmp = plots[p]
			plots[p] = plots[q]
			plots[q] = plots[p]




def setTiles(im, wp, hp, newplots):
	for i in xrange(len(newplots)):
		j = 0
		for ii in xrange(newplots[i].ul[0], newplots[i].ur[0]):
			for jj in xrange(newplots[i].ul[1], newplots[i].bl[1]):
				im.putpixel((ii, jj), newplots[i].pixels[j])
				j += 1


def matchImage(source, match, wp, hp, plots):
	avgs = []
	for p in plots:
		avgs.append(p.getAvgColor())
	matchplots = []
	tile(match, wp, hp, matchplots)
	newplots = []
	used = []
	for m in matchplots:
		a = m.getAvgColor()
		best = 100000
		bestidx = 0
		for b in xrange(len(avgs)):
			test = colorDiff(avgs[b], a)
			if best > test and b not in used:
				best = test
				bestidx = b
		n = PixelBlock(plots[bestidx].ul,plots[bestidx].br,source)
		newplots.append(n)
		used.append(bestidx)
		newplots[-1].copyCorners(plots[len(newplots)-1])
	setTiles(source, wp, hp, newplots)


def randomTiles(im, wp, hp, plots):
	newplots = []
	for p in plots:
		r = random.random()
		r = int(r*wp*hp)
		n = PixelBlock(plots[r].ul, plots[r].br,im)
		newplots.append(n)
		newplots[-1].copyCorners(plots[len(newplots)-1])
	setTiles(im, wp, hp, newplots)


# ------------- MAIN -----------------
image_name = sys.argv[1]
im = Image.open(image_name)

# get size of image
w = im.width
h = im.height
# agricultural plots array
agriPlots = []
# x by x plots
wplots = int(sys.argv[2])
hplots = int(sys.argv[3])

match_name = sys.argv[4]
match = Image.open(match_name)
match.resize((w,h))

save_name = sys.argv[5]

tile(im, wplots, hplots, agriPlots)
matchImage(im, match, wplots, hplots, agriPlots)
#randomTiles(im, wplots, hplots, agriPlots)
#showTiles(im, wplots, hplots, agriPlots)
im.show()
im.save(save_name)










