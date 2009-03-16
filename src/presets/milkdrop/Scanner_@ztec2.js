function Scanner_@ztec2() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=0.998999;
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
    darken=0;
    solarize=0;
    invert=0;
    wave_a=4.099998;
    fWaveScale=1.886994;
    fWaveSmoothing=0.63;
    wave_mystery=-0.5;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1.331;
    zoomexp=1;
    fShader=0;
    zoom=0.999514;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.01;
    sx=1;
    sy=1;
    wave_r=0.65;
    wave_g=0.65;
    wave_b=0.65;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.055;
    ob_r=1;
    ob_g=1;
    ob_b=0;
    ob_a=0.2;
    ib_size=0.0035;
    ib_r=0;
    ib_g=0;
    ib_b=0;
    ib_a=0;
    mv_x=38.399994;
    mv_y=24.000004;
    mv_dx=0;
    mv_dy=0.000002;
    mv_l=5;
    mv_r=0;
    mv_g=0;
    mv_b=0.7;
    mv_a=0;
    high_bass = above(bass_att,2);
    high_treb = above(treb, 2);
    
    wave_b = if_milk(high_treb,0,1);
    
    //mv_rr = if_milk(high_bass,.5 ,mv_rr*.9);
    //mv_r = mv_rr;
    //mv_b = if_milk(high_treb*high_bass,0,1);
    //mv_g = if_milk(high_treb*high_bass,0,.1*sin(time*.302)+.1);
    //mv_a = if_milk(above(bass_att,1.5),.6,mv_a);
    //mv_x = bits *3;
    //mv_y = mv_x *.8;
    
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
    monitor = bits;
    q1 = bits;
    w_x = if_milk(above(abs(w_x-.5),.5),random_integer(10)/10,w_x);
    w_y = if_milk(above(abs(w_y-.5),.5),random_integer(10)/10,w_y);
    
    wave_x = w_x;
    wave_y = w_y;
    
    monitor = brightness;
    monitor = av_bass;
    monitor = count;
    // per_pixel_1=//---- Rotation Angle
    // per_pixel_2=v_ang=time*.2*(x+y)*(.005+.003*(sin(time*.1)+cos(time*.14)));
    // per_pixel_3=
    // per_pixel_4=v_ang = time+sin(x*(sin(time*.32)*3+4)+y*(sin(time*.42)*3+4));
    // per_pixel_5=
    // per_pixel_6=//---- Initialisation: X, Y, ANG, CX, CY, DX, DY, SX, SY
    // per_pixel_7=//---- to these: VX, VY, VANG, CVX, CVY, DVX, DVY, SVX, SVY
    // per_pixel_8=vx = (x-.5)*cos(v_ang) - (y-.5)*sin(v_ang)+.5;
    // per_pixel_9=vy = (x-.5)*sin(v_ang) +(y-.5)*cos(v_ang)+.5;
    // per_pixel_10=vang=atan((vy-.5)/(vx+.000001-.5))+below(vx,.5)*sign(vy-.5)*3.14159;
    // per_pixel_11=cvx = (cx-.5)*cos(v_ang) - (cy-.5)*sin(v_ang)+.5;
    // per_pixel_12=cvy = (cx-.5)*sin(v_ang) +(cy-.5)*cos(v_ang)+.5;
    // per_pixel_13=svx=sx; svy=sy; dvx=dx; dvy=dy;
    // per_pixel_14=cang=atan((vy-cvy)/(vx+.000001-cvx))
    // per_pixel_15=+below(vx,cvx)*sign(vy-cvy)*3.14159; //Bonus var: angle about (cvx,cvy)
    // per_pixel_16=
    // per_pixel_17=//---- Preset Code
    // per_pixel_18=
    // per_pixel_19=dx=above(vx,sin(time*.5)*.7+.5)*1.0002;
    // per_pixel_20=dy = above(vy,(cos(time*.5)*.6+.5));
    // per_pixel_21=
    // per_pixel_22=//---- Realisation of virtual variables
    // per_pixel_23=cx = (cvx-.5)*cos(-v_ang) - (cvy-.5)*sin(-v_ang)+.5;
    // per_pixel_24=cy = (cvx-.5)*sin(-v_ang) +(cvy-.5)*cos(-v_ang)+.5;
    // per_pixel_25=dvx = dvx + (vx-cvx)*(svx-1);
    // per_pixel_26=dvy = dvy - (vy-cvy)*(svy-1);
    // per_pixel_27=//dx = dvx*cos(v_ang) - dvy*sin(v_ang);
    // per_pixel_28=//dy = -dvx*sin(v_ang) - dvy*cos(v_ang);
    // per_pixel_29=//---- End Virtual Axis Code
    bits = random_integer(7)+7;
  }
}
register_preset( Scanner_@ztec2);
