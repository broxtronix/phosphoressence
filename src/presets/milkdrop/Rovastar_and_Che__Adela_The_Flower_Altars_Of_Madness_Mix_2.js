function Rovastar_and_Che__Adela_The_Flower_Altars_Of_Madness_Mix_2() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=1;
    echo_zoom=1.000499;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=3;
    wave_additive=0;
    wave_usedots=1;
    bWaveThick=1;
    bModWaveAlphaByVolume=1;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=1.000416;
    fWaveScale=0.671923;
    fWaveSmoothing=0.45;
    wave_mystery=0;
    fModWaveAlphaStart=0.2;
    fModWaveAlphaEnd=0.6;
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
    sx=0.999999;
    sy=0.999999;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.005;
    ob_r=0;
    ob_g=0.6;
    ob_b=0;
    ob_a=1;
    ib_size=0.005;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=20.223999;
    mv_y=20.255999;
    mv_dx=0;
    mv_dy=0;
    mv_l=2.2;
    mv_r=0.9;
    mv_g=0.5;
    mv_b=0;
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
    
    cc=cc+beat;
    q1=cc;
    ib_a=if_milk(equal((3*sin(cc))%2,0),.3+.3*sin(.01*thccl),0);
    //zoom=.98+.02*sin(12*cc);
    //zoomexp=1+.3*sin(26*cc);
    //sx=1+.01*sin(11*cc);
    //sy=1+.01*sin(14*cc);
    wave_x=.5+.4*sin((.02+.005*sin(.003*time))*thccl)+.05*sin(8*time);
    wave_y=.5+.4*sin((.017+.005*sin(.0027*time))*thccl)+.05*sin(6.7*time);
    
    wave_r=sqr(sin(cc+.07*time));
    wave_g=sqr(sin(cc+.06*time));
    wave_b=sqr(sin(cc+.05*time));
    ob_r=.5+.5*sin(1.23*time+4*cc+.011*thccl);
    ob_g=.5+.5*sin(1.32*time+7*cc+.012*thccl);
    ob_b=.5+.5*sin(1.17*time+9*cc+.013*thccl);
    // per_pixel_1=ak=-sin(6*rad+((q1%5)*3)%5*ang+q1)*(1-rad+.2*sin(.54*q1))*above(rad,0);
    // per_pixel_2=block=if_milk(below(ak,-.15),ak,0);
    // per_pixel_3=dx=dx+0.005*sin((y*2-1)*48)+0.001*tan((y*2-1)*64)+0.000*tan((ang-3.1415)*8);
    // per_pixel_4=dy =dy+0.005*sin((x*2-1)*48)+0.001*tan((x*2-1)*64)+0.000*tan((ang-3.1415)*6);
    // per_pixel_5=//dx=dx+0.008*sin((x-0.5)*48)+0.008*sin((x-0.5)*64);
    // per_pixel_6=//dy=dy+0.008*cos((y-0.5)*64);
    // per_pixel_7=dx=if_milk(block,dx,0.008*sin((x-0.5)*48)+0.008*sin((x-0.5)*64));
    // per_pixel_8=dy=if_milk(block,dy,0.008*cos((y-0.5)*64));
    // per_pixel_9=
    // per_pixel_10=zoom = if_milk(block,1,0.97);
  }
}
register_preset( Rovastar_and_Che__Adela_The_Flower_Altars_Of_Madness_Mix_2);
