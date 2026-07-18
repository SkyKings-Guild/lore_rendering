from lore import sync_render

img = sync_render(
    "Hello, World!\nTesting!\nNANANANANANANNANANANANANANNA",
    generate_gif=False,
    background_style="very_special",
    return_io=False,
)
with open("test.png", "wb") as f:
    f.write(img)