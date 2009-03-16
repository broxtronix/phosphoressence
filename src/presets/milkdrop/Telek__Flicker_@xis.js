function Telek__Flicker_@xis() {
  with (Math) {
    fRating=2;
    gamma=1.000001;
    decay=1;
    echo_zoom=1;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=3;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=0;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=4.099998;
    fWaveScale=0.3873;
    fWaveSmoothing=0.63;
    wave_mystery=1;
    fModWaveAlphaStart=0.71;
    fModWaveAlphaEnd=1.3;
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
    warp=0.001;
    sx=1;
    sy=1;
    wave_r=0.65;
    wave_g=0.65;
    wave_b=0.65;
    wave_x=0.46;
    wave_y=0.005;
    ob_size=0.005;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0.06;
    ib_size=0.5;
    ib_r=1;
    ib_g=1;
    ib_b=1;
    ib_a=0;
    mv_x=38.399994;
    mv_y=15.647999;
    mv_dx=0;
    mv_dy=0;
    mv_l=0.5;
    mv_r=1;
    mv_g=1;
    mv_b=0;
    mv_a=0;
    //virtual
    vnum_increment = 2/fps;
    vtarget = vtarget + if_milk(above(bass*bass_att,4.5), if_milk(below(vtarget,vnum+1),1,0),0);
    vnum = vnum + if_milk(below(vnum,vtarget-vnum_increment*.5), vnum_increment,0);
    monitor = vnum;
    
    vang = vnum*3.14159265358979323*.25;
    q1=vang;
    q2 = vnum_increment;
    q3 = vnum;
    q4=vtarget;
    //vx = (x-.5)*cos(vang) - (y-.5)*sin(vang)+.5;
    //vy = (x-.5)*sin(vang) +(y-.5)*cos(vang)+.5;
    
    bass_x = max(bass_x*.7+max(bass_att-.9,0)*.3,0);    //decaying bass max
    wave_vx = ((frame%3-1)*bass_x* above(vnum,vtarget-vnum_increment*.5) +1)*wave_x;    //spreads flame
    wave_vy=wave_y;
    
    wave_x = -(wave_vx-.5)*cos(vang) + (wave_vy-.5)*sin(vang)+.5;
    wave_y = -(wave_vx-.5)*sin(vang) - (wave_vy-.5)*cos(vang)+.5;
    //end virtual
    wave_r = above(vnum,vtarget-vnum_increment*.5);
    //wave_g = below(bass*bass_att,3.5);
    decay = 3000000+57.75;                                      // Magic 'flame' decay
    //wave_mystery = sin(time*.2)*.05+1;
    
    ob_a = max(sqr(sqr(sin(time*1)*.25+.25)),if_milk(below(vnum,vtarget-.1),.2,0));     // 'ad-lib decay' to black - no ugly artefacts
    // ^4 to get it up there quick -> min time with decay on
    
    ob_a = ob_a*(1-bass_x);                         // just so we don't get rid of the wide impressive
    // flames so quickly
    
    //ob_a=0;
    //monitor = ob_a;
    
    //Other decays to try:
    //300000 +  42.53, 90.63, 43.00   These are all fairly similar, but all are stable (equiv to decay  0.990 -> 1 in terms of speed of fade)
    //3000000 + 57.75 <<<  =:-)
    
    // per_pixel_1=rot = below(q3, q4-q2*.5)*q2*.8*(1-0*(rad));
    // per_pixel_2=
    // per_pixel_3=//virtual axes
    // per_pixel_4=vang=q1;
    // per_pixel_5=vx = (x-.5)*cos(vang) - (y-.5)*sin(vang)+.5;
    // per_pixel_6=vy = (x-.5)*sin(vang) +(y-.5)*cos(vang)+.5;
    // per_pixel_7=vy=1-vy;
    // per_pixel_8=
    // per_pixel_9=dvy = (vx+.08*sin(random_integer(100)))*2%2*-.01-.005;
    // per_pixel_10=dvy = -.0025*((1-vy)*10+random_integer(5));    //wobble, and faster at top - accelerating like real flames
    // per_pixel_11=
    // per_pixel_12=dvx = random_integer(20)*.0001*sin(random_integer(2)-.5);                       //flicker
    // per_pixel_13=dvx = dvx*sqr(vy);                                                                //dampens top
    // per_pixel_14=//dvx = dvx*(1-x/2);                                                        //slows sides
    // per_pixel_15=dvx = dvx*-.2*(random_integer(10)-5);                                         //random_integerom damper
    // per_pixel_16=dvx = dvx -(vx-.5)*.04*(.8-sqr(vy));                                 //drif_milkt towards centre
    // per_pixel_17=dvx = dvx + cos(sqr(vy-.5)*10-time*1.1)*sqr(1-(vy))*.01; //add flutter at top
    // per_pixel_18=
    // per_pixel_19=//de-virtualise
    // per_pixel_20=dx = dvx*cos(vang) - dvy*sin(vang);
    // per_pixel_21=dy = -dvx*sin(vang) - dvy*cos(vang);
    // per_pixel_22=
    // per_pixel_23=// Telek - 09/11/2002
    bass_x = 1;
    vtarget=4.000000;
    vnum = 4.000000;
  }
}
register_preset( Telek__Flicker_@xis);
