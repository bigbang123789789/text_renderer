import os
from pathlib import Path
import imgaug.augmenters as iaa
import text_renderer
from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    SimpleTextColorCfg,
    UniformPerspectiveTransformCfg,
)
from text_renderer.effect.curve import Curve

CURRENT_DIR = Path('/content/text_renderer/workspace')

text_effect_cfg = Effects([
    text_renderer.effect.DropoutRand(p=0.1,dropout_p=(0.1, 0.2)), #Drop pixel
    Curve(p=0.2, period=180, amplitude=(7,8)), # Curve
    Line(p=0.1, thickness=(2, 5),line_pos_p=(0, 1, 0, 0, 0, 0, 0, 0, 0, 0)),  #Underline
    ImgAugEffect(p=0.1,aug=iaa.GaussianBlur(sigma=(0.5, 0.85))),   #Gaussian Blur
    Padding(p=1, w_ratio=[0.015, 0.021], h_ratio=[0.15, 0.16], center=True), #Add padding
])

extra_text_effect_cfg = Effects([
    
])


my_corpus = CharCorpus(
    CharCorpusCfg(
        text_paths=[CURRENT_DIR / "corpus" / "jp_text.txt"],
        length=(3,39),
        font_size=(35, 68),

        font_dir=CURRENT_DIR / "font",
        text_color_cfg=SimpleTextColorCfg(alpha=(110, 255)),
        char_spacing = (-0.1, 0.3),

        # horizontal= False  # horizontal
    ),
)

def story_data():
    return GeneratorCfg(
        num_image=10,
        save_dir=CURRENT_DIR / "output",
        render_cfg=RenderCfg(
              corpus= [my_corpus, my_corpus],
              corpus_effects=[text_effect_cfg, extra_text_effect_cfg],
              bg_dir=CURRENT_DIR / "bg",
              layout=text_renderer.layout.ExtraTextLineLayout(bottom_prob=0.5),
              perspective_transform=UniformPerspectiveTransformCfg(12, 12, 1.2), # rotate
              # render_effects=bg_effect_cfg
              text_color_cfg=SimpleTextColorCfg(),
              height=70,
              gray=False,
              return_bg_and_mask=False
          ),
    )

configs = [story_data()]
