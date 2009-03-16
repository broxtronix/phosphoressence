function che__terracarbon_stream() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=1;
    echo_zoom=1.000499;
    echo_alpha=0.5;
    echo_orient=1;
    wave_mode=3;
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
    wave_a=0.03074;
    fWaveScale=0.498516;
    fWaveSmoothing=0;
    wave_mystery=0;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.000158;
    fShader=0;
    zoom=1.000223;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0;
    sx=1;
    sy=1;
    wave_r=0;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.1;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0.06;
    ib_size=0.035;
    ib_r=0.25;
    ib_g=0.45;
    ib_b=0.25;
    ib_a=0.29;
    mv_x=19.199999;
    mv_y=14.400005;
    mv_dx=0;
    mv_dy=0;
    mv_l=2.5;
    mv_r=0.06;
    mv_g=1;
    mv_b=1;
    mv_a=0.2;
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
    
    q1=le;
    q2=thccl+.2*leccl;
    leccl=leccl+dle*le;
    dle=if_milk(beat,-dle,dle);
    bccl=bccl+beat;
    
    wave_r=.1+.8*sqr(sin(.011*thccl))+.1*sin(leccl*.061);
    wave_g=.1+.8*sqr(sin(.013*thccl))+.1*cos(leccl*.067);
    wave_b=.1+.8*sqr(cos(.017*thccl))+.1*sin(leccl*.065);
    
    ib_r=ib_r+.1*sin(1.3*time+.012*leccl);
    ib_g=ib_g+.1*sin(1.7*time+.019*leccl);
    ib_b=ib_b+.1*sin(1.9*time+.017*leccl);
    mv_r=.5*(ib_r+wave_r);mv_g=.5*(ib_g+wave_g);mv_b=.5*(ib_b+wave_b);
    mv_a=.5*sqr(sin(.01*leccl+bccl));
    
    echo_alpha=.5+.2*cos(.07*leccl+.02*thccl);
    eo=if_milk(band(equal(bccl%3,0),beat),random_integer(4),eo);
    q3=(equal(eo,2)+equal(eo,1))*equal(bccl%2,0);
    q4=(equal(eo,0)+equal(eo,3))*equal(bccl%2,0);
    echo_orient=eo;
    // per_pixel_1=dqv=above(x,.5)-above(y,.5);
    // per_pixel_2=rot=sin(sin(rad*(13+5*sin(.01*q2))+.06*q2)*q1*.01);
    // per_pixel_3=zoom=1+if_milk(q3,dqv,1)*.1*sin(7*ang+.03*q2);
    // per_pixel_4=zoom=if_milk(q4,if_milk(below(rad,.8*sqr(sin(.016*q2))),.75+.4*cos(.021*q2),zoom),zoom);
    dle=1;
  }
}
register_preset( che__terracarbon_stream);
