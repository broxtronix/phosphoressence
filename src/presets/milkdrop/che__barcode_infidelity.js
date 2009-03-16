function che__barcode_infidelity() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=0.992;
    echo_zoom=1.489606;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=7;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=1;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=1.000416;
    fWaveScale=0.303117;
    fWaveSmoothing=0;
    wave_mystery=-0.6;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.000158;
    fShader=0.8;
    zoom=1.000223;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0;
    sx=1;
    sy=1;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.501;
    wave_y=0.99;
    ob_size=0.34;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0.2;
    ib_size=0;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=2.048001;
    mv_y=47.999996;
    mv_dx=-0.08;
    mv_dy=0;
    mv_l=5;
    mv_r=1;
    mv_g=1;
    mv_b=1;
    mv_a=0;
    // timed sidon sensor
    // le = signal level; desired average value = 2
    le=1.4*bass_att+.1*bass+.5*treb;
    pulse=above(le,th);
    // pulsefreq = running average of floorerval between last 5 pulses
    pulsefreq=if_milk(equal(pulsefreq,0),2,
    if_milk(pulse,.8*pulsefreq+.2*(time-lastpulse),pulsefreq));
    lastpulse=if_milk(pulse,time,lastpulse);
    // bt = relative time; 0 = prev beat; 1 = expected beat
    bt=(time-lastbeat)/(.5*beatfreq+.5*pulsefreq);
    // hccp = handcicap for th driven by bt
    hccp=(.03/(bt+.2))+.5*if_milk(band(above(bt,.8),below(bt,1.2)),
    (pow(sin((bt-1)*7.854),4)-1),0);
    beat=band(above(le,th+hccp),btblock);
    btblock=1-above(le,th+hccp);
    lastbeat=if_milk(beat,time,lastbeat);
    beatfreq=if_milk(equal(beatfreq,0),2,
    if_milk(beat,.8*beatfreq+.2*(time-lastbeat),beatfreq));
    // th = threshold
    th=if_milk(above(le,th),le+114/(le+10)-7.407,
    th+th*.07/(th-12)+below(th,2.7)*.1*(2.7-th));
    th=if_milk(above(th,6),6,th);
    thccl=thccl+(th-2.5144);
    
    bccl=bccl+beat;
    q1=thccl;
    q2=bccl;
    
    wave_r=sqr(sin(.016*thccl+bccl+frame%2));
    wave_g=sqr(sin(.018*thccl+bccl+frame%2));
    wave_b=sqr(sin(.017*thccl+bccl+frame%2));
    wave_x=if_milk(frame%2,.501,.5);
    wave_y=if_milk(frame%2,.99,.5);
    wave_mode=if_milk(frame%2,7,0);
    wave_mystery=if_milk(frame%2,0,-.6);
    
    ob_a=if_milk(above(sin(.005*thccl+bccl),.9),.05*(1+sin(time)),0);
    // per_pixel_1=//middle part
    // per_pixel_2=zoom=1+above(sin(1.7*q2),-.5)*.1*sin(2*q2+.027*q1+4*(1+sin(.7*time+q2))*sin(.05*q2+time)*rad);
    // per_pixel_3=rot=.1*sin(q2)*sin(2.3*q2+.027*q1+2*sin(.07*q1+1.2*time)*(rad+sin(time+above(sin(q2),0)*4*sin(q2)*ang)));
    // per_pixel_4=rot=above(sin(1.2*q2+1.3),-.5)*rot;
    // per_pixel_5=
    // per_pixel_6=//borders
    // per_pixel_7=brdr=bor(below(y,.15),above(y,.85));
    // per_pixel_8=dy=if_milk(below(y,.15),y,0)+if_milk(above(y,.85),-1+y,0)+if_milk(brdr,0,dy);
    // per_pixel_9=dx=if_milk(brdr,.01*sin(.02*q1+x+3*ang+10*y),dx);
    // per_pixel_10=rot=if_milk(brdr,0,rot);
    // per_pixel_11=zoom=if_milk(brdr,1,zoom);
    // per_pixel_12=sx=if_milk(brdr,1,sx);
    // per_pixel_13=sy=if_milk(brdr,1,sy);
  }
}
register_preset( che__barcode_infidelity);
