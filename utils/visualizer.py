def visualize(im,predictor):
    '''
    For displaying the bounding boxes on the image given (im) by the Detectron2 predictor object (predictor)
    '''
    outputs=predictor(im)
    merge_close(outputs)
    suppress_multiple(outputs)
    merge_close(outputs)
    v = Visualizer(im[:, :, ::-1],metadata=test_metadata,scale=0.8)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2_imshow(out.get_image()[:, :, ::-1])            #use cv2_imshow if running on colab else use cv2.imshow('temp',out.get_image()[:,:,::-1])
