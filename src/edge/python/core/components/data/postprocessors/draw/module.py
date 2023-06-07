import cv2
import numpy as np
from abstract_postprocessor import AbstractPostprocessor
from common.config import CONFIG
from common.exceptions import InvalidBoundTypeException, MalformedOutputException


class Postprocessor(AbstractPostprocessor):

    def __init__(self, **kwargs):
        """Initialize drawing postprocessor module."""
        self.thickness = 2
        self._detection_type = CONFIG["inference"]["detection_type"]
        self._segmentation_type = CONFIG["inference"][
            "segmentation_type"] if "segmentation_type" in CONFIG[
                "inference"] else None
        self._bbox_format = CONFIG["inference"][
            "bbox_format"] if self._detection_type == "object_detection" else None
        super().__init__(**kwargs)

    def run(self, assets):
        """Run drawing postprocessor module.
        Args:
            assets: Dictionary of assets.

        Raises:
            InvalidBoundTypeException: Unsupported bound type.
            MalformedOutputException: Output is malformed.
        """
        try:
            if self._detection_type == "object_detection":
                frame = self._draw_bbox(assets)
            elif self._detection_type == "segmentation":
                if self._segmentation_type == "semantic":
                    frame = self._draw_semantic_mask(assets)
                else:
                    frame = self._draw_instance_mask(assets)
            else:
                raise InvalidBoundTypeException("Unsupported bound type!")
            assets["output_frame"] = frame
        except Exception as exc:
            raise MalformedOutputException(exc) from exc

    def _draw_bbox(self, assets):
        """Draw bounding boxes on frame.

        Args:
            assets: Dictionary of assets.

        Returns:
            Frame with bounding boxes drawn.
        """
        frame = cv2.cvtColor(assets["orig_frame"].copy(), cv2.COLOR_RGB2BGR)
        frame = np.array(frame)
        orig_shape = assets["orig_shape"]
        category_index = assets["category_index"]

        if self._bbox_format:
            for each_bbox, each_class, each_score in zip(
                    assets["predictions"]["boxes"],
                    assets["predictions"]["classes"],
                    assets["predictions"]["scores"]):
                color = assets["color_map"].get(each_class - 1)

                # Draw bbox on screen
                cv2.rectangle(
                    frame,
                    (
                        int(each_bbox[self._bbox_format.index("xmin")] *
                            orig_shape[1]),
                        int(each_bbox[self._bbox_format.index("ymin")] *
                            orig_shape[0]),
                    ),
                    (
                        int(each_bbox[self._bbox_format.index("xmax")] *
                            orig_shape[1]),
                        int(each_bbox[self._bbox_format.index("ymax")] *
                            orig_shape[0]),
                    ),
                    color,
                    self.thickness,
                )
                # Draw label background
                cv2.rectangle(
                    frame,
                    (
                        int(each_bbox[self._bbox_format.index("xmin")] *
                            orig_shape[1]),
                        int(each_bbox[self._bbox_format.index("ymax")] *
                            orig_shape[0]),
                    ),
                    (
                        int(each_bbox[self._bbox_format.index("xmax")] *
                            orig_shape[1]),
                        int(each_bbox[self._bbox_format.index("ymax")] *
                            orig_shape[0] + 15),
                    ),
                    color,
                    thickness=-1,
                )
                cv2.putText(
                    frame,
                    f"Class: {category_index[int(each_class)]['name']},"
                    f"Score: {str(round(each_score, 2))}",
                    (
                        int(each_bbox[self._bbox_format.index("xmin")] *
                            orig_shape[1]),
                        int(each_bbox[self._bbox_format.index("ymax")] *
                            orig_shape[0] + 10),
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
        return frame

    def _draw_polygon(self, assets):
        """Draw polygon masks on frame.

        Args:
            assets: Dictionary of assets.

        Returns:
            Frame with polygon masks drawn.
        """
        frame = cv2.cvtColor(assets["orig_frame"].copy(), cv2.COLOR_RGB2BGR)
        frame = np.array(frame)
        alpha = 0.5

        for each_mask, each_class in zip(assets["predictions"]["masks"],
                                         assets["predictions"]["classes"]):
            colors = assets["color_map"].get(each_class - 1)
            for color in range(3):
                frame[:, :, color] = np.where(
                    each_mask == 1,
                    frame[:, :, color] * (1 - alpha) + alpha * colors[color],
                    frame[:, :, color],
                )
        return self._draw_bbox(assets)

    def _draw_semantic_mask(self, assets):
        """Draw pixel masks on frame.

        Args:
            assets: Dictionary of assets.

        Returns:
            Frame with pixel masks drawn.
        """
        frame = cv2.cvtColor(assets["orig_frame"].copy(),
                             cv2.COLOR_RGB2BGR).astype(np.int64)
        output_mask = cv2.resize(
            assets["predictions"]["mask"],
            (assets["orig_shape"][1], assets["orig_shape"][0]))
        frame += output_mask.astype(np.int64)
        frame = np.clip(frame, 0, 255)
        frame = frame.astype(np.uint8)
        return frame

    def _draw_instance_mask(self, assets):
        frame = cv2.cvtColor(assets["orig_frame"].copy(),
                             cv2.COLOR_RGB2BGR).astype(np.int64)
        for each_mask, each_bbox in zip(assets["predictions"]["masks"],
                                        assets["predictions"]["boxes"]):
            mask = np.expand_dims(each_mask, -1)
            mask = np.tile(mask, 3)
            mask *= 255
            mask = np.clip(mask, 0, 255).astype(np.uint8)
            xmin, ymin, xmax, ymax = each_bbox
            ymin = int(ymin * assets["orig_shape"][1])
            ymax = int(ymax * assets["orig_shape"][1])
            xmin = int(xmin * assets["orig_shape"][0])
            xmax = int(xmax * assets["orig_shape"][0])
            mask_height = ymax - ymin
            mask_width = xmax - xmin
            mask = cv2.resize(mask, (mask_height, mask_width))
            resized_mask = np.zeros(assets["orig_shape"])
            resized_mask[xmin:xmax, ymin:ymax, :] = mask
            frame += resized_mask.astype(np.int64)
            frame = np.clip(frame, 0, 255)
        return frame
