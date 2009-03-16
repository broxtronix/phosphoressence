function idiot__Spectrum() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=0.925;
    echo_zoom=0.9867;
    echo_alpha=0.5;
    echo_orient=0;
    wave_mode=7;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=1;
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
    fWaveScale=1.285751;
    fWaveSmoothing=0.63;
    wave_mystery=0;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
    warp_speed=1;
    warp_scale=1.331;
    zoomexp=1;
    fShader=0;
    zoom=0.999514;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.01;
    sx=1;
    sy=1;
    wave_r=1;
    wave_g=1;
    wave_b=1;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.5;
    ob_r=0.01;
    ob_g=0;
    ob_b=0;
    ob_a=0;
    ib_size=0.26;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=0;
    mv_x=64;
    mv_y=1.248;
    mv_dx=0;
    mv_dy=0;
    mv_l=5;
    mv_r=1;
    mv_g=1;
    mv_b=0;
    mv_a=0;
    bass_thresh = above(bass_att,bass_thresh)*2 + (1-above(bass_att,bass_thresh))*((bass_thresh-1.3)*0.96+1.3);
    treb_thresh=above(treb_att,treb_thresh)*2+
    (1-above(treb_att,treb_thresh))*((treb_thresh-1.3)*0.96+1.3);
    mid_thresh=above(mid_att,mid_thresh)*2+
    (1-above(mid_mid_att,mid_thresh))*((mid_thresh-1.3)*0.96+1.3);
    vol_thresh=bass_thresh+treb_thresh+mid_thresh;
    q1=bass_thresh;
    q2=treb_thresh;
    q3=mid_thresh;
    q4=vol_thresh;
    wave_r=.1+.5*sin(time*.54)-.2*sin(below(Q1,q2));
    wave_B=if_milk(Above(q2,q3),.5-.3*Sin(time*.23),0);
    wave_g=if_milk(above(q2,q3),wave_r-.05*Sin(time*.3)+.5*sin(above(Q1,q2)),1-.5*Sin(Time)
    *sin(equal(wave_b,0)));
    ez=sin(wave_g)*cos(wave_R-wave_b)+.3*Sin(if_milk(below(ez,.7),ez,ez+.2));
    echo_zoom=ez;
    
    // per_pixel_1=zoom=zoom+.01*Sin(Rad*3.14-q1)+.03*sin(q3);
    // per_pixel_2=rot=rot-.01*sin(rad*3.14)+.02*sin(Above(Q1,q2));
    // per_pixel_3=dx=dx+.01*Sin(rad*5)*sin(time*.54-q3);
  }
}
register_preset( idiot__Spectrum);
