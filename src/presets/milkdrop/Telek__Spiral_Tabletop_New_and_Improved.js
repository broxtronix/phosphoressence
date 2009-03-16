function Telek__Spiral_Tabletop_New_and_Improved() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=1;
    echo_zoom=1;
    echo_alpha=0;
    echo_orient=3;
    wave_mode=2;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=1;
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
    fWaveScale=0.684871;
    fWaveSmoothing=0.9;
    wave_mystery=-0.28;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1;
    fShader=0;
    zoom=1;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.001;
    sx=1;
    sy=1;
    wave_r=0.65;
    wave_g=0.65;
    wave_b=0.65;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.5;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0.016;
    ib_size=0;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=0;
    mv_x=33.152;
    mv_y=28.799997;
    mv_dx=0.006;
    mv_dy=0;
    mv_l=1;
    mv_r=1;
    mv_g=1;
    mv_b=0;
    mv_a=0;
    wave_x = pow(sin(time*.3011101),5)*.4+.5;
    wave_y = pow(cos(time*.3),3)*.4+.5;
    wave_r = sin(time*.874)*.5+.5;
    wave_g = sin(time*1.54)*.5+.5;
    wave_b = sin(time*1.1)*.5+.5;
    
    vol= (bass+treb+mid)*.3;
    vol_cap = (max(min(vol,1),.5)-.5)*2;
    wave_r = wave_r*vol_cap;
    wave_g = wave_g*vol_cap;
    wave_b = wave_b*vol_cap;
    ob_size =1;
    ob_r=wave_r*.0;
    ob_g=wave_g*.0;
    ob_b=wave_b*.0;
    
    q1=wave_x;
    q2=1-wave_y;
    
    
    beat=if_milk(above(bass*bass_att,2.7),1,0);
    dm=dm-sign(dm)*bass*beat;
    vang=vang+.3*dm/fps;
    q3 = vang;
    
    monitor = vang;
    //mv_a = 1; decay = 0.81;
    // per_pixel_1=//cen_x = cos(time)*.2+.3;
    // per_pixel_2=//cen_y = sin(time)*.5+.5;
    // per_pixel_3=cen_x = q1;
    // per_pixel_4=cen_y = q2;
    // per_pixel_5=radxy = sin(time*.1)*.15+.3;
    // per_pixel_6=
    // per_pixel_7=dist_x = (x-cen_x)/(radxy*(sin(time*.2*0)*.3+cos((cen_x-x+ (cen_y-y))*10+time*2)*.3+1));
    // per_pixel_8=dist_y = (y-cen_y)/(radxy*(sin(time*.2*0)*.3+sin((cen_x-x+ (cen_y-y))*10+time*2)*.3+1));
    // per_pixel_9=in = below(abs(dist_x),1)*below(abs(dist_y),1);
    // per_pixel_10=//in = bnot(in);
    // per_pixel_11=out = bnot(in);
    // per_pixel_12=inx =(cen_x-q1)+.08*sign(dist_x)*sqr(1-abs(dist_x));
    // per_pixel_13=iny =(cen_y-q2)+.08*sign(dist_y)*sqr(1-abs(dist_y));
    // per_pixel_14=
    // per_pixel_15=//**********outside
    // per_pixel_16=vang=q3; //time*.1;
    // per_pixel_17=vx = (x-.5)*cos(vang) - (y-.5)*sin(vang)+.5;
    // per_pixel_18=vy = (x-.5)*sin(vang) +(y-.5)*cos(vang)+.5;
    // per_pixel_19=
    // per_pixel_20=dvx=.01*sin(time+vy*60*radxy);
    // per_pixel_21=dvy=.01*cos(time+vx*60*radxy);
    // per_pixel_22=
    // per_pixel_23=outx = dvx*cos(vang) - dvy*sin(vang);
    // per_pixel_24=outy = -dvx*sin(vang) - dvy*cos(vang);
    // per_pixel_25=
    // per_pixel_26=dx=in*inx+out*outx;
    // per_pixel_27=dy=in*iny+out*outy;
    dm = 1;
  }
}
register_preset( Telek__Spiral_Tabletop_New_and_Improved);
