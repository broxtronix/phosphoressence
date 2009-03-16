function Unchained__Games_With_Light_and_Sound() {
  with (Math) {
    fRating=3;
    gamma=2.12;
    decay=1;
    echo_zoom=2.986806;
    echo_alpha=0.9;
    echo_orient=3;
    wave_mode=6;
    wave_additive=1;
    wave_usedots=1;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=1;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=1;
    solarize=0;
    invert=0;
    wave_a=25.573208;
    fWaveScale=0.282091;
    fWaveSmoothing=0;
    wave_mystery=0;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1;
    fShader=0;
    zoom=0.9687;
    rot=0;
    cx=0.02;
    cy=0.02;
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
    mv_x=24.959999;
    mv_y=19.199999;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.85;
    mv_r=0.4999;
    mv_g=0.4999;
    mv_b=0.4999;
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
    wave_mystery=wave_mystery+sin(time*2.18+q6);
    wave_x=wave_x+.25*sin(time*.811+q1)+.1*(frame%3)*sign(q3);
    wave_y=wave_y+.25*sin(time*.788+q2)+.1*(frame%2)*sign(q3);
    
    decay=.995+.0025*q3+.0025*q1;
    mv_a=above(q2,0)*(.1+.1*q5);
    mv_r=1-ob_g;
    mv_b=1-ob_r;
    mv_g=1-ob_b;
    zoom=.999+.001*q1;
    cx=0.5;
    cy=0.5;
    // per_pixel_1=snee=bnot(above(sin(ang)-x,.5)*above(q2,0)+above(y-cos(ang),.5)*above(q1,0));
    // per_pixel_2=snur=bnot(below(x,.5)*above(q3,0)+below(y,.5)*below(q7,4));
    // per_pixel_3=grid=sin(sigmoid(sin(y*6.28*q2),sin(x*6.28*q1))*(10+q7));
    // per_pixel_4=zoom=zoom+.03*if_milk(above(grid,0),q6*snee,q5*snur);
    // per_pixel_5=rot=sin((x*q4+y*q5)*3.14)*.01;
  }
}
register_preset( Unchained__Games_With_Light_and_Sound);
