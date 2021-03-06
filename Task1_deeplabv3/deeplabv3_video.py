from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import time
import cv2 
import tensorflow as tf
from timeit import default_timer as timer

# 这个地方指定输出的模型路径
TEST_PB_PATH = './model/deeplabv3_cityscapes_train/frozen_inference_graph.pb'
# TEST_PB_PATH    = './edgetpu-deeplab-slim/frozen_inference_graph.pb'

# 这个地方指定需要测试的图片
# TEST_IMAGE_PATH = "/home/aistudio/work/models/research/deeplab/image/20180604225051855.jpg"

TEST_VIDEO_PATH = "./video/123.mp4"


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""
    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None

        with open(TEST_PB_PATH, 'rb') as fhandle:
            graph_def = tf.GraphDef.FromString(fhandle.read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
          image: A PIL.Image object, raw input image.

        Returns:
          resized_image: RGB image resized from original input image.
          seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        print(target_size)
        resized_image = image.convert('RGB').resize(
            target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map


def create_pascal_label_colormap():
    """Creates a label colormap used in PASCAL VOC segmentation benchmark.

    Returns:
      A Colormap for visualizing segmentation results.
    """
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3

    return colormap


def label_to_color_image(label):
    """Adds color defined by the dataset colormap to the label.

    Args:
      label: A 2D array with integer type, storing the segmentation label.

    Returns:
      result: A 2D array with floating type. The element of the array
        is the color indexed by the corresponding element in the input label
        to the PASCAL color map.

    Raises:
      ValueError: If label is not of rank 2 or its value is larger than color
        map maximum entry.
    """
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')

    colormap = create_pascal_label_colormap()
    colormap[0:19] = [
        [128, 64, 128],
        [244, 35, 232],
        [70, 70, 70],
        [102, 102, 156],
        [190, 153, 153],
        [153, 153, 153],
        [250, 170, 30],
        [220, 220, 0],
        [107, 142, 35],
        [152, 251, 152],
        [70, 130, 180],
        [220, 20, 60],
        [255, 0, 0],
        [0, 0, 142],
        [0, 0, 70],
        [0, 60, 100],
        [0, 80, 100],
        [0, 0, 230],
        [119, 11, 32],
    ]

    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')

    return colormap[label]


def vis_segmentation(image, seg_map, path):
    """Visualizes input image, segmentation map and overlay view."""

    plt.figure(figsize=(15, 5))
    grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

    plt.subplot(grid_spec[0])
    plt.imshow(image)
    plt.axis('off')
    plt.title('input image')

    plt.subplot(grid_spec[1])
    seg_image = label_to_color_image(seg_map).astype(np.uint8)

    plt.imshow(seg_image)
    plt.imsave('./result/'+path.split('/')[-1][:-4]+'_color.', seg_image)
    plt.axis('off')
    plt.title('segmentation map')

    plt.subplot(grid_spec[2])
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.4)
#   seg_image=Image.open('./result/'+path.split('/')[-1][:-4]+'_color.png').convert("RGB")
    seg_image = Image.fromarray(seg_image)
    img_mix = np.asarray(Image.blend(image, seg_image, 0.4))
    plt.imsave('./result/'+path.split('/')[-1][:-4]+'_color_image.', img_mix)
    plt.axis('off')
    plt.title('segmentation overlay')

    unique_labels = np.unique(seg_map)
    ax = plt.subplot(grid_spec[3])
    plt.imshow(
        FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
    plt.xticks([], [])
    ax.tick_params(width=0.0)
    plt.grid('off')
    plt.show()


def segmentation(image, seg_map):
    seg_image = Image.fromarray(label_to_color_image(seg_map).astype(np.uint8))
    img_mix = np.asarray(Image.blend(image, seg_image, 0.4))
    return img_mix


LABEL_NAMES = np.asarray([
    'road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic light',
    'traffic sign', 'vegetation', 'terrain', 'sky', 'person', 'rider', 'car', 'truck',
    'bus', 'train', 'motocycle', 'bicycle'
])

FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)


def segmentation(image, seg_map):
    seg_image = Image.fromarray(label_to_color_image(seg_map).astype(np.uint8))
    img_mix = np.asarray(Image.blend(image, seg_image, 0.4))
    return img_mix


def run_video_visualization(video_path, MODEL, output_path):
    #     path='./image/20180604225051855.jpg'

    print('running deeplab on video %s...' % video_path)

    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        print('Please enter the right path:')
    video_frameNumber = vid.get(7)
    video_FourCC = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps = vid.get(cv2.CAP_PROP_FPS)
    video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    isOutput = True if output_path != "" else False
    if isOutput:
        print("!!! TYPE:", type(output_path), type(
            video_FourCC), type(video_fps), type(video_size))
        out = cv2.VideoWriter(output_path, fourcc, 15, (640, 360))
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    index = 0
    while True:

        return_value, frame = vid.read()
        if(return_value == False):
            break

        index += 1
        print("视频处理进度：", index/video_frameNumber*100, "%")
        image = Image.fromarray(frame)
        resized_im, seg_map = MODEL.run(image)
        result = segmentation(resized_im, seg_map)
        result = cv2.resize(result, (640, 360))
        # plt.imsave('./result/_color_image_'+str(index)+'.', result)
        curr_time = timer()
        exec_time = curr_time-prev_time
        prev_time = curr_time
        accum_time = accum_time+exec_time
        curr_fps = curr_fps+1
        fps = "FPS: "+str(curr_fps/accum_time)
        accum_time = 0
        curr_fps = 0
        cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 0, 0), thickness=2)
        # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        # cv2.imshow("result", result)
        if(isOutput):
            print("write")
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# ------------------------------------
if __name__ == '__main__':
    MODEL = DeepLabModel()
    print('model loaded successfully!')
    run_video_visualization(TEST_VIDEO_PATH, MODEL, './result/test_seg.avi')
