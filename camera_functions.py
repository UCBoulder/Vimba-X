from vmbpy import *
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

def print_camera(cam: Camera):
    print('/// Camera Name   : {}'.format(cam.get_name()))
    print('/// Model Name    : {}'.format(cam.get_model()))
    print('/// Camera ID     : {}'.format(cam.get_id()))
    if cam.get_id() == "DEV_000F315DF185":
        print("Side Camera")
    elif cam.get_id() == "DEV_000F315DF178":
        print("Push Beam Camera")
    print('/// Serial Number : {}'.format(cam.get_serial()))
    print('/// Interface ID  : {}\n'.format(cam.get_interface_id()))

def set_camera_settings(cam,
                  exposure_time = 1e6, 
                  gain = 40,
                  pixel_format = 0,
                  offset_x = 0,
                  offset_y = 0,
                  width = 2064,
                  height = 1544):

    """
    exposure time: in us, [16.0, 85899344.0]
    gain: in dB [0, 40]
    pixel_format: of the image, 0: Mono8; 1: Mono12, 2: Mono12Packed
    offset_x: x offset of the frame
    offset_y: y offset of the frame
    width: width of the frame
    height: height of the frame
    ================================================================
    offset_x + width <= 2064
    offset_y + height <= 1544
    """

    print("Camera settings")
    print("-----------------------------------")
    # set the exposure time
    cam.ExposureTimeAbs.set(exposure_time)
    print("Exposure time:", str(cam.ExposureTimeAbs.get())+ " us")
    
    # set the gain
    cam.Gain.set(gain)
    print("Gain:", str(cam.Gain.get())+ " dB")

    # set pixel format
    cam.set_pixel_format(cam.get_pixel_formats()[pixel_format])
    print("Pixel Format:", cam.get_pixel_format())

    # recover default settings
    cam.OffsetX.set(0)
    cam.OffsetY.set(0)

    # set frame height and width
    cam.Width.set(width)
    cam.Height.set(height)
    print("frame size (w x h):\n\n", str(cam.Width.get())+ " x "+str(cam.Height.get()))

    # set center of the frame
    cam.OffsetX.set(offset_x)
    cam.OffsetY.set(offset_y)
    print("offset (X, Y):", "("+str(cam.OffsetX.get())+ ", "+str(cam.OffsetY.get())+")")

def get_image_avg(cam, 
                    N = 1):

    width = cam.Width.get()
    height = cam.Height.get()
    # create an empty array with (h x w x N) dimension
    frame_arr = np.empty((height, width, N), dtype=np.uint8)

    # taking N pictures consecutively
    for i, frame in enumerate(cam.get_frame_generator(limit=N)):
        frame_np = frame.as_numpy_ndarray()[:,:,0]
        frame_arr[:,:,i] = frame_np

    # taking the average of the pictures
    frame_avg = np.average(frame_arr, 2)
    # frame_avg_uint8 = np.round(frame_avg).astype(np.uint8)

    # return frame_avg_uint8
    return frame_avg

def get_images(cam, N=1):

    width = cam.Width.get()
    height = cam.Height.get()
    # create an empty array with (h x w x N) dimension
    frame_arr = np.empty((height, width, N), dtype=np.uint8)

    # taking N pictures consecutively
    for i, frame in enumerate(cam.get_frame_generator(limit=N)):
        frame_np = frame.as_numpy_ndarray()[:,:,0]
        # np.save(filepath, frame_np)  # Save image
        frame_arr[:,:,i] = frame_np

    # return frame_avg_uint8
    return frame_arr


if __name__ == '__main__':
    with VmbSystem.get_instance() as vmb:
        cams = vmb.get_all_cameras()
        print('Cameras found: {}'.format(len(cams)))

        for cam in cams:
            print_camera(cam)

        with cams[0] as cam:
            set_camera_settings(cam)
            frame_avg = get_image_avg(cam)
            # print(frame_avg)

    plt.imshow(frame_avg)
    plt.colorbar()
    plt.show()