function Unchained_and_Che__Oddnezz_3() {
  with (Math) {
    fRating=2;
    gamma=2;
    decay=0.9;
    echo_zoom=0.9999;
    echo_alpha=0.5;
    echo_orient=3;
    wave_mode=0;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=1;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=0.001043;
    fWaveScale=0.01;
    fWaveSmoothing=0.75;
    wave_mystery=-1;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.0081;
    fShader=0.3;
    zoom=1.00808;
    rot=1;
    cx=2;
    cy=-1;
    dx=0;
    dy=0;
    warp=0.01;
    sx=1;
    sy=1;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.005;
    ob_r=1;
    ob_g=0;
    ob_b=0;
    ob_a=0.1;
    ib_size=0.003;
    ib_r=0;
    ib_g=0;
    ib_b=1;
    ib_a=0.6;
    mv_x=12;
    mv_y=9;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.9;
    mv_r=1;
    mv_g=1;
    mv_b=1;
    mv_a=0;
    // sensor - alpha
    le=1.4*bass_att+.1*bass+.5*treb;
    pulse=band(above(le,th),above(le-th,block));
    block=le-th;
    th=if_milk(above(le,th),le+114/(le+10)-7.407,
    th+th*.07/(th-12)+below(th,2.7)*.1*(2.7-th));
    th=if_milk(above(th,5.2),4,th);
    
    q1=.12*th;
    ccl=if_milk(pulse,ccl+1,ccl);
    q2=ccl;
    
    mvrot=if_milk(pulse,
    if_milk(above(mvrot,4),0,mvrot+1),mvrot);
    mv_r=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.039,
    if_milk(equal(mvrot,3),.137,.835)),if_milk(above(mvrot,1),.651,
    if_milk(equal(mvrot,0),1,.773)));
    mv_g=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.267,
    if_milk(equal(mvrot,3),.886,.176)),if_milk(above(mvrot,1),.804,
    if_milk(equal(mvrot,0),1,.38)));
    mv_b=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.694,
    if_milk(equal(mvrot,3),.776,.851)),if_milk(above(mvrot,1),.114,
    if_milk(equal(mvrot,0),1,.145)));
    
    thccl = thccl + th;
    mv_r=min(1,max(0,mv_r+.5*sin(.015*thccl)));
    mv_g=min(1,max(0,mv_g+.5*sin(.016*thccl)));
    mv_b=min(1,max(0,mv_b+.5*sin(.017*thccl)));
    wave_r=1-mv_b;
    wave_g=1-mv_r;
    wave_b=1-mv_g;
    
    mv_x=mv_x+ccl%31-9;
    mv_y=mv_y+ccl%21-7;
    
    ob_r=ob_r + time*sin(bass);
    ob_b=ob_b + time*sin(treb+1);
    ob_g=ob_g + time*sin(mid/1.5);
    CX=2*sin(time);
    // per_pixel_1=zone=below(rad,q1);
    // per_pixel_2=zoom=1+.01*sin(if_milk(zone,q2%4-1,(q2+1)%3)*q2+rad*8);
    // per_pixel_3=sx=sx+sin(if_milk(zone,(q2+.5)%8-5,(q2+3)%6-3)*q2)*.008;
    // per_pixel_4=sy=sy+sin(if_milk(zone,q2%7-5,(q2+3.4)%7-3)*q2)*.008;
    // per_pixel_5=grid=pow(x*(4+sin(q1*18)),1+q2%5)%2 + pow(y*(4+sin(q1*20)),1+q2%6)%2;
    // per_pixel_6=rot=bnot(grid)*above(x,y)*above(y,(1-x))*below(rad,.5+.25*sin(zoom*317));
  }
}
register_preset( Unchained_and_Che__Oddnezz_3);
