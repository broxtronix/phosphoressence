function Che__Burning_Hus() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=1;
    echo_zoom=1.000499;
    echo_alpha=0;
    echo_orient=0;
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
    wave_a=1.000416;
    fWaveScale=1.000404;
    fWaveSmoothing=0;
    wave_mystery=0;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.000157;
    fShader=0;
    zoom=1.010225;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0;
    sx=1;
    sy=1;
    wave_r=0.8;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=1;
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
    q8=60/fps;
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
    thccl=thccl+q8*(th-2.5144);
    leccl=leccl+q8*le;
    btccl=btccl+beat;
    q1=thccl;
    q2=leccl;
    q3=btccl;
    wave_r=sqr(sin(1.5*time+.0037*leccl+3*bccl));
    wave_g=.5+.5*sin(1.6*time+.0042*leccl+2*bccl);
    wave_b=.5+.5*sin(1.7*time+.0056*leccl+4*bccl);
    // per_pixel_1=zoom=1.01+q8*.13*sin(.1*q1)*(sin((8+3*sin(q3))*rad)+sin(.1*q2));
    // per_pixel_2=rot=.05*q8*sin(.02*q1*sin(q3))*sin((4+3*sin(q3+.03*q2))*rad);
  }
}
register_preset( Che__Burning_Hus);
