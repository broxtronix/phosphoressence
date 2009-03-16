function Telek__Directive_Swagger_Spectral_Inferno_fix..._maybe.._YES() {
  with (Math) {
    fRating=3;
    gamma=1.21;
    decay=1;
    echo_zoom=1.006596;
    echo_alpha=0;
    echo_orient=3;
    wave_mode=3;
    wave_additive=0;
    wave_usedots=1;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=1;
    solarize=0;
    invert=0;
    wave_a=9.08852;
    fWaveScale=0.4995;
    fWaveSmoothing=0;
    wave_mystery=1;
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
    wave_r=0.99;
    wave_g=0;
    wave_b=0;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.005;
    ob_r=0.3;
    ob_g=0;
    ob_b=0.5;
    ob_a=0;
    ib_size=0.26;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=0;
    mv_x=64;
    mv_y=2.759997;
    mv_dx=0;
    mv_dy=-0.62;
    mv_l=5;
    mv_r=0;
    mv_g=1;
    mv_b=1;
    mv_a=0.4;
    // Hello,
    
    // My beat detection algorithm had the aim of being able to detect and pickup a reliable beat throughout a song.  This has creative possibilities of being able to PREDICT coming beats, and to have things lasting for (say) half a beat, etc.  It still requires work, but I think I have made progress
    // I emplore you to have a look over it and try to underdstand it. Help me out here - I think it could be reallly good
    
    //Telek Sterling =:-)
    //Dilettante Extrodinaire
    
    
    //rt = realtime (for use with beat count)
    rt=time-start;
    
    //color cycling, yellow dynamic treble
    wave_g = max(0,min(1,.25*sin(time*10)+treb/2));
    wave_x = cos(time*2.12)*.33+.5;
    wave_y = sin(time*1.5)*.13+.3;
    
    //initialisation bug patch
    beatrate = if_milk(below(beatcount,2),.1,beatrate);
    
    //beat = if_milk(longer that 10 sec,1,above(bass, decaying threshold)*(can't be less that .4 of last beat length)
    beat =if_milk(above(rt-lastbeat,10),1, above(bass,1.6+.2*(lastbeat-rt)/beatrate)* above((rt-lastbeat)/beatrate,max(.4,.95-abs(accuracy*2))));
    
    //Testing auto-beat trigger... exciting stuff.
    beat = if_milk(beat,1, if_milk(below(abs(accuracy),0.1)*below((lastbeat-rt)/beatrate,-1),1,0));
    
    //Comparison of last beat duration to current. Best value is 0. -1 and 5 are pretty bad
    accuracy =if_milk(beat,(rt-nextbeat)/beatrate,accuracy);
    
    beatcount = beatcount + beat;
    
    w_a = if_milk(beat,1,w_a*0);
    wave_a = w_a;            // I can't actually change this, can I..... Oh well, it's here now
    
    //Preserve beat rate
    l_beatrate=if_milk(beat,beatrate, l_beatrate);
    //Record new beatrate
    beatrate = if_milk(beat,rt-lastbeat,beatrate);
    
    //Record most recent beat
    lastbeat=if_milk(beat,rt,lastbeat);
    //Predict time of next beat
    nextbeat=if_milk(beat,rt+beatrate,nextbeat);
    
    
    
    
    //Actual Display code:
    
    //Current direction of travel
    state = beat * (state+1)%4+(1-beat)*state;
    
    //acceleration of horizon pofloor
    dddy = state%2-.5;
    dddx = above(state,1.5)-.5;
    
    //adjustment factors to play with
    ddx = dddx*.5;
    ddy = dddy*.5;
    
    
    q1 = (qq1*19+ddx)*.041;
    //preserve q variables
    qq1 = q1;
    
    q2 = (qq2*19+ddy)*.035;
    qq2 = q2;
    
    //Decay to Blue!!
    ob_a = 0.1*above(frame%10,6);
    
    
    
    
    //Well, what do we want to monitor??
    
    //monitor = q1;
    //monitor = beat;
    //monitor = 1.6+.2*(lastbeat-rt)/beatrate;
    monitor = (rt-lastbeat)/beatrate;
    //monitor = accuracy;
    //monitor = max(.4,.95-abs(accuracy*2));
    //monitor = wave_a;
    //monitor = wave_g;
    //qwer =   accuracy + if_milk(below(abs(accuracy),0.1)*above((lastbeat-rt)/beatrate,1),1,0)*1000;
    //monitor = qwer;
    //monitor  = (lastbeat-rt)/beatrate;
    // per_pixel_1=dx = sin(.5-x)*.1+q1;
    // per_pixel_2=dy = sin(.5-y)*.1+q2;
    ddx = 0;
    ddy = 0;
    start = time;
    rt = 0;
    beatcount = 0;
  }
}
register_preset( Telek__Directive_Swagger_Spectral_Inferno_fix..._maybe.._YES);
