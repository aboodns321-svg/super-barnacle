# fill-names

Fills the staff names into the last slide of the Madrasati activation video
(`madrasati-activation-guide.mp4`). The original labels ("مديرة المدرسة :",
"مسؤولة منصة مدرستي :") are kept as-is from the source frames; only the names
are rendered, in Mada Bold (Google Fonts, OFL), and they follow the original
zoom/fade-in of the slide's text.

```
python3 render.py <source.mp4> <clean-final-frame.png> <Mada-Bold.ttf> <out.mp4>
```

Names and layout constants live in `block.py`.
