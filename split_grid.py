from PIL import Image
import sys

# class for each agricultural plot
class PixelBlock:
	def __init__(self, ul_corner, br_corner, image):
		self.ul = ul_corner
		self.br = br_corner
		self.height = self.br[1] - self.ul[1]
		self.width = self.br[0] - self.ul[0]
		self.ur = self.ul + width
		self.bl = self.br - width
		# tranfser pixels
		for i in xrange(image.width):
			for j in xrange(image.height):
				self.pixels.append(image.getpixel((i,j)))

	# returns average color of pixel block	
	def getAvgColor(self):
		totalRGBA = [0,0,0,0]
		for i in xrange(self.width):
			for j in xrange(self.height):
				for k in xrange(4):
					totalRGBA[k] += self.pixels[i*self.height + j][k]
		return totalRGBA/(i*j)

# returns color difference between two rgba arrays
def colorDiff(rgba1, rgba2):
	totalDiff = 0
	for i in xrange(4):
		totalDiff += abs(rgba1[i] - rgba2[i])
	return totalDiff

# splitPlots()
# General: splits image into blocks of alike pixels
# Details: finds one plot and uses the size to assume dimensions for 
# the opthers because not every plot might have a large gradient with 
# neighboring plot
# Args: image, array of PixelBlocks
#
def splitPlots(image, plotArray):
	upperLeftCorner = (-1,-1)
	bottomRightCorner = (-1,-1)

	for i in xrange(image.width-1):
		for j in xrange(image.height-1):
			# look for edge
			curr_p = image.getpixel((i,j))
			edgeDiff_w = colorDiff(curr_p, image.getpixel((i+1,j)))
			edgeDiff_h = colorDiff(curr_p, image.getpixel((i,j+1)))
			if edgeDiff_w > 50:
				# look for upper left corner
				for k in xrange(j,image.height-1):
					edgeDiff_h1 = colorDiff(image.getpixel((i,k)), image.getpixel((i,k+1)))
					if edgeDiff_h1 > 50:
						upperLeftCorner = (i,k)
				# look for bottom right
				if upperLeftCorner[0] > -1:
					# right edge
					for k in xrange(i, image.width-1):
						edgeDiff_w1 = colorDiff(image.getpixel((k,j)), image.getpixel((k+1,j)))
						if edgeDiff_w1 > 50:
							# bottom right corner
							for l in xrange(j, image.height-1):
								edgeDiff_h2 = colorDiff(image.getpixel((k,l)), image.getpixel((k,l+1)))
								if edgeDiff_h2 > 50:
									bottomRightCorner = (k,l)
									return (upperLeftCorner,bottomRightCorner)

# ------------- MAIN -----------------
image_name = sys.argv[1]
im = Image.open(image_name)

# get size of image
w = im.width
h = im.height
# agricultural plots array
agriPlots = []


print splitPlots(im, agriPlots)











