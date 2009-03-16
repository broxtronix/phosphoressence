function Krash_and_Telek__Real_Noughts_and_Crosses_Random_Ending() {
  with (Math) {
    fRating=2;
    gamma=1;
    decay=1;
    echo_zoom=1;
    echo_alpha=0;
    echo_orient=0;
    wave_mode=0;
    wave_additive=1;
    wave_usedots=0;
    bWaveThick=1;
    bModWaveAlphaByVolume=0;
    wave_brighten=0;
    wrap=0;
    darken_center=1;
    bRedBlueStereo=0;
    brighten=0;
    darken=0;
    solarize=0;
    invert=0;
    wave_a=7.523887;
    fWaveScale=0.17573;
    fWaveSmoothing=0.63;
    wave_mystery=1;
    fModWaveAlphaStart=2;
    fModWaveAlphaEnd=2;
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
    wave_x=0.5;
    wave_y=0.5;
    ob_size=0.005;
    ob_r=0;
    ob_g=0;
    ob_b=0;
    ob_a=0;
    ib_size=0.26;
    ib_r=0.25;
    ib_g=0.25;
    ib_b=0.25;
    ib_a=0;
    mv_x=64;
    mv_y=48;
    mv_dx=-0.898;
    mv_dy=-0.927998;
    mv_l=5;
    mv_r=0;
    mv_g=0;
    mv_b=0.7;
    mv_a=0;
    flipped = if_milk(equal(state,0),random_integer(2),flipped);
    
    //1st turn
    turn1 = if_milk(equal(state,0),if_milk(below(random_integer(3),1),1,random_integer(2)+4),turn1);
    //2nd turn
    turn2 = if_milk(equal(state,0),if_milk(equal(turn1,1),5,1),turn2);
    //3rd turn
    temp = if_milk(equal(turn1+turn2,6),random_integer(4),random_integer(7));
    turn3 = if_milk(equal(state,0), if_milk(equal(turn1+turn2,6), if_milk(above(temp,0),temp+6,temp+4), if_milk(above(temp,1),temp+3,temp+2)),turn3);
    //4th turn
    temp = turn1+turn3;
    temp = if_milk(equal(temp, 5),7,if_milk(equal(temp,8),4,if_milk(equal(temp,9),6,if_milk(equal(temp,10),if_milk(equal(turn3,6),5,8),if_milk(equal(temp,12),3, if_milk(equal(temp,7),5,0))))));
    turn4 = if_milk(equal(state,0),if_milk(temp,temp, if_milk(equal(turn3,2),if_milk(equal(turn1,4),5,8),2)),turn4);
    //other turns
    temp = turn1 + turn3;
    temp2 = temp + turn2 + turn4;
    turn5 = if_milk(equal(state,0), if_milk(equal(temp2,20),4, if_milk(equal(temp2,23),2, if_milk(equal(temp2,16), if_milk(equal(temp,9),8, if_milk(equal(temp,10),9, if_milk(equal(temp,13), if_milk(equal(turn1,5),3,3), if_milk(equal(turn1,5),2,2)))), if_milk(equal(temp2,14),3, if_milk(equal(temp2,12),9, if_milk(equal(temp2,17), if_milk(equal(temp,8),6, if_milk(equal(temp,14),4,3)),9)))))),turn5);
    turn6 = if_milk(equal(state,0), if_milk(equal(temp2,20),7, if_milk(equal(temp2,23),3, if_milk(equal(temp2,16), if_milk(equal(temp,9),2, if_milk(equal(temp,10),3, if_milk(equal(temp,13), if_milk(equal(turn1,5),7,6), if_milk(equal(turn1,5),8,5)))), if_milk(equal(temp2,14),5, if_milk(equal(temp2,12),7, if_milk(equal(temp2,17), if_milk(equal(temp,8),8, if_milk(equal(temp,14),6,2)),6)))))),turn6);
    turn7 = if_milk(equal(state,0), if_milk(equal(temp2,20),3, if_milk(equal(temp2,23),7, if_milk(equal(temp2,16), if_milk(equal(temp,9),3, if_milk(equal(temp,10),2, if_milk(equal(temp,13), if_milk(equal(turn1,5),4,8), if_milk(equal(turn1,5),4,9)))), if_milk(equal(temp2,14),8, if_milk(equal(temp2,12),3, if_milk(equal(temp2,17), if_milk(equal(temp,8),2, if_milk(equal(temp,14),3,8)),7)))))),turn7);
    turn8 = if_milk(equal(state,0), if_milk(equal(temp2,20),2, if_milk(equal(temp2,23),4, if_milk(equal(temp2,16), if_milk(equal(temp,9),7, if_milk(equal(temp,10),7, if_milk(equal(temp,13), if_milk(equal(turn1,5),6,7), if_milk(equal(turn1,5),6,7)))), if_milk(equal(temp2,14),9, if_milk(equal(temp2,12),6, if_milk(equal(temp2,17), if_milk(equal(temp,8),3, if_milk(equal(temp,14),7,9)),8)))))),turn8);
    turn9 = if_milk(equal(state,0), if_milk(equal(temp2,20),9, if_milk(equal(temp2,23),6, if_milk(equal(temp2,16), if_milk(equal(temp,9),9, if_milk(equal(temp,10),11, if_milk(equal(temp,13), if_milk(equal(turn1,5),9,5), if_milk(equal(turn1,5),9,10)))), if_milk(equal(temp2,14),10, if_milk(equal(temp2,12),8, if_milk(equal(temp2,17), if_milk(equal(temp,8),9, if_milk(equal(temp,14),8,6)),2)))))),turn9);
    
    turn1 = if_milk(equal(state,0),if_milk(flipped,10-turn1,turn1),turn1);
    turn2 = if_milk(equal(state,0),if_milk(flipped,10-turn2,turn2),turn2);
    turn3 = if_milk(equal(state,0),if_milk(flipped,10-turn3,turn3),turn3);
    turn4 = if_milk(equal(state,0),if_milk(flipped,10-turn4,turn4),turn4);
    turn5 = if_milk(equal(state,0),if_milk(flipped,10-turn5,turn5),turn5);
    turn6 = if_milk(equal(state,0),if_milk(flipped,10-turn6,turn6),turn6);
    turn7 = if_milk(equal(state,0),if_milk(flipped,10-turn7,turn7),turn7);
    turn8 = if_milk(equal(state,0),if_milk(flipped,10-turn8,turn8),turn8);
    turn9 = if_milk(equal(state,0),if_milk(flipped,if_milk(below(turn9,10),10-turn9,turn9),turn9),turn9);
    
    oldcount = count;
    count = if_milk(equal(state,0),0,count);
    
    count = count + above(time-last,delay);
    last = if_milk(equal(count,oldcount),last,time);
    tick = (time-last)/delay;
    
    oldstate=state;
    decay =1 - equal(state,0);
    delay = if_milk(equal(state,0),dd,delay);
    state = if_milk(equal(state,0),1,state);
    count = if_milk(init,count,0);
    init = init+1;
    
    state = if_milk(equal(state,2)*equal(count,9),2.5,state);
    count = if_milk(equal(state,2.5),0,count);
    delay = if_milk(equal(state,2.5),dd*.5,delay);
    state = if_milk(equal(state,2.5),(random_integer(3)*2)+3,state);
    //******* random_integerom ending line above ^^ **********
    
    state = if_milk(equal(state,3)*equal(count,9),3.5,state);
    count = if_milk(equal(state,3.5),0,count);
    state = if_milk(equal(state,3.5),4,state);
    
    state = if_milk(equal(state,4)*equal(count,3),4.5,state);
    //Any tidy up stuff?  No? ok, then we dont really need state 4.5, just in case tho..1
    state = if_milk(equal(state,4.5),0,state);
    
    state = if_milk(equal(state,5)*above(count,fps*3),5.5,state);
    delay = if_milk(equal(state,5), 0,delay);
    delay = if_milk(equal(state,5.5), dd,delay);
    state = if_milk(equal(state,5.5),0,state);
    
    
    
    state = if_milk(equal(state,7),7.1,state);
    state = if_milk(equal(state,7.1)*equal(count,6),7.5,state);
    state = if_milk(equal(state,7.5),0,state);
    
    
    state = if_milk(equal(state,1)*equal(count,1),1.5,state);
    count = if_milk(equal(state,1.5),0,count);
    last = if_milk(equal(state,1.5),time,last);
    oldcount = if_milk(equal(state,1.5),-1, oldcount);
    state = if_milk(equal(state,1.5),2,state);
    
    
    posx = if_milk(equal(count,0),(turn1-1)%3,posx);
    posy = if_milk(equal(count,0),floor((turn1-0.5)/3),posy);
    posx = if_milk(equal(count,1),(turn2-1)%3,posx);
    posy = if_milk(equal(count,1),floor((turn2-0.5)/3),posy);
    posx = if_milk(equal(count,2),(turn3-1)%3,posx);
    posy = if_milk(equal(count,2),floor((turn3-0.5)/3),posy);
    posx = if_milk(equal(count,3),(turn4-1)%3,posx);
    posy = if_milk(equal(count,3),floor((turn4-0.5)/3),posy);
    posx = if_milk(equal(count,4),(turn5-1)%3,posx);
    posy = if_milk(equal(count,4),floor((turn5-0.5)/3),posy);
    posx = if_milk(equal(count,5),(turn6-1)%3,posx);
    posy = if_milk(equal(count,5),floor((turn6-0.5)/3),posy);
    posx = if_milk(equal(count,6),(turn7-1)%3,posx);
    posy = if_milk(equal(count,6),floor((turn7-0.5)/3),posy);
    posx = if_milk(equal(count,7),(turn8-1)%3,posx);
    posy = if_milk(equal(count,7),floor((turn8-0.5)/3),posy);
    posx = if_milk(equal(count,8),(turn9-1)%3,posx);
    posy = if_milk(equal(count,8),floor((turn9-0.5)/3),posy);
    
    q5 = if_milk(equal(state,3),posx,9);
    q6 = if_milk(equal(state,3),posy,9);
    ob_a = equal(state,3)*.05;
    
    posx = if_milk(equal(state,2),posx,4);
    posy = if_milk(equal(state,2),posy,4);
    
    decay = if_milk(equal(state,5),1-.0005*count,decay) + if_milk(equal(state,4),.95,decay);
    zoom = if_milk(equal(state,5),1-.0002*count,1) * if_milk(equal(state,4),1.05,1);
    rot = if_milk(equal(state,5),.0001*count,0);
    s5_cx=if_milk(equal(count,0),random_integer(2),s5_cx);
    s5_cy=if_milk(equal(count,0),random_integer(2),s5_cy);
    
    ob_size = if_milk(equal(state,7.1), sin((tick+count)/delay*.5236*.25), ob_size);
    ob_a = if_milk(equal(state,7.1), .1,ob_a);
    
    monitor = turn1+turn2*0.1+turn3*0.01+turn4*0.001+flipped*0.0001;
    
    cx = (posx*2+1)/6;
    cy = (posy*2+1)/6;
    
    q1 = (tick*4)%4;
    
    mode = if_milk(equal(state,0),-1,if_milk(equal(state,1),line, if_milk(equal(count,oldcount),mode, (mode+1)%2)));
    
    wave_x = if_milk(equal(mode,nought),cx,
    if_milk(equal(mode,   cross),cx+(tick*2-above(tick,.5))*.3-.15,
    if_milk(equal(mode,      line),.5,
    0)));
    wave_y = if_milk(equal(mode,nought),1-cy,
    if_milk(equal(mode,cross), 1-cy+(tick*2-above(tick,.5)*(tick-.5)*4)*.3-.15,
    .57));
    wave_mystery = if_milk(equal(mode,nought),-.2+sin(time*20)*.05,
    if_milk(equal(mode,  cross),-.45,
    if_milk(equal(mode,     line),(q1+1)%2,
    .5)));
    wave_mode = if_milk(equal(mode,nought),0,if_milk(equal(mode,cross),8,7));
    wave_size = if_milk(equal(mode,nought),.43,if_milk(equal(mode,cross),0,0));
    wave_r = if_milk(equal(mode,nought),1,if_milk(equal(mode,cross),0,0));
    wave_g = if_milk(equal(mode,nought),0,if_milk(equal(mode,cross),0,1));
    wave_b = if_milk(equal(mode,nought),0,if_milk(equal(mode,cross),1,0));
    q8 = mode;
    
    
    cx=if_milk(equal(state,5),s5_cx*1.3-.15,cx);
    cy=if_milk(equal(state,5),s5_cy*1.3-.15,cy);
    
    
    monitor = state+.001*count;
    
    //monitor = tick+count;
    // per_pixel_1=nought = 0;
    // per_pixel_2=cross = 1;
    // per_pixel_3=line = 2;
    // per_pixel_4=
    // per_pixel_5=//dx = if_milk(equal(q1%2,1)*equal(floor(y*10),q2),.005*(q1-2),0);
    // per_pixel_6=//dy = if_milk(equal(q1%2,0)*equal(floor(x*10),q2),.005*(q1-1),0);
    // per_pixel_7=
    // per_pixel_8=
    // per_pixel_9=dist = sqrt(sqr(cx-x)+sqr(cy-y));
    // per_pixel_10=
    // per_pixel_11=inX = below(abs((x-cx)-(y-cy)),.041)+below(abs((x-cx)+(y-cy)),.041);
    // per_pixel_12=rot = rot+if_milk(equal(q8,nought),if_milk(below(abs(dist-.12),.02),.1*bass,0),0);
    // per_pixel_13=dx = if_milk(equal(q8,nought),0,
    // per_pixel_14=if_milk(equal(q8,  cross),below(dist,.15)*inX*sign(x-cx)*.02*bass,
    // per_pixel_15=if_milk(equal(q8,     line),if_milk(equal(q1%2,1)*below(abs(y-(q1*.5+.5)*.333),.01),0,0),
    // per_pixel_16=0)));
    // per_pixel_17=dy = if_milk(equal(q8,nought),0,
    // per_pixel_18=if_milk(equal(q8,  cross),below(dist,.15)*inX*sign(y-cy)*.02*bass,
    // per_pixel_19=if_milk(equal(q8,     line),if_milk(equal(q1%2,0)*below(abs(x-(q1*.5+1)*.333),.01),00,0),
    // per_pixel_20=0)));
    // per_pixel_21=
    // per_pixel_22=dx = -(q5-1)*.1*
    // per_pixel_23=below(abs(x-(q5*.3333+.166)),.16)*below(abs(y-(q6*.3333+.166)),.16);
    // per_pixel_24=dy = -(q6-1)*.1*
    // per_pixel_25=below(abs(x-(q5*.3333+.166)),.16)*below(abs(y-(q6*.3333+.166)),.16);
    // per_pixel_26=
    // per_pixel_27=dx = dx+.02*equal(q5,q6)*equal(q5,1)*sign(x-.5)* below(abs(x-(q5*.3333+.166)),.16)*below(abs(y-(q6*.3333+.166)),.1);
    // per_pixel_28=dy = dy+.02*equal(q5,q6)*equal(q5,1)*sign(y-.5)* below(abs(x-(q5*.3333+.166)),.16)*below(abs(y-(q6*.3333+.166)),.12);
    nought=0;
    cross=1;
    line=2;
    
    
    state = 0;
    last = time;
    delay = 1;
    dd=delay;
    
  }
}
register_preset( Krash_and_Telek__Real_Noughts_and_Crosses_Random_Ending);
