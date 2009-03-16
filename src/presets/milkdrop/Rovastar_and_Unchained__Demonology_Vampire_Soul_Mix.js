function Rovastar_and_Unchained__Demonology_Vampire_Soul_Mix() {
  with (Math) {
    fRating=2;
    gamma=2;
    decay=1;
    echo_zoom=0.9999;
    echo_alpha=0.5;
    echo_orient=1;
    wave_mode=0;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=1;
    wave_brighten=0;
    wrap=1;
    darken_center=1;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=0.868;
    fWaveScale=0.282091;
    fWaveSmoothing=0;
    wave_mystery=0;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.0017;
    fShader=0;
    zoom=0.9881;
    rot=1;
    cx=2;
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
    ob_r=1;
    ob_g=0;
    ob_b=0;
    ob_a=0.2;
    ib_size=0.005;
    ib_r=0;
    ib_g=0;
    ib_b=0;
    ib_a=0.6;
    mv_x=64;
    mv_y=48;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.55;
    mv_r=0;
    mv_g=0;
    mv_b=0;
    mv_a=0;
    warp=0;
    le=1+.5+2*sin(bass_att);
    bpulse=band(above(le,bth),above(le-bth,bblock));
    bblock=le-bth;
    bth=if_milk(above(le,bth),le+114/(le+10)-7.407,
    bth+bth*.07/(bth-12)+below(bth,2.7)*.1*(2.7-bth));
    bth=if_milk(above(bth,6),6,bth);
    bres=bpulse*sin(pulse+le*.5) + bnot(bpulse)*bres;
    
    le=1+.5+2*sin(treb_att);
    tpulse=band(above(le,tth),above(le-tth,tblock));
    tblock=le-tth;
    tth=if_milk(above(le,tth),le+114/(le+10)-7.407,
    tth+tth*.07/(tth-12)+below(tth,2.7)*.1*(2.7-tth));
    tth=if_milk(above(tth,6),6,tth);
    tres=tpulse*sin(pulse+le*.5) + bnot(tpulse)*tres;
    
    le=1+.5+2*sin(mid_att);
    mpulse=band(above(le,mth),above(le-mth,mblock));
    mblock=le-mth;
    mth=if_milk(above(le,mth),le+114/(le+10)-7.407,
    mth+mth*.07/(mth-12)+below(mth,2.7)*.1*(2.7-mth));
    mth=if_milk(above(mth,6),6,mth);
    mres=mpulse*sin(pulse+le*.5) + bnot(mpulse)*mres;
    
    
    
    pulse=if_milk(above(abs(pulse),3.14),-3.14,pulse+(bth+mth+tth)*.003);
    q1=bres;
    q2=tres;
    q3=mres;
    q4=sin(pulse);
    
    mod_state=(above(q1,0)+above(q2,0)+above(q3,0))*(1+above(q4,0));
    ccl=ccl+tpulse+mpulse-bpulse;
    q5=cos(pulse*(.5+.1*mod_state));
    q6=sin(pulse*(.5+pow(.25,mod_state)));
    q7=mod_state;
    q8=ccl;
    ob_r=.5+.5*cos(q1+q7);
    ob_g=.5+.5*cos(q2*3.14+q7);
    ob_b=.5+.5*cos(q3*2+sin(time*.0816));
    ib_size=.025+.02*q2;
    ob_size=.03+.02*q3-.002*q7;
    wave_r=.5+.5*sin(q1*q7+time*2.183);
    wave_g=.5+.5*sin(q2*3+time*1.211);
    wave_b=.5+.5*sin(q3+time*1.541);
    wave_mystery=wave_mystery+0.2*sin(time*2.18+q6);
    wave_x=wave_x+0.1*sin(time*.811+q1)+.1*(frame%3)*sign(q3);
    wave_y=wave_y+0.1*sin(time*.788+q2)+.1*(frame%2)*sign(q3);
    wave_mode=3 - 0.3*q7;
    mv_a = bass+ bass_att -2.5;
    // per_pixel_1=snee=bnot(above(x,.5)*above(q2,0)+above(y,.5)*above(q1,0));
    // per_pixel_2=snur=bnot(below(x,.5)*above(q3,0)+below(y,.5)*below(q7,4));
    // per_pixel_3=grid=pow(sin(rad*6*sin(q8)+(atan(ang*(1-y)-1.57))*6*q1)*2,1+q8%3)*(1+q7);
    // per_pixel_4=test = below(rad,0.5+ 0.25*q1);
    // per_pixel_5=cx =if_milk(test,(0&(x*15-0.5*rad))*(1/(15-0.5*rad))+0,0.5);
    // per_pixel_6=cy =if_milk(test, (0&(y*15-0.5*rad))*(1/(15-0.5*rad))+0,0.5);
    // per_pixel_7=rot=if_milk(test, 0.1*q1-0.5*rad,snee*bnot(below(y,.5)*below(q7,3))*if_milk(bnot(grid%q8),1,.1*sin(rad*3.14*q3)));
    // per_pixel_8=zoom=zoom-.031*snur*sin(rad*q7*q5)+snee*bnot(snur)*sin(rad*6*q5)*.1;
    // per_pixel_9=sx=if_milk(test,1,sx+.0361*bnot(snee)*cos(y*3.14*q4));
    // per_pixel_10=sy=if_milk(test,1,sy+.00361*bnot(snur)*cos(x*3.14*q6));
    // per_pixel_11=zoomexp = if_milk(test,1 + rad,zoom+rot);
  }
}
register_preset( Rovastar_and_Unchained__Demonology_Vampire_Soul_Mix);
