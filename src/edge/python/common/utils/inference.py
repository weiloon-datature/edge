#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   inference.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Inference helper functions.
"""

import copy

import numpy as np
import torch
import torchvision
from scipy.special import expit


def yolo_decode(
    prediction,
    anchors,
    num_classes,
    input_shape,
):
    """Decode final layer features to bounding box parameters."""
    batch_size = np.shape(prediction)[0]
    num_anchors = len(anchors)
    grid_shape = np.shape(prediction)[1:3]

    # Check if stride on height & width are same
    assert (input_shape[0] // grid_shape[0] == input_shape[1] //
            grid_shape[1]), "model stride mismatch."

    prediction = np.reshape(
        prediction,
        (
            batch_size,
            grid_shape[0] * grid_shape[1] * num_anchors,
            num_classes + 5,
        ),
    )

    # Generate x_y_offset grid map
    grid_y = np.arange(grid_shape[0])
    grid_x = np.arange(grid_shape[1])
    x_offset, y_offset = np.meshgrid(grid_x, grid_y)

    x_offset = np.reshape(x_offset, (-1, 1))
    y_offset = np.reshape(y_offset, (-1, 1))

    x_y_offset = np.concatenate((x_offset, y_offset), axis=1)
    x_y_offset = np.tile(x_y_offset, (1, num_anchors))
    x_y_offset = np.reshape(x_y_offset, (-1, 2))
    x_y_offset = np.expand_dims(x_y_offset, 0)

    # Log space transform of the height and width
    anchors = np.tile(anchors, (grid_shape[0] * grid_shape[1], 1))
    anchors = np.expand_dims(anchors, 0)

    # Eliminate grid sensitivity
    box_xy = (expit(prediction[..., :2]) +
              x_y_offset) / np.array(grid_shape)[::-1]

    box_wh = (np.exp(prediction[..., 2:4]) *
              anchors) / np.array(input_shape)[::-1]

    # Sigmoid objectness scores
    objectness = expit(prediction[..., 4])
    objectness = np.expand_dims(objectness, -1)

    # Sigmoid class scores
    class_scores = expit(prediction[..., 5:])

    return np.concatenate([box_xy, box_wh, objectness, class_scores], axis=2)


def yolov3v4_decode(
    predictions,
    anchors,
    num_classes,
    input_shape,
):
    """
    YOLOv3/v4 Head to process predictions from YOLOv3/v4 models

    Args:
        num_classes: Total number of classes
        anchors: YOLO style anchor list for bounding box assignment
        input_shape: Input shape of the image
        predictions: A list of three tensors with shape
            (N, 19, 19, 255), (N, 38, 38, 255) and (N, 76, 76, 255)

    Returns:
        A tensor with the shape (N, num_boxes, 85)
    """
    assert (len(predictions) == len(anchors) //
            3), "Anchor numbers does not match prediction."

    if len(predictions) == 3:
        anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
    elif len(predictions) == 2:
        anchor_mask = [[3, 4, 5], [0, 1, 2]]
    else:
        raise ValueError(f"Unsupported prediction length: {len(predictions)}")

    results = []

    for idx, prediction in enumerate(predictions):
        results.append(
            yolo_decode(
                prediction,
                anchors[anchor_mask[idx]],
                num_classes,
                input_shape,
            ))

    return np.concatenate(results, axis=1)


def yolo_correct_boxes(predictions, img_shape, model_input_shape):
    """Rescale predicition boxes back to original image shape"""
    box_xy = predictions[..., :2]
    box_wh = predictions[..., 2:4]
    objectness = np.expand_dims(predictions[..., 4], -1)
    class_scores = predictions[..., 5:]

    # Model_input_shape & image_shape should be (height, width) format
    model_input_shape = np.array(model_input_shape, dtype="float32")
    image_shape = np.array(img_shape, dtype="float32")

    new_shape = np.round(image_shape * np.min(model_input_shape / image_shape))
    offset = (model_input_shape - new_shape) / 2.0 / model_input_shape
    scale = model_input_shape / new_shape
    # Reverse offset/scale to match (w,h) order
    offset = offset[..., ::-1]
    scale = scale[..., ::-1]

    box_xy = (box_xy - offset) * scale
    box_wh *= scale

    # Convert centoids to top left coordinates
    box_xy -= box_wh / 2

    # Scale boxes back to original image shape.
    image_wh = image_shape[..., ::-1]
    box_xy *= image_wh
    box_wh *= image_wh

    return np.concatenate([box_xy, box_wh, objectness, class_scores], axis=2)


def box_diou(boxes):
    """
    Calculate DIoU value of 1st box with other boxes of a box array
    Reference Paper:
        "Distance-IoU Loss: Faster and Better Learning for Bounding Box
        Regression" https://arxiv.org/abs/1911.08287

    Args:
        boxes: bbox numpy array, shape=(N, 4), xywh
            x,y are top left coordinates

    Returns:
        diou: numpy array, shape=(N-1,)
            IoU value of boxes[1:] with boxes[0]
    """
    # get box coordinate and area
    x_pos = boxes[:, 0]
    y_pos = boxes[:, 1]
    wid = boxes[:, 2]
    hei = boxes[:, 3]
    areas = wid * hei

    # check IoU
    inter_xmin = np.maximum(x_pos[1:], x_pos[0])
    inter_ymin = np.maximum(y_pos[1:], y_pos[0])
    inter_xmax = np.minimum(x_pos[1:] + wid[1:], x_pos[0] + wid[0])
    inter_ymax = np.minimum(y_pos[1:] + hei[1:], y_pos[0] + hei[0])

    inter_w = np.maximum(0.0, inter_xmax - inter_xmin + 1)
    inter_h = np.maximum(0.0, inter_ymax - inter_ymin + 1)

    inter = inter_w * inter_h
    iou = inter / (areas[1:] + areas[0] - inter)

    # box center distance
    x_center = x_pos + wid / 2
    y_center = y_pos + hei / 2
    center_distance = np.power(x_center[1:] - x_center[0], 2) + np.power(
        y_center[1:] - y_center[0], 2)

    # get enclosed area
    enclose_xmin = np.minimum(x_pos[1:], x_pos[0])
    enclose_ymin = np.minimum(y_pos[1:], y_pos[0])
    enclose_xmax = np.maximum(x_pos[1:] + wid[1:], x_pos[0] + wid[0])
    enclose_ymax = np.maximum(y_pos[1:] + wid[1:], y_pos[0] + wid[0])
    enclose_w = np.maximum(0.0, enclose_xmax - enclose_xmin + 1)
    enclose_h = np.maximum(0.0, enclose_ymax - enclose_ymin + 1)
    # get enclosed diagonal distance
    enclose_diagonal = np.power(enclose_w, 2) + np.power(enclose_h, 2)
    # calculate DIoU, add epsilon in denominator to avoid dividing by 0
    diou = iou - 1.0 * (center_distance) / (enclose_diagonal +
                                            np.finfo(float).eps)

    return diou


def nms_boxes(
    boxes,
    classes,
    scores,
    iou_threshold,
    confidence=0.1,
    sigma=0.5,
):
    """Carry out non-max supression on the detected bboxes"""
    is_soft = False
    use_exp = False

    nboxes, nclasses, nscores = [], [], []
    for cls in set(classes):
        # handle data for one class
        inds = np.where(classes == cls)
        bbx = boxes[inds]
        cls = classes[inds]
        sco = scores[inds]

        # make a data copy to avoid breaking
        # during nms operation
        b_nms = copy.deepcopy(bbx)
        c_nms = copy.deepcopy(cls)
        s_nms = copy.deepcopy(sco)

        while len(s_nms) > 0:
            # pick the max box and store, here
            # we also use copy to persist result
            i = np.argmax(s_nms, axis=-1)
            nboxes.append(copy.deepcopy(b_nms[i]))
            nclasses.append(copy.deepcopy(c_nms[i]))
            nscores.append(copy.deepcopy(s_nms[i]))

            # swap the max line and first line
            b_nms[[i, 0], :] = b_nms[[0, i], :]
            c_nms[[i, 0]] = c_nms[[0, i]]
            s_nms[[i, 0]] = s_nms[[0, i]]

            iou = box_diou(b_nms)

            # drop the last line since it has been record
            b_nms = b_nms[1:]
            c_nms = c_nms[1:]
            s_nms = s_nms[1:]

            if is_soft:
                # Soft-NMS
                if use_exp:
                    # score refresh formula:
                    # score = score * exp(-(iou^2)/sigma)
                    s_nms = s_nms * np.exp(-(iou * iou) / sigma)
                else:
                    # score refresh formula:
                    # score = score * (1 - iou) if iou > threshold
                    depress_mask = np.where(iou > iou_threshold)[0]
                    s_nms[depress_mask] = s_nms[depress_mask] * (
                        1 - iou[depress_mask])
                keep_mask = np.where(s_nms >= confidence)[0]
            else:
                # normal Hard-NMS
                keep_mask = np.where(iou <= iou_threshold)[0]

            # keep needed box for next loop
            b_nms = b_nms[keep_mask]
            c_nms = c_nms[keep_mask]
            s_nms = s_nms[keep_mask]

    # reformat result for output
    nboxes = np.array(nboxes)
    nclasses = np.array(nclasses)
    nscores = np.array(nscores)
    return nboxes, nclasses, nscores


def filter_boxes(boxes, classes, scores, max_boxes):
    """Sort the prediction boxes according to score
    and only pick top "max_boxes" ones
    """
    # sort result according to scores
    sorted_indices = np.argsort(scores)
    sorted_indices = sorted_indices[::-1]
    nboxes = boxes[sorted_indices]
    nclasses = classes[sorted_indices]
    nscores = scores[sorted_indices]

    # only pick max_boxes
    nboxes = nboxes[:max_boxes]
    nclasses = nclasses[:max_boxes]
    nscores = nscores[:max_boxes]

    return nboxes, nclasses, nscores


def yolo_handle_predictions(predictions,
                            num_classes,
                            max_boxes=100,
                            confidence=0.1,
                            iou_threshold=0.4):
    """Apply NMS algorithm & filter top max boxes."""
    boxes = predictions[:, :, :4]
    box_confidences = np.expand_dims(predictions[:, :, 4], -1)
    box_class_probs = predictions[:, :, 5:]

    # Check if only 1 class for different score
    if num_classes == 1:
        box_scores = box_confidences
    else:
        box_scores = box_confidences * box_class_probs

    # Filter boxes with score threshold
    box_classes = np.argmax(box_scores, axis=-1)
    box_class_scores = np.max(box_scores, axis=-1)
    pos = np.where(box_class_scores >= float(confidence))

    boxes = boxes[pos]
    classes = box_classes[pos]
    scores = box_class_scores[pos]

    # Boxes, Classes and Scores returned from NMS
    n_boxes, n_classes, n_scores = nms_boxes(
        boxes,
        classes,
        scores,
        iou_threshold,
    )

    if n_boxes:
        boxes = np.concatenate(n_boxes)
        classes = np.concatenate(n_classes).astype("int32")
        scores = np.concatenate(n_scores)
        boxes, classes, scores = filter_boxes(boxes, classes, scores,
                                              max_boxes)

        return boxes, classes, scores

    return [], [], []


def yolo_adjust_boxes(boxes, img_shape):
    """Change box format from (x,y,w,h) top left coordinate to
    (xmin,ymin,xmax,ymax) format
    """
    if boxes is None or len(boxes) == 0:
        return []

    image_shape = np.array(img_shape, dtype="float32")
    height, width = image_shape

    adjusted_boxes = []
    for box in boxes:
        x_coord, y_coord, box_width, box_height = box

        xmin = min(max(0, x_coord / width), 1)
        ymin = min(max(0, y_coord / height), 1)
        xmax = min(max(xmin, (x_coord + box_width) / width), 1)
        ymax = min(max(ymin, (y_coord + box_height) / height), 1)

        adjusted_boxes.append([xmin, ymin, xmax, ymax])

    return np.array(adjusted_boxes, dtype=np.float32)


def yolov3v4_postprocess(
    yolo_outputs,
    image_shape,
    anchors,
    num_classes,
    model_input_shape,
    max_boxes=100,
    confidence=0.1,
    iou_threshold=0.4,
):
    """Postprocess YOLOv3 or YOLOv4 output."""
    predictions = yolov3v4_decode(
        yolo_outputs,
        anchors,
        num_classes,
        input_shape=model_input_shape,
    )

    predictions = yolo_correct_boxes(predictions, image_shape,
                                     model_input_shape)

    boxes, classes, scores = yolo_handle_predictions(
        predictions,
        num_classes,
        max_boxes=max_boxes,
        confidence=confidence,
        iou_threshold=iou_threshold,
    )

    boxes = yolo_adjust_boxes(boxes, image_shape)

    return boxes, classes, scores


def yolo_postprocess(prediction,
                     num_classes,
                     conf_thre=0.7,
                     nms_thre=0.45,
                     class_agnostic=False):
    """Postprocess YOLOX output."""
    prediction = torch.Tensor(prediction)
    box_corner = prediction.new(prediction.shape)
    box_corner[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
    box_corner[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
    box_corner[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
    box_corner[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
    prediction[:, :, :4] = box_corner[:, :, :4]

    output = [None for _ in range(len(prediction))]
    for i, image_pred in enumerate(prediction):
        # If none are remaining => process next image
        if not image_pred.size(0):
            continue
        # Get score and class with highest confidence
        class_conf, class_pred = torch.max(image_pred[:, 5:5 + num_classes],
                                           1,
                                           keepdim=True)

        conf_mask = (image_pred[:, 4] * class_conf.squeeze() >=
                     conf_thre).squeeze()
        # Detections ordered as
        # (x1, y1, x2, y2, obj_conf, class_conf, class_pred)
        detections = torch.cat(
            (image_pred[:, :5], class_conf, class_pred.float()), 1)
        detections = detections[conf_mask]
        if not detections.size(0):
            continue

        if class_agnostic:
            nms_out_index = torchvision.ops.nms(
                detections[:, :4],
                detections[:, 4] * detections[:, 5],
                nms_thre,
            )
        else:
            nms_out_index = torchvision.ops.batched_nms(
                detections[:, :4],
                detections[:, 4] * detections[:, 5],
                detections[:, 6],
                nms_thre,
            )

        detections = detections[nms_out_index]
        if output[i] is None:
            output[i] = detections  # type: ignore
        else:
            output[i] = torch.cat((output[i], detections))  # type: ignore

    return output


def get_instance_mask(mask: np.ndarray, lab: int,
                      threshold: float) -> np.ndarray:
    """Convert class mask to instance mask"""
    instance_mask = np.zeros_like(mask, np.uint8)
    instance_mask[np.where(mask > threshold)] = lab + 1
    return instance_mask


def get_binary_mask(mask: np.ndarray) -> np.ndarray:
    """Convert class mask to binary mask"""
    binary_mask = np.zeros_like(mask[0], np.uint8)
    for class_id, class_mask in enumerate(mask):
        if class_id > 0:
            binary_mask[np.where(class_mask > 0.0)] = class_id
    return binary_mask
