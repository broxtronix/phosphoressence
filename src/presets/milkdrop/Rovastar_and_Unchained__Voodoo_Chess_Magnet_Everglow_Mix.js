function Rovastar_and_Unchained__Voodoo_Chess_Magnet_Everglow_Mix() {
  with (Math) {
    fRating=3;
    gamma=2;
    decay=1;
    echo_zoom=1.006496;
    echo_alpha=0.5;
    echo_orient=3;
    wave_mode=1;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=1;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=2.781664;
    fWaveScale=0.590116;
    fWaveSmoothing=0.36;
    wave_mystery=0;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1;
    warp_scale=1;
    zoomexp=7.523901;
    fShader=0;
    zoom=1.009898;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=1;
    sx=1;
    sy=1;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.01;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=1;
    ib_size=0;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=64;
    mv_y=48;
    mv_dx=0;
    mv_dy=0;
    mv_l=0;
    mv_r=0.35;
    mv_g=0.35;
    mv_b=0.35;
    mv_a=0;
    warp=0;
    state=if_milk(above(bass_att,1.3),3,if_milk(above(treb_att,1.3),2,1));
    wave_b=if_milk(equal(state,2),.2+.2*sin(time),if_milk(equal(state,3),.9+.1*sin(time),.6+.08*sin(time)));
    wave_g=if_milk(equal(state,2),0,if_milk(equal(state,3),0,.49));
    wave_r=if_milk(equal(state,2),.7+.1*sin(time*.888),0);
    //zoom=if_milk(above(bass_att+treb,2),1+sin(state*1.3)/10,1-sin(state*1.5)/10);
    q1=state;
    wave_mystery=wave_mystery+(1-zoom)*10;
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
    q3=30/fps;
    ccl=ccl+beat;
    minorccl=minorccl+.01*le;
    q4=beat;
    beatcounter = if_milk(beat,beatcounter +1, beatcounter);
    beatcounter = if_milk(above(beatcounter,7), 0, beatcounter);
    beateven = beatcounter%2;
    q5 = beateven;
    q8 =oldq8+ 0.005*(pow(1.2*bass+0.4*bass_att+0.1*treb+0.1*treb_att+0.1*mid+0.1*mid_att,6)/fps);
    oldq8 = q8;
    // per_pixel_1=grid=abs(x*18+3*q5)%2 + abs(y*18+3*q5)%2;
    // per_pixel_2=cx = grid;
    // per_pixel_3=cy = grid;
    // per_pixel_4=zoom=1+0.5*if_milk(bnot(grid),cos(rad*10*sin(q8))*.07,cos(x*10*sin(q8))*.07);
    // per_pixel_5=rot = 0.01*(1-rad);
    // per_pixel_6=dx=0.4*grid*(0.008*sin((y*2-1)*48)+0.008*sin((y*2-1)*64));
    // per_pixel_7=dy=0.4*grid*(0.008*cos((x*2-1)*64)+0.008*cos((x*2-1)*48));
  }
}
register_preset( Rovastar_and_Unchained__Voodoo_Chess_Magnet_Everglow_Mix);
