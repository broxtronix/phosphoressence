function Che__Watch_and_Fly() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=1;
    echo_zoom=1.173164;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=0;
    wave_additive=0;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=1;
    darken_center=0;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=1.000416;
    fWaveScale=1.105069;
    fWaveSmoothing=0.9;
    wave_mystery=-0.56;
    fModWaveAlphaStart=1;
    fModWaveAlphaEnd=1;
    warp_speed=1;
    warp_scale=1;
    zoomexp=1.000158;
    fShader=0;
    zoom=1.000223;
    rot=0;
    cx=0.5;
    cy=0.5;
    dx=0;
    dy=0;
    warp=0;
    sx=1;
    sy=1;
    wave_r=0.5;
    wave_g=0.5;
    wave_b=0.5;
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.1;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0;
    ib_size=0.035;
    ib_r=1;
    ib_g=0;
    ib_b=0;
    ib_a=1;
    mv_x=8.959999;
    mv_y=7.200006;
    mv_dx=0.08;
    mv_dy=0.06;
    mv_l=5;
    mv_r=1;
    mv_g=0;
    mv_b=0;
    mv_a=1;
    // sensor - alpha
    // le = signal level; desired average value = 2
    // th = threshold
    le=1.4*bass_att+.1*bass+.5*treb;
    pulse=band(above(le,th),above(le-th,block));
    block=le-th;
    th=if_milk(above(le,th),le+114/(le+10)-7.407,
    th+th*.07/(th-12)+below(th,2.7)*.1*(2.7-th));
    th=if_milk(above(th,6),6,th);
    
    // pulse cycler
    pcl=if_milk(pulse,pcl+1,pcl);
    q1=pcl;
    
    ib_r=.5+.5*sin(pcl)+.3*sin(time*2.2);
    ib_g=.5+.5*sin(pcl*1.1)+.3*sin(time*2.1);
    ib_b=.5+.5*sin(pcl*1.2)+.3*sin(time*2);
    mv_r=ib_g;
    mv_g=ib_b;
    mv_b=ib_r;
    wave_r=1-ib_r;
    wave_g=1-ib_g;
    wave_b=1-ib_b;
    
    // level cycler
    levccl=levccl+le;
    q2=.1*levccl;
    
    mvx=if_milk(pulse,random_integer(2)*random_integer(25),mvx);mv_x=mvx;
    mvy=if_milk(pulse,random_integer(2)*random_integer(19),mvy);mv_y=mvy;
    
    q3=.5+.2*sin(23*pcl)+.2*sin(.023*levccl);
    wave_x=q3;
    q4=.5+.2*sin(24*pcl)+.2*sin(.02*levccl);
    wave_y=1-q4;
    thavg=.5*thavg+.5*th;
    q6=.2*thavg;
    // per_pixel_1=// coordinates transfomation
    // per_pixel_2=// q3,q4 = position; q6 = 1/size;
    // per_pixel_3=aang=atan2(y-q4,x-q3);
    // per_pixel_4=arad=sqrt(sqr(y-q4)+sqr(x-q3))*q6;
    // per_pixel_5=atx=cos(aang)*arad;
    // per_pixel_6=aty=sin(aang)*arad;
    // per_pixel_7=
    // per_pixel_8=boxzone=below(arad,.1);
    // per_pixel_9=
    // per_pixel_10=fxzone=band(band(above(x,.1),below(x,.9)),
    // per_pixel_11=band(above(y,.1),below(y,9)));
    // per_pixel_12=
    // per_pixel_13=
    // per_pixel_14=zoom=zoom+(1-boxzone)*if_milk(fxzone,(-.2+.3*sin(3*q1)),-.2);
    // per_pixel_15=rot=(1-boxzone)*fxzone*(3.142*sin(12*q1));
    // per_pixel_16=
    // per_pixel_17=dx=.01*bor(band(above(x,.05),below(x,.1)),above
    // per_pixel_18=(x,.95))-.01*bor(below(x,.05),band(above(x,.9),below(x,.95)));
    // per_pixel_19=dy=.01*bor(band(above(y,.05),below(y,.1)),above
    // per_pixel_20=(y,.95))-.01*bor(below(y,.05),band(above(y,.9),below(y,.95)));
    // per_pixel_21=
    // per_pixel_22=dx=if_milk(boxzone,.1*atx,dx+fxzone*(.05*sin(q1+(9+4*sin(q1*2.3))*x+
    // per_pixel_23=(6+3*sin(q1*2.4))*y+q2)+sin(q1*13)));
    // per_pixel_24=dy=if_milk(boxzone,.1*aty,dy+fxzone*(.05*sin(q1+(8+4*sin(q1*2.2))*x+
    // per_pixel_25=(5+3*sin(q1*2.1))*y+q2*1.2)+sin(q1*14)));
  }
}
register_preset( Che__Watch_and_Fly);
