function Rovastar_and_Telek__Altars_of_Madness_Rolling_Oceans_Mix() {
  with (Math) {
    fRating=5.000000;
    gamma=1.98;
    decay=1;
    echo_zoom=1.006596;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=5;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=4.099998;
    fWaveScale=0.660126;
    fWaveSmoothing=0;
    wave_mystery=0.3;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1.331;
    zoomexp=1;
    fShader=0;
    zoom=1;
    rot=0;
    cx=0.5;
    cy=0.5;
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
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=1;
    ib_size=0.005;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=64;
    mv_y=48;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.5;
    mv_r=0.15;
    mv_g=0.45;
    mv_b=0.65;
    mv_a=0.2;
    warp=0;
    ib_a =0.2*bass;
    wave_r = wave_r + 0.45*(0.5*sin(time*0.701)+ 0.3*cos(time*0.438));
    wave_b = wave_b - 0.4*(0.5*sin(time*4.782)+0.5*cos(time*0.522));
    wave_g = wave_g + 0.4*sin(time*1.731);
    decay = decay - equal(frame%100,0)*0.1;
    vol = 0.167*(bass+mid);
    xamptarg = if_milk(equal(frame%15,0),min(0.5*vol*bass_att,0.5),xamptarg);
    xamp = xamp + 0.5*(xamptarg-xamp);
    xdir = if_milk(above(abs(xpos),xamp),-sign(xpos),if_milk(below(abs(xspeed),0.1),2*above(xpos,0)-1,xdir));
    xspeed = xspeed + xdir*xamp - xpos - xspeed*0.055*below(abs(xpos),xamp);
    xpos = xpos + 0.001*xspeed;
    wave_x = 1.5*xpos + 0.5;
    yamptarg = if_milk(equal(frame%15,0),min(0.3*vol*treb_att,0.5),yamptarg);
    yamp = yamp + 0.5*(yamptarg-yamp);
    ydir = if_milk(above(abs(ypos),yamp),-sign(ypos),if_milk(below(abs(yspeed),0.1),2*above(ypos,0)-1,ydir));
    yspeed = yspeed + ydir*yamp - ypos - yspeed*0.055*below(abs(ypos),yamp);
    ypos = ypos + 0.001*yspeed;
    wave_y = 1.5*ypos + 0.5;
    zoom = .995;
    
    
    
    
    
    
    
    frametest = frame%2;
    wave_x = if_milk(frametest,1-wave_x,wave_x);
    wave_y = if_milk(frametest,1-wave_y,wave_y);
    wave_r = if_milk(frametest,wave_r,wave_g);
    wave_g = if_milk(frametest,wave_g,wave_b);
    wave_b = if_milk(frametest,wave_b,wave_r);
    monitor = green;
    q8 =  oldq8+ 0.0005*(pow(1+1.2*bass+0.4*bass_att+0.1*treb+0.1*treb_att+0.1*mid+0.1*mid_att,6)/fps);
    oldq8 = q8;
    
    mv_g=0.5+bass_att*.1;
    beat=if_milk(above(bass*bass_att,4.5),1-beat,beat);
    q1=beat*2-1;
    
    amp =amp*.8+.2*(bass_att+mid_att+treb_att)*.3;
    q2 = min(amp,1);
    trebcap=trebcap*.7+.16*treb;
    q3=trebcap*2;
    monitor = q3;
    // per_pixel_1=dx=dx+0.008*sin((y*2-1)*(48+12*sin(0.412*q8)))+0.008*sin(((y+sin(time*0.163))*2-1)* (3+sin(0.241*q8)));
    // per_pixel_2=dy=dy+0.008*cos((x*2-1)*(64+18*sin(0.376*q8)))+0.008*sin(((x+sin(q8*0.282))*2-1) *(3+sin(0.349*q8)));
    // per_pixel_3=wang = (3+q3)*x+time*1.7+bass*.1;
    // per_pixel_4=in = 0;
    // per_pixel_5=in = in + below(abs(x-.25),.05)*below(abs(y-.5),.25);
    // per_pixel_6=in = below(abs(y-(.5+.5*sin(wang)*q2)),.1);
    // per_pixel_7=in=bnot(bnot(in));
    // per_pixel_8=dx = dx+.02*in;
    // per_pixel_9=dy = dy+.08*cos(wang)*q2*in;
    // per_pixel_10=
    // per_pixel_11=dx = dx+bnot(in)*.005*q1;
    // per_pixel_12=dy = dy+bnot(in)*cos(wang)*-.01*q1;
    q8=0;
  }
}
register_preset( Rovastar_and_Telek__Altars_of_Madness_Rolling_Oceans_Mix);
