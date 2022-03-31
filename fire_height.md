# Fire Height
Ways to figure out the fire height

## Calculating the Height
### Color
 - Another heuristic is that the red channel is likely much higher-signal than
   green and blue. This is because the edges of the flame are red (so high red)
   and the middle of the frame also has a high red (in addition to green and blue)

### Semantic Segmentation
 - K-means clustering can tell us which pixels belong to an "average" fire color
 - Problem: fire reflections would be included

### Difference between frames
 - Take advantage of the fact that the flame is the only moving part of
   the image.
 - We could try subtracting a frame without fire from a frame with fire
    - Problem: glow and shadows would also show pixel changes and merge
      with the fire.
 - We could also try subtracting a frame from the previous frame. This
   lets us select for fast-moving actions, like the flicker of a flame.
    - Should give us very good resolution. However, this technique will
      capture _any_ moving object, including non-flames (like
      reflections of researchers moving in the background)

### A Combination
 - The semantic segmentation based on color can tell us where the fire
   roughly is.
 - The frame differencing can give us the fire's edges but will give
   false positives.
 - Therefore, we can use the following signals to classify a pixel:
    - Velocity (from frame differencing)
    - Color (is it fire-like?)
    - Location (is it close to other high-confidence pixels?)

### Priorities
 - False positives can always be cut down by adding more signals/heuristics
   to the model. However, we cannot tolerate false negatives, as they can affect
   the data recording. 
    - Note that false positive is a non-flame pixel marked as flame, while
      false negative is a flame pixel marked as non-flame
 - We want to prioritize recall in the higher part of the flame, as that is used
   to calculate the flame height. We also want to aggressively remove false
   positives in that region to keep the data intact.
 - If we have false negatives in the inner/lower part of the flame, that may be
   acceptable, since it isn't used to calculate flame height.

## Further processing
 - We can then compute the height of the flame in pixels and select the
   frame with the highest pixeled flame height.
 - After selecting a frame, we can give it to the analyst to convert to
   normal units
 - There should be a way to measure uncertainty and choose multiple
   candidates. This way, the analyst can choose between, say, 5 frames
   rather than a massive number. Perhaps present the analyst with a
   "higher or lower?" set of questions.

## User Experience
 - Researchers should be shown the original flame along with the probability
   map used to calculate the flame height. This way, they can spot any obvious
   errors before recording
