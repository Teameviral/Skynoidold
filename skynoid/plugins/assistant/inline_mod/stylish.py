from skynoid.plugins.stylish import bubbles
from skynoid.plugins.stylish import bubblesblack
from skynoid.plugins.stylish import CHAR_OVER
from skynoid.plugins.stylish import CHAR_POINTS
from skynoid.plugins.stylish import CHAR_STRIKE
from skynoid.plugins.stylish import CHAR_UNDER
from skynoid.plugins.stylish import formatting_text_inline
from skynoid.plugins.stylish import graffiti
from skynoid.plugins.stylish import graffitib
from skynoid.plugins.stylish import handwriting
from skynoid.plugins.stylish import handwritingb
from skynoid.plugins.stylish import smallcaps
from skynoid.plugins.stylish import smothtext
from skynoid.plugins.stylish import subscript
from skynoid.plugins.stylish import superscript
from skynoid.plugins.stylish import text_style_generator
from skynoid.plugins.stylish import upsidedown_text_inline
from skynoid.plugins.stylish import wide
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent


async def stylish_func(text, answers):
    upside = upsidedown_text_inline(text)
    answers.append(
        InlineQueryResultArticle(
            title=upside,
            description='Upside-down Text',
            input_message_content=InputTextMessageContent(upside),
        ),
    )
    over = text_style_generator(text, CHAR_OVER)
    answers.append(
        InlineQueryResultArticle(
            title=over,
            description='Overline Text',
            input_message_content=InputTextMessageContent(over),
        ),
    )
    under = text_style_generator(text, CHAR_UNDER)
    answers.append(
        InlineQueryResultArticle(
            title=under,
            description='Underline Text',
            input_message_content=InputTextMessageContent(under),
        ),
    )
    strike = text_style_generator(text, CHAR_STRIKE)
    answers.append(
        InlineQueryResultArticle(
            title=strike,
            description='Strike Text',
            input_message_content=InputTextMessageContent(strike),
        ),
    )
    points = text_style_generator(text, CHAR_POINTS)
    answers.append(
        InlineQueryResultArticle(
            title=points,
            description='Points Text',
            input_message_content=InputTextMessageContent(points),
        ),
    )
    smallcaps_conv = formatting_text_inline(text, smallcaps)
    answers.append(
        InlineQueryResultArticle(
            title=smallcaps_conv,
            description='Smallcaps Text',
            input_message_content=InputTextMessageContent(smallcaps_conv),
        ),
    )
    super_script = formatting_text_inline(text, superscript)
    answers.append(
        InlineQueryResultArticle(
            title=super_script,
            description='Superscript Text',
            input_message_content=InputTextMessageContent(super_script),
        ),
    )
    sub_script = formatting_text_inline(text, subscript)
    answers.append(
        InlineQueryResultArticle(
            title=sub_script,
            description='Subscript Text',
            input_message_content=InputTextMessageContent(sub_script),
        ),
    )
    wide_text = formatting_text_inline(text, wide)
    answers.append(
        InlineQueryResultArticle(
            title=wide_text,
            description='Wide Text',
            input_message_content=InputTextMessageContent(wide_text),
        ),
    )
    bubbles_text = formatting_text_inline(text, bubbles)
    answers.append(
        InlineQueryResultArticle(
            title=bubbles_text,
            description='Bubbles Text',
            input_message_content=InputTextMessageContent(bubbles_text),
        ),
    )
    bubblesblack_text = formatting_text_inline(text, bubblesblack)
    answers.append(
        InlineQueryResultArticle(
            title=bubblesblack_text,
            description='Bubbles Black Text',
            input_message_content=InputTextMessageContent(
                bubblesblack_text,
            ),
        ),
    )
    smoth_text = formatting_text_inline(text, smothtext)
    answers.append(
        InlineQueryResultArticle(
            title=smoth_text,
            description='Smoth Text',
            input_message_content=InputTextMessageContent(smoth_text),
        ),
    )

    graffiti_text = formatting_text_inline(text, graffiti)
    answers.append(
        InlineQueryResultArticle(
            title=graffiti_text,
            description='Graffiti Text',
            input_message_content=InputTextMessageContent(graffiti_text),
        ),
    )
    graffitib_text = formatting_text_inline(text, graffitib)
    answers.append(
        InlineQueryResultArticle(
            title=graffitib_text,
            description='Graffiti Bold Text',
            input_message_content=InputTextMessageContent(graffitib_text),
        ),
    )
    handwriting_text = formatting_text_inline(text, handwriting)
    answers.append(
        InlineQueryResultArticle(
            title=handwriting_text,
            description='Handwriting Text',
            input_message_content=InputTextMessageContent(
                handwriting_text,
            ),
        ),
    )
    handwritingb_text = formatting_text_inline(text, handwritingb)
    answers.append(
        InlineQueryResultArticle(
            title=handwritingb_text,
            description='Handwriting Bold Text',
            input_message_content=InputTextMessageContent(
                handwritingb_text,
            ),
        ),
    )
