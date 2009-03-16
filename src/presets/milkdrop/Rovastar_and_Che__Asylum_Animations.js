function Rovastar_and_Che__Asylum_Animations() {
  with (Math) {
    fRating=3.5;
    gamma=2;
    decay=1;
    echo_zoom=1;
    echo_alpha=0;
    echo_orient=1;
    wave_mode=2;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=1;
    wave_brighten=1;
    wrap=1;
    darken_center=1;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=1;
    fWaveScale=0.5;
    fWaveSmoothing=0;
    wave_mystery=0;
    fModWaveAlphaStart=1.5;
    fModWaveAlphaEnd=1;
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
    warp=0;
    sx=1;
    sy=1;
    wave_r=0.23;
    wave_g=0.2;
    wave_b=0.2;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.005;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0.4;
    ib_size=0;
    ib_r=0;
    ib_g=0;
    ib_b=0.3;
    ib_a=0;
    mv_x=0;
    mv_y=0;
    mv_dx=0;
    mv_dy=0.33;
    mv_l=5;
    mv_r=1;
    mv_g=0.3;
    mv_b=0.1;
    mv_a=1;
    wave_r = wave_r + 0.350*( 0.60*sin(0.825*time) + 0.40*sin(0.915*time) );
    wave_g = wave_g + 0.350*( 0.60*sin(0.900*time) + 0.40*sin(1.025*time) );
    wave_b = wave_b + 0.350*( 0.60*sin(0.810*time) + 0.40*sin(0.950*time) );
    wave_x = 0.5-cos(time+dx_residual)/3.5;
    wave_y = 0.5-cos(time+dy_residual)/2.5;
    cx = cx + 0.225*( 0.60*sin(0.350*time) + 0.40*sin(0.350*time) );
    cy = cy + 0.225*( 0.60*sin(0.350*time) + 0.40*sin(0.350*time) );
    dx = 0.005 + 0.002*( 0.60*sin(0.234*time) + 0.40*sin(0.277*time) );
    dy = 0.005 + 0.002*( 0.60*sin(0.234*time) + 0.40*sin(0.277*time) );
    dx_residual=max(bass, bass_att)-1;
    dy_residual=min(bass, bass_att)-1;
    dx = if_milk(above(bass_att+bass,2.8),6*dx,dx);
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
    wave_r=.5+.15*sin(12*ccl)+.35*sin(3.62*minorccl);
    wave_g=.5+.15*sin(14*ccl)+.35*sin(7.38*minorccl);
    wave_b=.5+.15*sin(16*ccl)+.35*sin(5.21*minorccl);
    q1=.5+.25*sin(17*ccl+minorccl);
    cx=if_milk(beat,.5+.5*sin(38*ccl),q1);
    q2=.5+.25*sin(17*ccl+minorccl);
    cy=if_milk(beat,.5+.5*sin(46*ccl),q2);
    mv_x = 1.25;
    mv_y = 1.25;
    mv_dx =q1-0.5;
    mv_dy = -1*(q2-0.5);
    // per_pixel_1=myrot = 0.03*sin(0.84*time)-0.013*cos(0.784*time)+0.02*sin(1-rad);
    // per_pixel_2=rot = myrot;
    // per_pixel_3=// coordinates transfomation
    // per_pixel_4=// q1,q2 = position; q3 = 1/zoom; q4 = rotation
    // per_pixel_5=aang=atan2(y-q2,x-q1)-1.57;
    // per_pixel_6=arad=sqrt(sqr(y-q2)+sqr(x-q1));
    // per_pixel_7=atx=cos(aang)*arad;
    // per_pixel_8=aty=sin(aang)*arad;
    // per_pixel_9=
    // per_pixel_10=sound=if_milk(below(x,.5),2*x*mid+(1-(2*x))*bass,
    // per_pixel_11=(x-.5)*2*treb+(1-(x-.5)*2)*mid);
    // per_pixel_12=sound=sound*q3;
    // per_pixel_13=zone=below(abs(x-q1),.15)*below(abs(y-q2),.15);
    // per_pixel_14=rot=if_milk(zone,bass*bass_att*0.2*pow(arad,arad),myrot);
    // per_pixel_15=dx = if_milk(zone,0,dx+0.01*rad*sound);
  }
}
register_preset( Rovastar_and_Che__Asylum_Animations);
