function Idiot_and_Che__Various_Abstract_Effects() {
  with (Math) {
    fRating=1;
    gamma=1;
    decay=0.97;
    echo_zoom=1.000499;
    echo_alpha=0.5;
    echo_orient=3;
    wave_mode=1;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=1.000416;
    fWaveScale=1.000404;
    fWaveSmoothing=0;
    wave_mystery=-0.72;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=0.01;
    fShader=0;
    zoom=1.000198;
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
    wave_x=0.6;
    wave_y=0.7;
    ob_size=0.005;
    ob_r=1;
    ob_g=0;
    ob_b=0;
    ob_a=0.1;
    ib_size=0;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=1;
    mv_x=20.223999;
    mv_y=10.656;
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
    
    wave_r=.5*sqr(sin(time*3.7))+.5*sin(37*ccl+.01*leccl);
    wave_g=.5*sqr(sin(time*2.8))+.5*sin(38*ccl+.01*leccl);
    wave_b=.5*sqr(sin(time*3.2))+.5*sin(36*ccl+.01*leccl);
    wave_x=.5+.1*sin(leccl+frame);
    wave_y=.5+.1*sin(1.2*leccl+frame+1.17);
    
    ccl=ccl+beat;
    q1=ccl;
    leccl=leccl+bass+treb;
    q2=.001*leccl;
    q3=th;
    
    ob_r=wave_R;
    ob_b=wave_b;
    ob_g=wave_G;
    // per_pixel_1=sector=(ang+rot+x+y)*5000+q1+10*sin(q2);
    // per_pixel_2=orient=sector%4;
    // per_pixel_3=spd=.005*q3;
    // per_pixel_4=quadrant=above(x,.5)*2+above(y,.5-x);
    // per_pixel_5=
    // per_pixel_6=// variant movement
    // per_pixel_7=dx=dx+equal(quadrant,q1%4)*if_milk(below(orient,2),-spd,spd);
    // per_pixel_8=dy=dx+equal(quadrant,q1%4)*if_milk(orient%2,-spd,spd);
    // per_pixel_9=
    // per_pixel_10=// pulsed zoom
    // per_pixel_11=zoom = 1+equal(quadrant,(q1+1)%4-x*5*sin(100*q2+10*sign(sin(20*q1))*rad));
    // per_pixel_12=
    // per_pixel_13=// weird warp
    // per_pixel_14=dx=dx+equal(quadrant,(q1+3)%4)*spd*sin((20+14*sin(18*q2))*x
    // per_pixel_15=+(15+10*sin(19*q2))*y+sin(1.8*q2)*q1)*Rad*sin(q1);
    // per_pixel_16=dy=dy+equal(quadrant,(q1+3)%4)*spd*sin((20+14*sin(18.5*q2))*x
    // per_pixel_17=+(15+10*sin(19.5*q2))*y+sin(1.7*q2)*q1)*Rad*sin(q1);
    // per_pixel_18=
    // per_pixel_19=// ccl driven stretch fx
    // per_pixel_20=sx=1+equal(quadrant,(q1+2)%4)*.1*sin(53*q1+10*q2+4*ang);
    // per_pixel_21=sy=1+equal(quadrant,(q1+2)%4)*.1*sin(32*q1+10*q2+4*ang);
    // per_pixel_22=rot=equal(quadrant,(q1+2)%4)*.05*sin(27*q1+10*q2);
    // per_pixel_23=
    // per_pixel_24=// structures
    // per_pixel_25=structure=equal(quadrant,(21.7*q1)%4)*above(sector%6,2)-q1*rad;
    // per_pixel_26=
    // per_pixel_27=dx=if_milk(structure,5*-dx,dx);
    // per_pixel_28=dy=if_milk(structure,5*-dy,dy);;
    // per_pixel_29=rot=if_milk(structure,5*-rot-rad*rad,rad*rad);
    // per_pixel_30=zoom=if_milk(structure,5*-zoom+6,zoom);
    // per_pixel_31=
    // per_pixel_32=sx=sx+.3*Sin(x)*sin(q3);
    // per_pixel_33=sy=sy-.3*sin(y)*sin(q1);
  }
}
register_preset( Idiot_and_Che__Various_Abstract_Effects);
