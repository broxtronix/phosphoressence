function Che__Escape() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=0.95;
    echo_zoom=1.000498;
    echo_alpha=0.5;
    echo_orient=1;
    wave_mode=5;
    wave_additive=0;
    wave_usedots=1;
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
    fWaveScale=0.608285;
    fWaveSmoothing=0.9;
    wave_mystery=0;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.000154;
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
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.15;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0;
    ib_size=0.05;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=6.4;
    mv_y=14.400005;
    mv_dx=0;
    mv_dy=-0.01;
    mv_l=0.35;
    mv_r=0.9;
    mv_g=0.5;
    mv_b=0;
    mv_a=1;
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
    
    q8=30/fps;
    ccl=ccl+beat;
    minorccl=minorccl+le*q8;
    q7=ccl+.0002*minorccl;
    q6=3.7*ccl+.01*minorccl;
    ob_size=.3+.3*sin(16*ccl+.007*minorccl);
    ib_a=.5+.4*sin(.01*minorccl+ccl);
    wave_r=.7+.3*sin(.04*ccl+.01*minorccl);
    wave_g=.7+.3*sin(.02*ccl+.012*minorccl);
    wave_b=.3+.3*sin(36*ccl+.013*minorccl);
    ib_r=.25+.25*sin(72*ccl+.016*minorccl);
    ib_g=.25+.25*sin(48*ccl+.021*minorccl);
    ib_b=.5+.3*sin(86*ccl)+.2*(.028*minorccl);
    
    echo_alpha=.5+.5*cos(68*ccl+.0041*minorccl);
    echo_zoom=exp(sin(13.7*ccl+.017*minorccl));
    echo_orient=ccl%4;
    
    mvrot=ccl%6;
    mv_r=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.039,
    if_milk(equal(mvrot,3),.137,.835)),if_milk(above(mvrot,1),.651,
    if_milk(equal(mvrot,0),1,.773)));
    mv_g=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.267,
    if_milk(equal(mvrot,3),.886,.176)),if_milk(above(mvrot,1),.804,
    if_milk(equal(mvrot,0),1,.38)));
    mv_b=if_milk(above(mvrot,2),if_milk(above(mvrot,4),.694,
    if_milk(equal(mvrot,3),.776,.851)),if_milk(above(mvrot,1),.114,
    if_milk(equal(mvrot,0),1,.145)));
    // per_pixel_1=zone=below(sin(sin(49*q7)*14*x-sin(36*q7)*14*y),-.2);
    // per_pixel_2=zoom=1+.33*q8*if_milk(zone,-.5+.1*sin(1.08*q6),.5+.1*sin(.96*q6));
    // per_pixel_3=zoomexp=exp(sin(if_milk(zone,q6,-q6)));
    // per_pixel_4=rot=q8*.03*sin(q6+q7+q7*zone);
  }
}
register_preset( Che__Escape);
