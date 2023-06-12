import numpy as np
from scipy import ndimage
from sewar.full_ref import ssim

class ImageCompression():

    def __init__(self, image, domainSize, rangeSize, stAmount=8):

        # Initialise attributes
        self.image = image
        self.range_size = rangeSize
        self.domain_size = domainSize
        self.stAmount = stAmount

        # predefined possible contractions
        rotations = [0, 90, 180, 270]
        flip = [True, False]
        self.possible = [(r, f) for r in rotations for f in flip]
       

        # Generate transformations of domain blocks and encode
        self.domainBlockTransforms = self.transform_all_blocks()
        self.encoded = self.encode()

    def scale(self, image, scale_amount):

        x, y = image.shape[0] // scale_amount, image.shape[1] // scale_amount

        scaled = np.zeros((x, y))

        for i in range(scaled.shape[0]):
            for j in range(scaled.shape[1]):
                scaled[i, j] = np.mean(image[i*scale_amount:(i + 1)*scale_amount, j*scale_amount:(j + 1) * scale_amount])

        return scaled 
    
    def transform(self, image, flip, rotation, s=1, o=0):

        transformed = image.copy()

        if flip:
            transformed = transformed[::-1, :]

        return s * ndimage.rotate(transformed, rotation, reshape=False) + o

    def transform_all_blocks(self):

        scale_amount = self.domain_size // self.range_size

        contraction_list = []

        for i in range((self.image.shape[0] - self.domain_size) // self.stAmount + 1):
            for j in range((self.image.shape[1] - self.domain_size) // self.stAmount + 1):

                # Get domain block and scale to range block size
                block = self.image[i*self.stAmount:i*self.stAmount + self.domain_size, j*self.stAmount:j*self.stAmount + self.domain_size]
                block = self.scale(block, scale_amount)

                for rotation, flip in self.possible:
                    contraction_list.append((i, j, flip, rotation, self.transform(block, flip, rotation)))

        return contraction_list

    def compute_s_o(self, domain, range):

        mat = np.concatenate((np.ones((domain.size, 1)), np.reshape(domain, (domain.size, 1))), axis=1)
        b = np.reshape(range, (range.size,))

        x, _, _, _ = np.linalg.lstsq(mat, b, rcond=None)

        return x[1], x[0]

    def encode(self):

        encoding = []

        row_block_num = self.image.shape[0] // self.range_size
        col_block_num = self.image.shape[1] // self.range_size

        for i in range(row_block_num):

            encoding.append([])

            for j in range(col_block_num):
                
                cur_min = np.inf
                encoding[i].append("transform")

                rangeBlock = self.image[i*self.range_size:(i+1)*self.range_size, j*self.range_size:(j+1)*self.range_size]

                for domain_i, domain_j, flip, rotation, transformed in self.domainBlockTransforms:
                    
                    s, o = self.compute_s_o(transformed, rangeBlock)

                    new_transform = s * transformed + o

                    difference = np.sum(np.square(rangeBlock - new_transform))

                    if difference < cur_min:
                        cur_min = difference
                        encoding[i][j] = (domain_i, domain_j, flip, rotation, s, o)
            
        return encoding

    
    def decode(self, number_iterations):

        scale_amount = self.domain_size // self.range_size

        width = len(self.encoded) * self.range_size
        height = len(self.encoded[0]) * self.range_size

        zero_iter = np.random.randint(0, 256, (height, width))
        image_iterations = [(zero_iter, ssim(self.image, zero_iter)[0])]
        next_image = np.zeros((height, width))

        for _ in range(number_iterations):
            
            for i in range(len(self.encoded)):

                for j in range(len(self.encoded[i])):

                    i_domain, j_domain, flip, rotation, s, o = self.encoded[i][j]
                    block = image_iterations[-1][0][i_domain*self.stAmount:i_domain*self.stAmount + self.domain_size, j_domain*self.stAmount:j_domain*self.stAmount + self.domain_size]
                    block = self.scale(block, scale_amount)
                    block = self.transform(block, flip, rotation, s, o)

                    next_image[i*self.range_size:(i+1)*self.range_size, j*self.range_size:(j+1)*self.range_size] = block
                
            image_iterations.append((next_image, ssim(self.image, next_image.astype(np.int32))[0]))
        
        return image_iterations
                                             

