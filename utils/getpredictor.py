def get_predictor():
    '''
    Generate a Detectron2 predictor object for getting the bounding boxes.
    Requires no arguments.
    '''
    cfg=get_cfg()
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))

    cfg.SOLVER.BASE_LR = 0.001
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS=False

    cfg.SOLVER.WARMUP_ITERS = 1000
    cfg.SOLVER.MAX_ITER = 2500 
    cfg.SOLVER.STEPS = (1000, 1500)
    cfg.SOLVER.GAMMA = 0.05
    #cfg.MODEL.DEVICE="cpu"                    #uncomment this line if running on a device which does not have a gpu or does not support cuda


    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 64
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3 #your number of classes + 1

    cfg.TEST.EVAL_PERIOD = 500
    cfg.MODEL.WEIGHTS ="/content/model_final_3200.pth"                    #path to the weights to be used for generating the predictor can be set here
    cfg.DATASETS.TEST=("test",)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9   
    return DefaultPredictor(cfg)