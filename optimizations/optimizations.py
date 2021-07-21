from detectron2.structures import Boxes,Instances
def suppress_multiple(outputs):
    '''Adjust the boundaries of output boxes so that they do not have any intersection
    Outputs should be an instance of the predictions of the detectron2 predictor
    Example: 
    predictor=get_predictor()
    outputs=predictor(image)
    suppress_multiple(outputs)
    '''
    temp=outputs['instances']
    boxes=temp.get_fields()['pred_boxes'].tensor.cpu().numpy()
    classes=temp.get_fields()['pred_classes'].cpu().numpy()

    #x1 y1 x2 y2 top-left bottom-right
    boxes=sorted(zip(boxes,classes),key=lambda t:t[0][1])
    classes=[i[1] for i in boxes]
    boxes=[i[0] for i in boxes]

    for i in range(len(boxes)):
        for j in range(i+1,(len(boxes))):
            if boxes[i][3]>boxes[j][1]:
                if boxes[i][0]>boxes[j][0] and boxes[i][0]<boxes[j][2]:
                    boxes[i][3]=boxes[j][1]
                elif boxes[i][2]>boxes[j][0] and boxes[i][2]<boxes[j][2]:
                    boxes[i][3]=boxes[j][1]
                elif boxes[j][0]>boxes[i][0] and boxes[j][0]<boxes[i][2]:
                    boxes[i][3]=boxes[j][1]
    tbox=torch.tensor(boxes)
    tclass=torch.tensor(classes)
    outputs['instances'].get_fields()['pred_boxes']=Boxes(tbox)
    outputs['instances'].get_fields()['pred_classes']=tclass


def merge_close(outputs):
    '''
    Merge boxes which are very close to each other
    Outputs should be an instance of the predictions of the detectron2 predictor
    Example: 
    predictor=get_predictor()
    outputs=predictor(image)
    merge_close(outputs)
    '''
    temp=outputs['instances']
    boxes=temp.get_fields()['pred_boxes'].tensor.cpu().numpy()
    classes=temp.get_fields()['pred_classes'].cpu().numpy()
    #x1 y1 x2 y2 top-left bottom-right
    boxes=sorted(zip(boxes,classes),key=lambda t:t[0][1])
    classes=[i[1] for i in boxes]
    boxes=[i[0] for i in boxes]
    newboxes=[]
    newclasses=[]
    finalboxes=[]
    finalclasses=[]
    newlist=[]
    orig=len(boxes)
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            '''
            Condition for merging two boxes can be changed here.
            Setting the values of the absolute differences lower will stricten the condition while increasing them will relax the required closeness.
            '''
            if  abs(boxes[i][3] - boxes[j][1]) < 60 and abs(boxes[i][2]-boxes[j][2])<25 and abs(boxes[i][0]-boxes[j][0])<25 and classes[i]==classes[j]: 
                newx1=min(boxes[i][0],boxes[j][0])
                newy1=min(boxes[i][1],boxes[j][1])
                newx2=max(boxes[i][2],boxes[j][2])
                newy2=max(boxes[i][3],boxes[j][3])
                newboxes.append([newx1,newy1,newx2,newy2])
                newclasses.append(classes[i])
                newlist+=[i,j]
    for i in range(len(boxes)):
        if i not in newlist:
            finalboxes.append(boxes[i])
            finalclasses.append(classes[i])
    for i in range(len(newboxes)):
        finalboxes.append(newboxes[i])
        finalclasses.append(newclasses[i])
        finalboxes.append([0,0,0,0])
        finalclasses.append(1)
    tt=outputs['instances']
    tbox=torch.tensor(finalboxes)
    tclass=torch.tensor(finalclasses)
    outputs['instances']=tt
    outputs['instances'].get_fields()['pred_boxes']=Boxes(tbox)
    outputs['instances'].get_fields()['pred_classes']=tclass
    
