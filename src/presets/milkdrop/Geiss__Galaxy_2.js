function Geiss__Galaxy_2() {
  with (Math) {
    gamma=1.97;
    decay=0.98;
    echo_zoom=2;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=3;
    wave_additive=1;
    wave_usedots=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=1;
    wrap=1;
    darken_center=0;
    bMotionVectorsOn=0;
    bRedBlueStereo=0;
    mv_x=12;
    mv_y=9;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=5;
    fWaveScale=1.053;
    fWaveSmoothing=0.9;
    wave_mystery=0;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1;
    warp_scale=2.853;
    zoomexp=1;
    fShader=0;
    zoom=1.02;
    rot=0.02;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0.869267;
    sx=1;
    sy=0.99;
    wave_r=0.25;
    wave_g=0.25;
    wave_b=0.9;
    wave_x=0.5;
    wave_y=0.5;
    wave_r = wave_r + 0.120*( 0.60*sin(0.733*time) + 0.40*sin(0.345*time) );
    wave_g = wave_g + 0.120*( 0.60*sin(0.600*time) + 0.40*sin(0.456*time) );
    wave_b = wave_b + 0.100*( 0.60*sin(0.510*time) + 0.40*sin(0.550*time) );
    dx=dx+0.004*sin(time*0.974);
    dy=dy+0.004*cos(time*0.705);
    
    // per_pixel_1=rot=rot+0.082*(1-pow(abs(rad-0.3)*2.0, 0.3));
    fRating=1;
  }
}
register_preset( Geiss__Galaxy_2);
