import numpy as np
import mrcfile
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
import cv2


"""
The formula of contrast transfer function is based on 'CTF Simulation' and some papers
'CTF Simulation': https://ctfsimulation.streamlit.app
'cryoSPARC CTF estimation': https://guide.cryosparc.com/processing-data/all-job-types-in-cryosparc/ctf-estimation
CTFFIND4: Fast and accurate defocus estimation from electron micrographs. Alexis Rohou and Nikolaus Grigorieff. Journal of Structural Biology 192 (2015) 216–221.
Computational Methods for Single-Particle Cryo-EM. Amit Singer and Fred J. Sigworth. Annual Review of Biomedical Data Science, Vol. 3, pp. 163-190, 2020.
"""
class CTF:
    def __init__(self):
        self.df = 1.5  # defocus (delta_f) (unit: miu_m)
        self.ddf = 0.0  # magnitude of astigmatism: max_df - min_df (delta_delta_f) (unit: miu_m)
        self.theta_0 = 0.0  # astigmatism angle: angle of max defocus direction (theta_0) (unit: degree)
        self.phi = 0.0  # phase shift (phi) (unit: degree)
        self.pixel_size = 1.0  # pixel size (unit: Angstrom/pixel)
        self.V = 300.0  # accelerating voltage: determine wave length lambda (unit: kV)
        self.Cs = 2.7  # Spherical aberration coefficient (Cs) (unit: mm)
        self.Q = 0.0  # amplitude contrast in percentage (Q) (unit: percent)
        self.image_size = 256  # image size (unit: pixel)
        self.B = 0.0  # b-factor (B) (unit: Angstrom^2)

    def get_wave_length(self):
        wl = 12.2639 / np.sqrt(self.V * 1000.0 + 0.97845 * self.V * self.V)  # unit: Angstrom, a little bit numerical simplified
        return wl

    def ctf_value(self, s, theta):
        # unit of input s: 1/Angstrom
        # unit of input theta_0: degree

        wl = self.get_wave_length()  # unit: Angstrom
        a = np.pi * wl * s*s * self.df*1e4  # unit: radians
        b = np.pi/2.0 * wl * s*s * self.ddf*1e4 * np.cos(2.0*(theta-self.theta_0)*np.pi/180.0)  # unit: radians
        c = -np.pi/2.0 * wl*wl*wl * s*s*s*s * self.Cs*1e7  # unit: radians
        d = self.phi*np.pi/180.0 + np.arcsin(self.Q/100.0)  # unit: radians
        env = np.exp(-self.B * s*s / 4.0)
        ctf = -np.sin(a+b+c+d) * env  # unit: 1

        return ctf

    def ctf2d(self):
        s_nyquist = 1./2 / self.pixel_size
        s_interval = s_nyquist / (self.image_size//2)
        sx = np.arange(-self.image_size//2, self.image_size//2) * s_interval
        sy = np.arange(-self.image_size//2, self.image_size//2) * s_interval
        ctf_img = np.zeros((sx.shape[0], sy.shape[0]))
        for i in range(ctf_img.shape[0]):
            for j in range(ctf_img.shape[0]):
                s = np.sqrt(sx[i]*sx[i] + sy[j]*sy[j])
                theta = np.arctan2(sy[j], sx[i]) * 180/np.pi
                ctf_value = self.ctf_value(s, theta)
                ctf_img[i, j] = ctf_value
        return ctf_img

if __name__ == '__main__':

    # create a CTF instance
    ctf = CTF()

    # set CTF parameters
    ctf.df = 1.5
    ctf.ddf = 0.1
    ctf.theta_0 = 45.0
    ctf.phi = 30.0
    ctf.pixel_size = 0.6575
    ctf.V = 300.0
    ctf.Cs = 2.7
    ctf.Q = 7.0
    ctf.image_size = 440.0
    ctf.B = 0.0

    # check 1D CTF values at some points
    for s in [0, 0.0019, 0.0038, 0.0057, 0.0076, 0.4091, 0.4110, 0.4129, 0.4148, 0.4167]:
        print('s:', s, 'CTF value:', ctf.ctf_value(s, 0))

    # create 2D CTF image
    ctf_image = ctf.ctf2d()

    # save 2D CTF image to check
    flag = cv2.imwrite('/home/hubin/CODE_shared/utils/CTF_image.png', (ctf_image - np.min(ctf_image)) * 255.0 / (np.max(ctf_image) - np.min(ctf_image)))

    # plot 2D CTF image to check
    imshow(ctf_image)
    plt.show()
    plt.imshow(ctf_image, cmap='gray')
    plt.show()

    # load a projection stack .mrcs file
    mrc = mrcfile.open('/home/hubin/CODE_shared/utils/CTF_cryosparc_projection.mrcs', mode='r')
    stack = mrc.data
    mrc.close()
    N = stack.shape[0]

    # create CTF corrupted projection stack
    CTF_stack = np.zeros_like(stack)
    for i in range(N):
        proj = stack[i, :, :]
        CTF_proj = np.real(np.fft.ifft2(np.fft.fft2(proj)*np.fft.fftshift(ctf_image)))
        CTF_stack[i, :, :] = CTF_proj

    # save CTF corrupted projection stack
    mrc = mrcfile.new('/home/hubin/CODE_shared/utils/CTF_corrupted_projection.mrcs', overwrite=True)
    mrc.set_data(CTF_stack)
    mrc.close()




