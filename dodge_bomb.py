import os, random, sys, math
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(5,0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: tate = False
    return yoko, tate

def init_bb_imgs():
    bb_imgs = []
    for r in range(1, 11):
        bb = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb, (255,0,0), (10*r,10*r), 10*r)
        bb.set_colorkey((0,0,0))
        bb_imgs.append(bb)
    bb_accs = [a for a in range(1,11)]
    return bb_imgs, bb_accs

def get_kk_imgs():
    base = pg.image.load("fig/3.png")
    return {
        (0,0): pg.transform.rotozoom(base,0,0.9),
        (+5,0): pg.transform.rotozoom(base,0,0.9),
        (-5,0): pg.transform.rotozoom(base,180,0.9),
        (0,-5): pg.transform.rotozoom(base,90,0.9),
        (0,+5): pg.transform.rotozoom(base,-90,0.9),
        (+5,-5): pg.transform.rotozoom(base,-45,0.9),
        (+5,+5): pg.transform.rotozoom(base,-135,0.9),
        (-5,-5): pg.transform.rotozoom(base,45,0.9),
        (-5,+5): pg.transform.rotozoom(base,135,0.9),
    }

def calc_orientation(org, dst, v):
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    d = math.hypot(dx, dy)
    if d == 0: return v
    if d < 300: return v
    s = math.sqrt(50)/d
    return dx*s, dy*s

def gameover(sc):
    g = pg.Surface((WIDTH, HEIGHT))
    g.fill((0,0,0)); g.set_alpha(200)
    f = pg.font.Font(None,100)
    t = f.render("Game Over", True, (255,255,255))
    r = t.get_rect(center=(WIDTH//2, HEIGHT//2))
    img = pg.image.load("fig/8.png")
    ir = img.get_rect(center=(WIDTH//2, HEIGHT//2+100))
    sc.blit(g,(0,0)); sc.blit(t,r); sc.blit(img,ir)
    pg.display.update(); pg.time.wait(3000)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    sc = pg.display.set_mode((WIDTH, HEIGHT))
    bg = pg.image.load("fig/pg_bg.jpg")

    kk_imgs = get_kk_imgs()
    kk_r = kk_imgs[(0,0)].get_rect()
    kk_r.center = 300,200

    bb_imgs, bb_accs = init_bb_imgs()
    # --- 多个炸弹，但写得不规范 ---
    b1 = bb_imgs[0].get_rect(); b1.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    b2 = bb_imgs[0].get_rect(); b2.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    b3 = bb_imgs[0].get_rect(); b3.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    v1 = (5,5); v2 = (-5,5); v3 = (5,-5)

    clock = pg.time.Clock(); tmr=0
    while True:
        for e in pg.event.get():
            if e.type==pg.QUIT:return
        sc.blit(bg,[0,0])

        # 碰撞检测（写重复）
        if kk_r.colliderect(b1) or kk_r.colliderect(b2) or kk_r.colliderect(b3):
            gameover(sc); return

        # こうかとん移动
        key=pg.key.get_pressed(); mv=[0,0]
        for k,d in DELTA.items():
            if key[k]: mv[0]+=d[0]; mv[1]+=d[1]
        kk_r.move_ip(mv)
        if check_bound(kk_r)!=(True,True): kk_r.move_ip(-mv[0],-mv[1])
        sc.blit(kk_imgs.get(tuple(mv), kk_imgs[(0,0)]), kk_r)

        idx = min(tmr//500, 9)
        # 炸弹1
        v1 = calc_orientation(b1, kk_r, v1)
        b1.move_ip(v1[0]*bb_accs[idx], v1[1]*bb_accs[idx])
        sc.blit(bb_imgs[idx], b1)
        # 炸弹2
        v2 = calc_orientation(b2, kk_r, v2)
        b2.move_ip(v2[0]*bb_accs[idx], v2[1]*bb_accs[idx])
        sc.blit(bb_imgs[idx], b2)
        # 炸弹3
        v3 = calc_orientation(b3, kk_r, v3)
        b3.move_ip(v3[0]*bb_accs[idx], v3[1]*bb_accs[idx])
        sc.blit(bb_imgs[idx], b3)

        pg.display.update(); tmr+=1; clock.tick(50)

if __name__=="__main__":
    pg.init(); main(); pg.quit(); sys.exit()
