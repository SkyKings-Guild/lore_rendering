import asyncio
import io

from .item_gen import render as raw_render

__all__ = (
    'sync_render',
    'render',
)


def sync_render(text):
    to_pass = text.splitlines()
    image, images = raw_render(to_pass)
    saved = io.BytesIO()
    if not images:
        image.save(saved, format='png')
    else:
        image.save(saved, format='gif', append_images=images, save_all=True, duration=75, loop=0)
    saved.seek(0)
    return saved


async def render(text, *, loop=None):
    loop = loop or asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_render, text)
