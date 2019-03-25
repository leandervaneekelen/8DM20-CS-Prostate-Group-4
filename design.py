# Design document for decision fusion 
# Group 4, 8DM20, CS Prostate registration

# Fundamental assumption behind this decision fusion technique:
# better registrated images contributes more to the segmentation 
# result than less succesful registered images. Weighting images
# according to segmentation result would take this into account.

# Decision fusion process according to Isgum et al.:

## <-- INDICATE ASSERTIONS

# Subtract images:
for all registered images:
	do D[i] = ||registered atlas image - target image||
## D.shape() is [im_x, im_y, im_z, n_images - 1]
## values in D are 0.0 <= n <= 1.0

# Calculate weights lambda
for all difference maps D[i]:
	do D[i] = D[i] * gauss(/w sigma1 & mean = 0)
	do lambda[i] = 1/(D[i] + epsilon) /w epsilon << 1 # Epsilon in Isgum et al = 0.001
## lambda.shape() is [im_x, im_y, im_z, n_images - 1]
## values in lambda > 0, real 

# Merge probabilistic labels 
normalisation factor = 1 / (sum of all weight maps) ## normalisation factor > 0, 
													## shape is [im_x, im_y, im_z, 1]
segmentation map = normalisation factor * sum of (lambda[i]*registered atlas image i) for all i
## segmentation map.shape() is [im_x, im_y, im_z, 1]
## values in segmentation map are 0.0 <= n <= 1.0

# Treshold segmentation map
segmentation map = segmentation map * gauss(/w sigma2 & mean = 0)
segmentation = segmentation map > 0.5
## segmentation.shape is [im_x, im_y, im_z, 1]
## values in segmentation are 0 or 1 (binary)

# Details:
# Free parameters are sigma1 and sigma2. 
# These should be optimised to get highest metric score.
# Look up what '3D component labelling' is.

# Practical considerations:
# Input is preferably via numpy arrays: easy to manipulate
# As such, 15 numpy arrays (3D) needed, 14 registered images
# and 1 target image. Can be best supplied in two arguments
# target_image (3D array), registered_images (4D array)
# Outputs 3D array with segmentation, ready to be judged
# on correctness
