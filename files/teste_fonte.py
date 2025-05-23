from moviepy.editor import TextClip

FONT_NAME = "ActiveHeart"  # Esse nome precisa estar listado no `convert -list font`

clip = TextClip(
    txt="Teste com ActiveHeart 💛",
    fontsize=100,
    color="yellow",
    font=FONT_NAME,
    size=(1080, None),
    method="caption",
    align="center"
).set_duration(5)

clip.save_frame("/home/n8n/files/teste_fonte.png", t=0)
print("✅ Imagem criada: /home/n8n/files/teste_font.png")

