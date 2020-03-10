# @Author  :_kerman jt
# @Time    : 19-10-17 上午10:54

from marko import Markdown
from marko.ext.gfm import GFMExtension
from marko.ext.toc import TocExtension
from marko.ext.pangu import PanguExtension
from marko.ext.footnote import FootnoteExtension

from .extensions import BlogExtension

markdown = Markdown(
    extensions=[
        GFMExtension,
        PanguExtension,
        TocExtension,
        FootnoteExtension,
        BlogExtension,
    ]
)
