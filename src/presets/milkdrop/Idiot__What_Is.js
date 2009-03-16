function Idiot__What_Is() {
  with (Math) {
    fRating=3;
    gamma=1;
    decay=1;
    echo_zoom=0.999609;
    echo_alpha=0.5;
    echo_orient=3;
    wave_mode=0;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=1;
    wrap=1;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=4.099998;
    fWaveScale=0.01;
    fWaveSmoothing=0.63;
    wave_mystery=-0.2;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1.331;
    zoomexp=1.000157;
    fShader=0;
    zoom=1.04102;
    rot=0.16;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.01;
    sx=0.999944;
    sy=0.999904;
    wave_r=1;
    wave_g=1;
    wave_b=1;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.0499;
    ob_r=0.11;
    ob_g=1;
    ob_b=0;
    ob_a=0;
    ib_size=0.055;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=0;
    mv_x=1.28;
    mv_y=48;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.5;
    mv_r=1;
    mv_g=1;
    mv_b=0;
    mv_a=0;
    vol_att=bass_att+treb_Att+mid_att;
    bass_thresh = above(bass_att,bass_thresh)*2 + (1-above(bass_att,bass_thresh))*((bass_thresh-1.3)*0.96+1.3);
    treb_thresh=above(treb_att,treb_thresh)*2+
    (1-above(treb_att,treb_thresh))*((treb_thresh-1.3)*0.96+1.3);
    mid_thresh=above(mid_att,mid_thresh)*2+
    (1-above(mid_mid_att,mid_thresh))*((mid_thresh-1.3)*0.96+1.3);
    vol_thresh=bass_thresh+treb_thresh+mid_thresh;
    treb_effect=max(max(treb,treb_Att),react);
    bass_effect=max(max(Bass,bass_Att),react);
    mid_effect=max(max(mid,mid_att),react);
    vol_effect=bass_effect+treb_effect+mid_effect;
    normal=5;
    more=bass_effect;
    less=7;
    react=less;
    new_bass=if_milk(above(Bass,bass_effect),bass&bass_att,bass_effect+bass_thresh);
    new_treb=if_milk(above(treb,treb_effect),treb&treb_att,treb_Effect+treb_thresh);
    new_mid=if_milk(above(mid,mid_effect),mid&mid_Att,mid_effect+mid_thresh);
    new_vol=new_bass+new_treb+new_mid+.04;
    change=bnot(1);
    q1=new_bass;
    q2=new_treb;
    q3=new_mid;
    q4=new_vol;
    q5=if_milk(above(q2,q3),above(q1,q3),-above(q1,q3));
    q6=if_milk(above(q1,q3),above(q2,q4),-above(q2,q3));
    q7=if_milk(above(q5,q6),q5,-q6);;
    q8=if_milk(above(q6,q7),q6,-q7);;
    
    wave_R=.5*sin(above(q1,q2));
    wave_b=1*sin(above(q3,q2));
    wave_G=wave_g*Sin(q4);
    wave_myster=wavE_myster-.2*sin(above(Q3,q5));
    // per_pixel_1=rot=if_milk(above(no_effect,5),rot*Sin(-ang+ang-.4*q1)-rot*sin(ang+-ang*q3)*rad*Sin(q1-rad)-x*.05*sin(q4)-y*.05
    // per_pixel_2=*sin(q6-x+y*rad)-rot*sin(equal(q1,q2)),.1*rad);
    // per_pixel_3=zoom=if_milk(above(no_effect,5),zoom+raD*.03*sin(q2+q5)-x*.05*sin(q4+q6)+y*.10*.25*sin(q5-q3)
    // per_pixel_4=,1+.10*sin(rad)
    // per_pixel_5=);
    // per_pixel_6=no_effect=q1-q3*sin(above(q1,q2));
  }
}
register_preset( Idiot__What_Is);
