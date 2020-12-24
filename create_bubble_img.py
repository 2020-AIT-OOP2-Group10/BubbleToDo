import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os
import glob
from PIL import Image, ImageDraw, ImageFilter
from datetime import datetime as dt
import json

##　About バブルに貼り付ける画像を作成するプログラム

def create_bubble_img(content_text:str, date:str, color_code:str):

    #フォントをしていするためにメイリオをファイルで読み込む
    font_path = "meiryo.ttc"

    # date_format == "2020/12/10"
    content_date = date.split("/")

    # 経過した日付を確定
    now = dt.now()
    elapsed_time = (dt(now.year,now.month,now.day)-dt(int(content_date[0]),int(content_date[1]),int(content_date[2]))).days

    # elapsed_timeは正の値の場合は今日の日付と比較して過ぎている（値が大きくなればなるほど）
    # 負の値の場合は今日の日付と比較して期限がまだ来ていない（値が小さくなればなるほど）
    # バブルのサイズは100~400とし、一日ごとに10大きくなる(当日で最大、30日で最小となる)
    thumb_width = min(max(400 + elapsed_time * 10, 100), 400)
    canvasSize = (thumb_width, thumb_width)
    fixsize = thumb_width/100
    if fixsize == 0:
        fontsize = 100 - 70
    else:
        fontsize = thumb_width - 70*int(fixsize)

    # 使うフォント,描くテキストの設定(先頭から三文字)
    ttfontname = font_path

    if len(content_text) < 3:
        text = content_text
    else:
        text = content_text[:3]

    # 背景色決定（引数から）
    rgb_data = []
    rgb_data += [int(color_code[1:3],16),int(color_code[3:5],16),int(color_code[5:7],16)]
    # print(int(color_code[1:3],16),int(color_code[3:5],16),int(color_code[5:7],16))
    backgroundRGB = (int(color_code[1:3],16),int(color_code[3:5],16),int(color_code[5:7],16))

    #フォントの色を設定(補色)
    # 全部黒だったら文字色は白にする　（白なら黒）
    if rgb_data[0] == 255 and rgb_data[1] == 255 and rgb_data[2] == 255:
        textRGB = (0,0,0)
    elif rgb_data[0] == 0 and rgb_data[1] == 0 and rgb_data[2] == 0:
        textRGB = (255,255,255)
    else:
        # 補色の計算
        base_num = max(rgb_data) + min(rgb_data)
        textRGB       = (base_num-rgb_data[0],base_num-rgb_data[1],base_num-rgb_data[2])


    # 文字を描く画像の作成
    im  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(im)

    # 用意した画像に文字列を描く
    font = PIL.ImageFont.truetype(ttfontname, fontsize)
    textWidth, textHeight = draw.textsize(text,font=font)
    # フォントの位置決定場
    # textTopLeft = (canvasSize[0]/2 - (textWidth * len(text)) / 2, canvasSize[1]//2-textHeight//2)
    # print(f"textWidth:{textWidth}, textHeight:{textHeight}")
    textTopLeft = (canvasSize[0]/2-textWidth/2,canvasSize[1]/2-textHeight/1.7)
    draw.text(textTopLeft, text, fill=textRGB, font=font)

    def crop_center(pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    # thumb_width = 150

    # 円形にマスク
    def crop_max_square(pil_img):
        return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    # マスクされたものの周りをブラーでぼかす
    def mask_circle_transparent(pil_img, blur_radius, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = pil_img.copy()
        result.putalpha(mask)

        return result

    im_square = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
    im_thumb = mask_circle_transparent(im_square, 3)
    im_thumb.save(f'./img/{text}.png')

    return thumb_width


#　json読み込み
with open('todo-list.json','r',encoding="utf-8") as f:
    jsn = json.load(f)


# jsonからもらったデータをもとに画像を一つづつ作成する
for i in range(0,len(jsn)):
    create_bubble_img(jsn[i]["content"], jsn[i]["timelimit"], jsn[i]["color"])