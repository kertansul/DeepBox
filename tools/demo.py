#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------
# --------------------------------------------------------
# Fast DeepBox
# Written by Weicheng Kuo, 2015.
# See LICENSE in the project root for license information.
# --------------------------------------------------------


import sys
sys.path.insert(0, '/home/Object-Proposal/src/DeepBox/caffe-fast-rcnn/python')
import caffe
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'src')))

from fast_dbox_config import cfg, cfg_from_file
import fast_dbox_test
import argparse
import pprint
import time
import pdb
def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Fast DeepBox demo....')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU id to use',
                        default=0, type=int)
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the network',
                        default='./models/DboxNet/test.prototxt', type=str)
    parser.add_argument('--net', dest='caffemodel',
                        help='model to test',
                        default='./output/default/coco_train2014/fast-dbox-multiscale.caffemodel', type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file', default=None, type=str)
    parser.add_argument('--wait', dest='wait',
                        help='wait until net file exists',
                        default=True, type=bool)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='dataset to test',
                        default='coco_val2014', type=str)
    parser.add_argument('--demo', dest='demo_quick',
                        help='Quick demo or not',
                        default=1, type=int)
    parser.add_argument('--frame', dest='frame',
                        help='frame # used in full COCO demo',
                        default=33, type=int)
    parser.add_argument('--numboxes', dest='num_boxes_vis',
                        help='number of boxes to visualize in demo',
                        default=5, type=int)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit() 
    
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)

    print('Using fast_dbox_config:')
    pprint.pprint(cfg)
    while not os.path.exists(args.caffemodel) and args.wait:
        print('Waiting for {} to exist...'.format(args.caffemodel))
        time.sleep(10)

    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    net = caffe.Net(args.prototxt, args.caffemodel, caffe.TEST)
    net.name = os.path.splitext(os.path.basename(args.caffemodel))[0]
    
    if args.demo_quick is 0:
        from datasets.factory import get_imdb
        imdb = get_imdb(args.imdb_name)
        fast_dbox_test.demo_net(net, imdb, args.frame, args.num_boxes_vis)
    else:
        fast_dbox_test.demo_net_quick(net,args.num_boxes_vis)
