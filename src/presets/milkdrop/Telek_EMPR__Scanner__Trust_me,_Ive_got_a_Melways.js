function Telek_EMPR__Scanner__Trust_me,_Ive_got_a_Melways() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=1;
    echo_zoom=1.006596;
    echo_alpha=0;
    echo_orient=3;
    wave_mode=0;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=1;
    wrap=1;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=1;
    solarize=0;
    invert=0;
    wave_a=4.099998;
    fWaveScale=1.886994;
    fWaveSmoothing=0.63;
    wave_mystery=-0.512022;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1.331;
    zoomexp=1;
    fShader=0;
    zoom=0.989618;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.01;
    sx=1;
    sy=1;
    wave_r=0.080049;
    wave_g=0.672309;
    wave_b=0.063195;
    wave_x=0.075045;
    wave_y=0.423466;
    ob_size=0.055;
    ob_r=0.773572;
    ob_g=0.389471;
    ob_b=0.393519;
    ob_a=0.013639;
    ib_size=0.0035;
    ib_r=0.718305;
    ib_g=0.386754;
    ib_b=0.344725;
    ib_a=0.018358;
    mv_x=38.399994;
    mv_y=24.000004;
    mv_dx=-0.281976;
    mv_dy=0.406558;
    mv_l=5;
    mv_r=0.78774;
    mv_g=0.415692;
    mv_b=0.483679;
    mv_a=0.11169;
    high_bass = above(bass_att,2);
    high_treb = above(treb, 2);
    
    wave_b = if_milk(high_treb,0,1);
    
    ob_r = sin(time*.3)/2+.5;
    ob_g= sin(time*.34)/2+.5;
    ob_b = sin(time*.3714)/2+.5;
    
    boomnow = if_milk(high_bass,time,boomnow);
    brightness = min(sqr(time-boomnow-.866)+.25,1);
    av_bass=if_milk(high_bass,av_bass*.8+.2*bass,av_bass);
    count=count+above(bass,av_bass*1.2);
    
    ob_r = ob_r*brightness;
    ob_g = ob_g*brightness;
    ob_b = ob_b*brightness;
    
    w_dx = (above((w_y*bits)%2,0)*.01-.005)*sin(time);
    w_dy = (above((w_x*bits)%2,0)*.01-.005)*cos(time);
    
    w_x = w_x+w_dx;
    w_y = w_y +w_dy;
    q1 = bits;
    
    
    w_dx = if_milk(above(abs(w_x-.5),.5),-w_dx,w_dx);
    w_dy = if_milk(above(abs(w_y-.5),.5),-w_dy,w_dy);
    w_x = if_milk(above(abs(w_x-.5),.5),(w_x-.5)*.95+.5,w_x);
    w_y = if_milk(above(abs(w_y-.5),.5),(w_y-.5)*.95+.5,w_y);
    
    wave_x = w_x;
    wave_y = w_y;
    
    monitor = count;
    
    
    ob_a = max(wave_b - bass , wave_b * time);
    ib_r = max(treb * bass_att , wave_x * wave_b);
    //ob_g = max(time * wave_r , warp * wave_x);
    wave_g = min(wave_r + wave_x , time * wave_g);
    wave_b = if_milk(equal(bass * wave_r , bass * treb_att) , treb * zoom , treb - time);
    //ob_b = max(max(bass_att + treb_att , mid_att * wave_g) , wave_r - wave_b);
    mv_l = 5 + min(bass + wave_g , zoom - frame);
    wave_b = max(if_milk(equal(wave_b * wave_y , mid_att - wave_r) , time - frame , zoom * wave_r) , treb * frame);
    mv_r = if_milk(equal(treb + mid , bass - mid_att) , wave_y + wave_y , wave_r * treb);
    mv_g = if_milk(above(wave_r * treb_att , time - frame) , mid + warp , warp - treb);
    ib_G = wave_x + zoom;
    //ob_r = if_milk(below(time * time , frame * bass) , bass_att * wave_g , bass * wave_g);
    wave_b=if_milk(below(wave_b,0.0), 0.0, wave_b);
    wave_b=if_milk(above(wave_b,1.0), 1.0, wave_b);
    wave_g=if_milk(below(wave_g,0.0), 0.0, wave_g);
    wave_g=if_milk(above(wave_g,1.0), 1.0, wave_g);
    //ob_r=if_milk(below(ob_r,0.0), 0.0, ob_r);
    //ob_r=if_milk(above(ob_r,1.0), 1.0, ob_r);
    //ob_g=if_milk(below(ob_g,0.0), 0.0, ob_g);
    //ob_g=if_milk(above(ob_g,1.0), 1.0, ob_g);
    //ob_b=if_milk(below(ob_b,0.0), 0.0, ob_b);
    //ob_b=if_milk(above(ob_b,1.0), 1.0, ob_b);
    //ob_a=if_milk(below(ob_a,0.0), 0.0, ob_a);
    //ob_a=if_milk(above(ob_a,1.0), 1.0, ob_a);
    mv_r=if_milk(below(mv_r,0.0), 0.0, mv_r);
    mv_r=if_milk(above(mv_r,1.0), 1.0, mv_r);
    mv_g=if_milk(below(mv_g,0.0), 0.0, mv_g);
    mv_g=if_milk(above(mv_g,1.0), 1.0, mv_g);
    mv_l=if_milk(below(mv_l,0.0), 0.0, mv_l);
    mv_l=if_milk(above(mv_l,5.0), 5.0, mv_l);
    wave_g=if_milk(below(wave_g,0.0), 0.0, wave_g);
    wave_g=if_milk(above(wave_g,1.0), 1.0, wave_g);
    wave_b=if_milk(below(wave_b,0.0), 0.0, wave_b);
    wave_b=if_milk(above(wave_b,1.0), 1.0, wave_b);
    ob_r=if_milk(below(ob_r,0.0), 0.0, ob_r);
    ob_r=if_milk(above(ob_r,1.0), 1.0, ob_r);
    ob_g=if_milk(below(ob_g,0.0), 0.0, ob_g);
    ob_g=if_milk(above(ob_g,1.0), 1.0, ob_g);
    ob_b=if_milk(below(ob_b,0.0), 0.0, ob_b);
    ob_b=if_milk(above(ob_b,1.0), 1.0, ob_b);
    wave_b=if_milk(below(wave_b,0.0), 0.0, wave_b);
    wave_b=if_milk(above(wave_b,1.0), 1.0, wave_b);
    wave_g=if_milk(below(wave_g,0.0), 0.0, wave_g);
    wave_g=if_milk(above(wave_g,1.0), 1.0, wave_g);
    ob_a=if_milk(below(ob_a,0.0), 0.0, ob_a);
    ob_a=if_milk(above(ob_a,1.0), 1.0, ob_a);
    ob_g=if_milk(below(ob_g,0.0), 0.0, ob_g);
    ob_g=if_milk(above(ob_g,1.0), 1.0, ob_g);
    ob_r=if_milk(below(ob_r,0.0), 0.0, ob_r);
    ob_r=if_milk(above(ob_r,1.0), 1.0, ob_r);
    ob_b=if_milk(below(ob_b,0.0), 0.0, ob_b);
    ob_b=if_milk(above(ob_b,1.0), 1.0, ob_b);
    ib_r=if_milk(below(ib_r,0.0), 0.0, ib_r);
    ib_r=if_milk(above(ib_r,1.0), 1.0, ib_r);
    ib_b=if_milk(below(ib_b,0.0), 0.0, ib_b);
    ib_b=if_milk(above(ib_b,1.0), 1.0, ib_b);
    ib_G=if_milk(below(ib_G,0.0), 0.0, ib_G);
    ib_G=if_milk(above(ib_G,1.0), 1.0, ib_G);
    mv_r=if_milk(below(mv_r,0.0), 0.0, mv_r);
    mv_r=if_milk(above(mv_r,1.0), 1.0, mv_r);
    mv_g=if_milk(below(mv_g,0.0), 0.0, mv_g);
    mv_g=if_milk(above(mv_g,1.0), 1.0, mv_g);
    // per_pixel_1=zoom = 1-.03*(1-rad);
    // per_pixel_2=rot = sin(time*.07845+sin(time*.1))*.04*(1+sin(time*.09784)*.5-rad);
    bits = 5;
  }
}
register_preset( Telek_EMPR__Scanner__Trust_me,_Ive_got_a_Melways);
