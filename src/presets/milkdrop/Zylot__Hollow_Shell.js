function Zylot__Hollow_Shell() {
  with (Math) {
    gamma=2;
    decay=1;
    echo_zoom=0.091496;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=0;
    wave_additive=0;
    wave_usedots=0;
    bModWaveAlphaByVolume=0;
    wave_brighten=1;
    wrap=0;
    darken_center=0;
    bMotionVectorsOn=0;
    bRedBlueStereo=0;
    mv_x=12;
    mv_y=9;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=0.8;
    fWaveScale=0.018167;
    fWaveSmoothing=0.9;
    wave_mystery=0.48;
    fModWaveAlphaStart=0.75;
    fModWaveAlphaEnd=0.95;
    warp_speed=1.816695;
    warp_scale=1.220187;
    zoomexp=0.359495;
    fShader=0;
    zoom=0.960971;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=2.006756;
    sx=1;
    sy=1;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    wave_r = wave_r + .4*sin(time*.555) + bass*.1;
    wave_g = wave_g + .4*sin(time*.222) + treb*.1;
    wave_b = wave_b + .4*sin(time*.777) + rot;
    // per_pixel_1=rot = rot + (sin(rad/5)) - .5
  }
}
register_preset( Zylot__Hollow_Shell);
