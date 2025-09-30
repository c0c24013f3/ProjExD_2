import os
import random
import sys
import math
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数: screen Surface
    戻り値: None
    """
    go_sfc = pg.Surface((WIDTH, HEIGHT))
    go_sfc.fill((0, 0, 0))
    go_sfc.set_alpha(200)

    font = pg.font.Font(None, 100)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとん
    kk_rct = kk_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(go_sfc, (0, 0))
    screen.blit(txt, txt_rct)
    screen.blit(kk_img, kk_rct)
    pg.display.update()
    pg.time.wait(5000)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾のサイズリストと加速度リストを生成する関数
    戻り値: (爆弾Surfaceリスト, 加速度リスト)
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動方向ごとにこうかとん画像を返す辞書を作成する関数
    戻り値: {移動量タプル: Surface}
    """
    kk_base = pg.image.load("fig/3.png")
    kk_imgs = {
        (0, 0): pg.transform.rotozoom(kk_base, 0, 0.9),
        (+5, 0): pg.transform.rotozoom(kk_base, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(kk_base, 180, 0.9),
        (0, -5): pg.transform.rotozoom(kk_base, 90, 0.9),
        (0, +5): pg.transform.rotozoom(kk_base, -90, 0.9),
        (+5, -5): pg.transform.rotozoom(kk_base, -45, 0.9),
        (+5, +5): pg.transform.rotozoom(kk_base, -135, 0.9),
        (-5, -5): pg.transform.rotozoom(kk_base, 45, 0.9),
        (-5, +5): pg.transform.rotozoom(kk_base, 135, 0.9),
    }
    return kk_imgs


def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    爆弾をこうかとんに向かわせるための方向ベクトルを計算する関数
    引数: org 爆弾Rect, dst こうかとんRect, current_xy 現在の速度ベクトル
    戻り値: (vx, vy) 新しい速度ベクトル
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    dist = math.hypot(dx, dy)
    if dist == 0:
        return current_xy
    if dist < 300:  # 距離が近すぎる場合は慣性で移動
        return current_xy
    scale = math.sqrt(50) / dist
    return dx * scale, dy * scale


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_imgs = get_kk_imgs()
    kk_rct = kk_imgs[(0, 0)].get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # こうかとん移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        screen.blit(kk_img, kk_rct)

        # 追従型爆弾
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        avx, avy = vx * bb_accs[idx], vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
