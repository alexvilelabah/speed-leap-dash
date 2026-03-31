import sys

with open(r'C:\Users\stree\Desktop\jogopulo\dinamica.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_drawBG = '''function drawBG() {
  function mtn(wx0,yBase,sc,fr,col,alp) {
    ctx.save(); ctx.globalAlpha=alp; ctx.fillStyle=col; ctx.beginPath();
    const steps=Math.ceil(W/4)+2; ctx.moveTo(0,H);
    for (let i=0; i<=steps; i++) {
      const sx=i*(W/steps), wx=(wx0+sx)*sc+T*fr;
      const y=yBase+Math.sin(wx*0.73)*48*sc+Math.sin(wx*1.31)*28*sc+Math.sin(wx*2.57)*14*sc+Math.sin(wx*0.18)*72*sc;
      ctx.lineTo(sx,y);
    }
    ctx.lineTo(W,H); ctx.closePath(); ctx.fill(); ctx.restore();
  }
  const rawPh = getPhase();
  const phase = rawPh;
  const T = tick * 0.018;

  // ===============================================================
  //  FASE 1 — Noite Gotica
  // ===============================================================
  if (phase === 1) {
    const sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,\'#06030f\'); sky.addColorStop(0.45,\'#130a2a\'); sky.addColorStop(1,\'#1a0f10\');
    ctx.fillStyle=sky; ctx.fillRect(0,0,W,H);

    // Estrelas
    for (let i=0; i<120; i++) {
      const sx=d_s(i*31)*W, sy=d_s(i*31+1)*H*0.72;
      const sa=0.4+0.6*d_s(i*31+2)+0.25*Math.sin(T*1.3+i);
      ctx.globalAlpha=sa; ctx.fillStyle=\'#fff\';
      ctx.beginPath(); ctx.arc(sx,sy,d_s(i*31+3)*1.6+0.4,0,Math.PI*2); ctx.fill();
    }
    ctx.globalAlpha=1;

    // Lua com halo
    const moonX=W*0.15+(-camX)*0.008, moonY=H*0.18;
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    const mHalo=ctx.createRadialGradient(moonX,moonY,18,moonX,moonY,90);
    mHalo.addColorStop(0,\'rgba(220,210,170,0.30)\'); mHalo.addColorStop(1,\'rgba(0,0,0,0)\');
    ctx.fillStyle=mHalo; ctx.beginPath(); ctx.arc(moonX,moonY,90,0,Math.PI*2); ctx.fill();
    ctx.restore();
    ctx.fillStyle=\'#d8cc99\'; ctx.beginPath(); ctx.arc(moonX,moonY,22,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=\'#c0b880\'; ctx.beginPath(); ctx.arc(moonX+6,moonY-4,16,0,Math.PI*2); ctx.fill();

    // Nuvens tempestuosas
    ctx.save(); ctx.globalAlpha=0.75;
    for (let i=0; i<8; i++) {
      const csx=((d_s(i*19)*2800+(-camX)*0.12+T*18)%2800)-400;
      if (csx<-200||csx>W+200) continue;
      const csy=40+d_s(i*19+1)*80, cr=70+d_s(i*19+2)*50;
      const cg=ctx.createRadialGradient(csx,csy,0,csx,csy,cr);
      cg.addColorStop(0,\'rgba(35,20,55,0.9)\'); cg.addColorStop(1,\'rgba(10,5,20,0)\');
      ctx.fillStyle=cg; ctx.beginPath(); ctx.arc(csx,csy,cr,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();

    // Montanhas distantes (parallax)
    const off1=(-camX)*0.022;
    mtn(off1, H*0.48, 0.00012, 0, \'#0e071a\', 0.92);
    mtn(off1*1.4, H*0.55, 0.00018, 0, \'#120d20\', 0.85);

    // Castelo gotico
    const castX=W*0.5+(-camX)*0.04, castY=H*0.72;
    ctx.fillStyle=\'#09040f\';
    ctx.fillRect(castX-14,castY-110,28,110);
    for (let b=-3; b<=3; b++) ctx.fillRect(castX+b*9-4,castY-118,7,14);
    for (const [tx,ty] of [[-55,70],[-35,50],[35,50],[55,70]]) {
      ctx.fillRect(castX+tx-8,castY-ty,16,ty);
      for (let b=-1; b<=1; b++) ctx.fillRect(castX+tx+b*8-3,castY-ty-8,6,10);
    }
    ctx.beginPath(); ctx.arc(castX,castY-14,12,Math.PI,0); ctx.fill();
    ctx.fillRect(castX-12,castY-14,24,14);
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    for (const [wx,wy] of [[castX-6,castY-72],[castX+6,castY-72],[castX-6,castY-50],[castX+6,castY-50]]) {
      const wg=ctx.createRadialGradient(wx,wy,0,wx,wy,12);
      wg.addColorStop(0,\'rgba(255,210,60,0.7)\'); wg.addColorStop(1,\'rgba(255,120,0,0)\');
      ctx.fillStyle=wg; ctx.beginPath(); ctx.arc(wx,wy,12,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();

    // Floresta de arvores mortas
    const off2=(-camX)*0.055;
    ctx.fillStyle=\'#0b0614\';
    for (let i=0; i<22; i++) {
      const tx=((d_s(i*41)*28000+off2)%28000)/28000*W;
      if (tx<-10||tx>W+10) continue;
      const th=60+d_s(i*41+1)*80;
      ctx.fillRect(tx-3,H-th,6,th);
      for (let b=0; b<3; b++) {
        const by2=H-th*(0.5+b*0.18);
        const blen=(18+d_s(i*41+b+2)*22)*(b%2?1:-1);
        ctx.save();
        ctx.strokeStyle=\'#0b0614\'; ctx.lineWidth=2;
        ctx.beginPath(); ctx.moveTo(tx,by2); ctx.lineTo(tx+blen,by2-12-b*4); ctx.stroke();
        ctx.restore();
      }
    }

    // Nevoa do chao
    const fog=ctx.createLinearGradient(0,H*0.78,0,H);
    fog.addColorStop(0,\'rgba(0,0,0,0)\'); fog.addColorStop(1,\'rgba(18,8,30,0.78)\');
    ctx.fillStyle=fog; ctx.fillRect(0,H*0.78,W,H*0.22);

    // Morcegos
    for (let i=0; i<6; i++) {
      const bx=(T*35*(1+i*0.3)+d_s(i*7)*W*2)%(W*2)-W*0.5;
      const by2=H*0.12+d_s(i*7+1)*H*0.28+Math.sin(T*1.1+i*2.1)*18;
      const bflap=Math.sin(T*4.5+i*1.8);
      ctx.save(); ctx.fillStyle=\'#1a0a28\';
      ctx.beginPath();
      ctx.moveTo(bx,by2);
      ctx.quadraticCurveTo(bx-18,by2-12*bflap,bx-28,by2+4);
      ctx.quadraticCurveTo(bx-12,by2+6,bx,by2+2);
      ctx.quadraticCurveTo(bx+12,by2+6,bx+28,by2+4);
      ctx.quadraticCurveTo(bx+18,by2-12*bflap,bx,by2);
      ctx.fill(); ctx.restore();
    }
  }

  // ===============================================================
  //  FASE 2 — Fundo do Mar
  // ===============================================================
  else if (phase === 2) {
    const sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,\'#001830\'); sky.addColorStop(0.4,\'#002848\'); sky.addColorStop(1,\'#003060\');
    ctx.fillStyle=sky; ctx.fillRect(0,0,W,H);

    // Raios de luz da superficie
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    for (let i=0; i<8; i++) {
      const rx=W*0.08+i*(W*0.115)+Math.sin(T*0.4+i)*22;
      const ra=0.07+0.05*Math.sin(T*0.6+i*1.3);
      const rg=ctx.createLinearGradient(rx,0,rx+30,H);
      rg.addColorStop(0,`rgba(80,180,220,${ra})`);
      rg.addColorStop(1,\'rgba(0,80,140,0)\');
      ctx.fillStyle=rg;
      ctx.beginPath(); ctx.moveTo(rx-20,0); ctx.lineTo(rx+20,0); ctx.lineTo(rx+60,H); ctx.lineTo(rx+20,H); ctx.closePath(); ctx.fill();
    }
    ctx.restore();

    // Penhascos subaquaticos (parallax)
    const off1=(-camX)*0.018;
    mtn(off1, H*0.55, 0.00014, 0, \'#001425\', 0.9);
    mtn(off1*1.5, H*0.62, 0.00020, 0, \'#001c30\', 0.85);

    // Corais
    const off2=(-camX)*0.065;
    for (let i=0; i<14; i++) {
      const cx=((d_s(i*29)*28000+off2)%28000)/28000*W;
      if (cx<-20||cx>W+20) continue;
      const ch=40+d_s(i*29+1)*60;
      const ctype=Math.floor(d_s(i*29+2)*3);
      ctx.fillStyle=`hsl(${[350,15,330][ctype]},70%,35%)`;
      if (ctype===0) {
        ctx.fillRect(cx-4,H-ch,8,ch);
        ctx.fillRect(cx-14,H-ch*0.65,10,ch*0.35);
        ctx.fillRect(cx+4,H-ch*0.55,10,ch*0.25);
      } else if (ctype===1) {
        for (let b=0; b<5; b++) {
          const bx=cx+Math.sin(b*0.7)*18;
          ctx.fillRect(bx-2,H-ch*(0.3+b*0.15),4,ch*(0.3+b*0.15));
        }
      } else {
        ctx.beginPath(); ctx.ellipse(cx,H-ch,22,12,0,0,Math.PI*2); ctx.fill();
        ctx.fillRect(cx-5,H-ch,10,ch);
      }
    }

    // Algas marinhas (kelp)
    const off3=(-camX)*0.08;
    for (let i=0; i<18; i++) {
      const kx=((d_s(i*53)*28000+off3)%28000)/28000*W;
      if (kx<-5||kx>W+5) continue;
      const kh=70+d_s(i*53+1)*100;
      const ksway=Math.sin(T*0.9+i*1.4)*14;
      ctx.strokeStyle=`rgba(20,${100+Math.floor(d_s(i*53+2)*60)},40,0.85)`;
      ctx.lineWidth=3+d_s(i*53+3)*2;
      ctx.beginPath(); ctx.moveTo(kx,H);
      for (let s=1; s<=6; s++) {
        const ky=H-kh*s/6;
        ctx.quadraticCurveTo(kx+ksway*(s%2?1:-1),ky+kh/12,kx+ksway*0.6*(s%2?1:-1),ky);
      }
      ctx.stroke();
    }

    // Bolhas
    for (let i=0; i<30; i++) {
      const bphase=(T*0.6+d_s(i*17)*10)%10;
      const bx=d_s(i*17+1)*W+Math.sin(T+i)*8;
      const by=H-(bphase/10)*H*1.1;
      if (by<-10||by>H+10) continue;
      ctx.save(); ctx.globalAlpha=0.45+d_s(i*17+3)*0.3;
      ctx.strokeStyle=\'rgba(150,220,255,0.8)\'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.arc(bx,by,2+d_s(i*17+2)*5,0,Math.PI*2); ctx.stroke();
      ctx.restore();
    }

    // Mario face (homenagem)
    { const cx=W*0.68, cy=H*0.46;
      const breathe=1.0+0.04*Math.sin(T*0.36); const fade=0.52+0.30*Math.sin(T*0.40);
      ctx.save(); ctx.translate(cx,cy); ctx.scale(breathe,breathe); ctx.translate(-cx,-cy);
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const mAura=ctx.createRadialGradient(cx,cy-85,15,cx,cy-85,270);
      mAura.addColorStop(0,`rgba(200,160,40,${fade*0.25})`); mAura.addColorStop(0.5,`rgba(180,100,0,${fade*0.10})`); mAura.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=mAura; ctx.beginPath(); ctx.arc(cx,cy-85,270,0,Math.PI*2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.fillStyle=\'#4a7030\'; ctx.globalAlpha=fade;
      ctx.beginPath(); ctx.arc(cx,cy-163,82,Math.PI,0); ctx.fill();
      ctx.fillRect(cx-82,cy-163,164,53); ctx.fillRect(cx-108,cy-113,216,26);
      ctx.beginPath(); ctx.arc(cx+5,cy-58,72,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(cx+58,cy-44,30,21,0,0,Math.PI*2); ctx.fill();
      ctx.fillRect(cx-38,cy-22,82,18); ctx.restore();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      for (const [ex,ey] of [[cx-24,cy-72],[cx+26,cy-72]]) {
        const eg=ctx.createRadialGradient(ex,ey,0,ex,ey,50);
        eg.addColorStop(0,\'rgba(255,240,60,0.96)\'); eg.addColorStop(0.28,\'rgba(255,190,0,0.65)\'); eg.addColorStop(1,\'rgba(255,130,0,0)\');
        ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(ex,ey,50,0,Math.PI*2); ctx.fill();
        ctx.fillStyle=\'rgba(255,255,200,0.99)\'; ctx.beginPath(); ctx.arc(ex,ey,11,0,Math.PI*2); ctx.fill();
      }
      ctx.restore(); ctx.restore();
    }
  }

  // ===============================================================
  //  FASE 3 — Tempestade Eletrica / Cidade
  // ===============================================================
  else if (phase === 3) {
    const sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,\'#050914\'); sky.addColorStop(0.5,\'#0c1828\'); sky.addColorStop(0.85,\'#12202e\'); sky.addColorStop(1,\'#0e1a10\');
    ctx.fillStyle=sky; ctx.fillRect(0,0,W,H);

    // Brilho de horizonte urbano
    const hGlow=ctx.createLinearGradient(0,H*0.55,0,H*0.75);
    hGlow.addColorStop(0,\'rgba(255,160,40,0.18)\'); hGlow.addColorStop(1,\'rgba(0,0,0,0)\');
    ctx.fillStyle=hGlow; ctx.fillRect(0,H*0.55,W,H*0.20);

    // Nuvens de tempestade
    for (let i=0; i<10; i++) {
      const csx=(d_s(i*23)*W*3+T*22*(1+d_s(i*23+1)*0.8))%(W*3)-W;
      if (csx<-250||csx>W+250) continue;
      const csy=20+d_s(i*23+2)*90, cr=90+d_s(i*23+3)*70;
      const cg=ctx.createRadialGradient(csx,csy,0,csx,csy,cr);
      cg.addColorStop(0,`rgba(14,20,36,${0.55+d_s(i*23+4)*0.3})`); cg.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=cg; ctx.beginPath(); ctx.arc(csx,csy,cr,0,Math.PI*2); ctx.fill();
    }

    // Skyline distante
    const off1=(-camX)*0.025;
    ctx.fillStyle=\'#0a111e\';
    for (let i=0; i<28; i++) {
      const bx=((d_s(i*37)*28000+off1)%28000)/28000*W;
      if (bx<-30||bx>W+30) continue;
      ctx.fillRect(bx-(14+d_s(i*37+1)*24)/2,H-H*0.32-(30+d_s(i*37+2)*70),14+d_s(i*37+1)*24,30+d_s(i*37+2)*70);
    }

    // Edificios medios com janelas iluminadas
    const off2=(-camX)*0.065;
    ctx.fillStyle=\'#070d18\';
    for (let i=0; i<18; i++) {
      const bx=((d_s(i*43)*28000+off2)%28000)/28000*W;
      if (bx<-40||bx>W+40) continue;
      const bw=22+d_s(i*43+1)*32, bh=55+d_s(i*43+2)*100;
      ctx.fillRect(bx-bw/2,H-H*0.22-bh,bw,bh);
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      for (let wr=0; wr<4; wr++) {
        for (let wc=0; wc<Math.floor(bw/10); wc++) {
          if (d_s(i*43+wr*10+wc+5)<0.45) continue;
          const wx2=bx-bw/2+wc*10+3, wy2=H-H*0.22-bh+wr*18+8;
          const wg=ctx.createRadialGradient(wx2,wy2,0,wx2,wy2,8);
          wg.addColorStop(0,`rgba(255,${180+d_s(i*43+wr+wc)*60|0},60,${0.4+d_s(i*43+wr+wc+6)*0.4})`);
          wg.addColorStop(1,\'rgba(0,0,0,0)\');
          ctx.fillStyle=wg; ctx.beginPath(); ctx.arc(wx2,wy2,8,0,Math.PI*2); ctx.fill();
        }
      }
      ctx.restore();
    }

    // Chuva diagonal
    ctx.save(); ctx.globalAlpha=0.35; ctx.strokeStyle=\'rgba(160,200,255,0.7)\'; ctx.lineWidth=1;
    for (let i=0; i<80; i++) {
      const rx=((d_s(i*11)*W*1.5+T*120)%(W*1.5))-W*0.25;
      const ry=((d_s(i*11+1)*H*1.5+T*200)%(H*1.5))-H*0.25;
      ctx.beginPath(); ctx.moveTo(rx,ry); ctx.lineTo(rx+6,ry+14); ctx.stroke();
    }
    ctx.restore();

    // Relampago ocasional
    if (Math.sin(T*3.1)*Math.sin(T*7.3)>0.82) {
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      ctx.fillStyle=\'rgba(180,220,255,0.15)\'; ctx.fillRect(0,0,W,H);
      let lx=W*0.3+Math.sin(T*5)*W*0.4, ly=0;
      ctx.strokeStyle=\'rgba(200,230,255,0.9)\'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(lx,ly);
      for (let s=0; s<8; s++) { lx+=(d_s(s*17+99)-0.5)*30; ly+=H/8; ctx.lineTo(lx,ly); }
      ctx.stroke(); ctx.restore();
    }

    // Sonic face (homenagem)
    { const cx=W*0.68, cy=H*0.46;
      const breathe=1.0+0.05*Math.sin(T*0.44); const fade=0.52+0.28*Math.sin(T*0.44);
      ctx.save(); ctx.translate(cx,cy); ctx.scale(breathe,breathe); ctx.translate(-cx,-cy);
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const sAura=ctx.createRadialGradient(cx,cy-100,20,cx,cy-100,280);
      sAura.addColorStop(0,`rgba(0,200,255,${fade*0.22})`); sAura.addColorStop(0.5,`rgba(0,80,200,${fade*0.08})`); sAura.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=sAura; ctx.beginPath(); ctx.arc(cx,cy-100,280,0,Math.PI*2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.fillStyle=\'#1e3490\'; ctx.globalAlpha=fade;
      ctx.beginPath(); ctx.arc(cx,cy-130,106,0,Math.PI*2); ctx.fill();
      for (const [sx,sy,ex,ey,ex2,ey2] of [[-43,-202,-120,-284,-24,-182],[-72,-178,-158,-254,-53,-163],[-96,-149,-178,-216,-77,-137]]) {
        ctx.beginPath(); ctx.moveTo(cx+sx,cy+sy); ctx.lineTo(cx+ex,cy+ey); ctx.lineTo(cx+ex2,cy+ey2); ctx.fill();
      }
      ctx.beginPath(); ctx.ellipse(cx+77,cy-91,48,34,0,0,Math.PI*2); ctx.fill();
      ctx.restore();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      for (const [ex,ey] of [[cx-24,cy-149],[cx+43,cy-144]]) {
        const eg=ctx.createRadialGradient(ex,ey,0,ex,ey,58);
        eg.addColorStop(0,\'rgba(0,240,255,0.97)\'); eg.addColorStop(0.3,\'rgba(0,160,255,0.65)\'); eg.addColorStop(1,\'rgba(0,80,255,0)\');
        ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(ex,ey,58,0,Math.PI*2); ctx.fill();
        ctx.fillStyle=\'rgba(200,250,255,0.99)\'; ctx.beginPath(); ctx.arc(ex,ey,13,0,Math.PI*2); ctx.fill();
      }
      ctx.restore(); ctx.restore();
    }
  }

  // ===============================================================
  //  FASE 4 — Vazio Cosmico
  // ===============================================================
  else if (phase === 4) {
    const sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,\'#000005\'); sky.addColorStop(0.5,\'#050010\'); sky.addColorStop(1,\'#080018\');
    ctx.fillStyle=sky; ctx.fillRect(0,0,W,H);

    // Campo de estrelas
    for (let i=0; i<220; i++) {
      const sx=d_s(i*19)*W, sy=d_s(i*19+1)*H;
      const sa=0.3+0.7*d_s(i*19+2)+0.2*Math.sin(T*1.5+i*0.8);
      ctx.globalAlpha=sa; ctx.fillStyle=\'#fff\';
      ctx.beginPath(); ctx.arc(sx,sy,d_s(i*19+3)*1.8+0.3,0,Math.PI*2); ctx.fill();
    }
    ctx.globalAlpha=1;

    // Nebulosa colorida
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    for (const [nc,nx,ny] of [[\'rgba(120,0,80,0.12)\',W*0.10,H*0.15],[\'rgba(0,60,160,0.10)\',W*0.32,H*0.27],[\'rgba(180,80,0,0.09)\',W*0.54,H*0.39],[\'rgba(0,100,80,0.08)\',W*0.76,H*0.51]]) {
      const nr=120+Math.floor(nx/W*120);
      const ng=ctx.createRadialGradient(nx,ny,0,nx,ny,nr);
      ng.addColorStop(0,nc); ng.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=ng; ctx.beginPath(); ctx.arc(nx,ny,nr,0,Math.PI*2); ctx.fill();
    }
    for (let i=0; i<10; i++) {
      const fx=d_s(i*61)*W, fy=d_s(i*61+1)*H*0.8;
      const fw=60+d_s(i*61+2)*100, fh=8+d_s(i*61+3)*12;
      const fa=0.04+d_s(i*61+4)*0.06;
      ctx.fillStyle=`rgba(${[140,0,180][i%3]},${[40,100,60][i%3]},${[200,160,80][i%3]},${fa})`;
      ctx.save(); ctx.translate(fx,fy); ctx.rotate(d_s(i*61+5)*Math.PI);
      ctx.fillRect(-fw/2,-fh/2,fw,fh); ctx.restore();
    }
    ctx.restore();

    // Planeta com aneis
    const px=W*0.72+(-camX)*0.005, py=H*0.32, pr=88;
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    const pGlow=ctx.createRadialGradient(px,py,pr*0.6,px,py,pr*2.2);
    pGlow.addColorStop(0,\'rgba(80,120,255,0.12)\'); pGlow.addColorStop(1,\'rgba(0,0,0,0)\');
    ctx.fillStyle=pGlow; ctx.beginPath(); ctx.arc(px,py,pr*2.2,0,Math.PI*2); ctx.fill();
    ctx.restore();
    const pGrad=ctx.createRadialGradient(px-pr*0.28,py-pr*0.28,pr*0.05,px,py,pr);
    pGrad.addColorStop(0,\'#6a8aff\'); pGrad.addColorStop(0.4,\'#3858c8\'); pGrad.addColorStop(0.75,\'#1a2a90\'); pGrad.addColorStop(1,\'#0a1050\');
    ctx.fillStyle=pGrad; ctx.beginPath(); ctx.arc(px,py,pr,0,Math.PI*2); ctx.fill();
    ctx.save(); ctx.globalCompositeOperation=\'screen\'; ctx.globalAlpha=0.2;
    for (let b=0; b<4; b++) {
      ctx.strokeStyle=`rgba(${[180,200,160,220][b]},${[200,160,220,180][b]},255,1)`;
      ctx.lineWidth=5+b*3;
      ctx.beginPath(); ctx.ellipse(px,py+(-15+b*10),pr*0.9,pr*0.12,0,0,Math.PI*2); ctx.stroke();
    }
    ctx.restore();
    ctx.save(); ctx.globalAlpha=0.55;
    for (const [ra,rb,rc] of [[pr*1.45,pr*0.25,\'rgba(180,160,120,0.6)\'],[pr*1.7,pr*0.30,\'rgba(160,140,100,0.4)\'],[pr*1.95,pr*0.35,\'rgba(140,120,80,0.3)\']]) {
      ctx.strokeStyle=rc; ctx.lineWidth=6;
      ctx.beginPath(); ctx.ellipse(px,py,ra,rb,0,0,Math.PI*2); ctx.stroke();
    }
    ctx.restore();

    // Campo de asteroides
    const off1=(-camX)*0.12;
    for (let i=0; i<18; i++) {
      const ax=((d_s(i*31)*28000+off1)%28000)/28000*W;
      if (ax<-30||ax>W+30) continue;
      const ay=H*0.1+d_s(i*31+1)*H*0.65;
      const ar=4+d_s(i*31+2)*14;
      const arot=T*(0.4+d_s(i*31+3)*0.8)*(d_s(i*31+4)>0.5?1:-1);
      ctx.save(); ctx.translate(ax,ay); ctx.rotate(arot);
      ctx.fillStyle=`hsl(${20+d_s(i*31+5)*20},12%,${18+d_s(i*31+6)*15}%)`;
      ctx.beginPath();
      const np=6+Math.floor(d_s(i*31+7)*4);
      for (let v=0; v<np; v++) {
        const va=(v/np)*Math.PI*2, vr=ar*(0.7+d_s(i*31+v+8)*0.5);
        v===0?ctx.moveTo(Math.cos(va)*vr,Math.sin(va)*vr):ctx.lineTo(Math.cos(va)*vr,Math.sin(va)*vr);
      }
      ctx.closePath(); ctx.fill(); ctx.restore();
    }

    // Mega Man face (homenagem)
    { const cx=W*0.68, cy=H*0.46;
      const breathe=1.0+0.04*Math.sin(T*0.38); const fade=0.50+0.30*Math.sin(T*0.38);
      ctx.save(); ctx.translate(cx,cy); ctx.scale(breathe,breathe); ctx.translate(-cx,-cy);
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const mmAura=ctx.createRadialGradient(cx,cy-100,18,cx,cy-100,270);
      mmAura.addColorStop(0,`rgba(40,100,255,${fade*0.22})`); mmAura.addColorStop(0.5,`rgba(0,60,200,${fade*0.08})`); mmAura.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=mmAura; ctx.beginPath(); ctx.arc(cx,cy-100,270,0,Math.PI*2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.fillStyle=\'#203898\'; ctx.globalAlpha=fade;
      ctx.beginPath(); ctx.arc(cx,cy-130,91,Math.PI,0); ctx.fill();
      ctx.fillRect(cx-91,cy-130,182,48); ctx.fillRect(cx-115,cy-90,48,38); ctx.fillRect(cx+67,cy-90,48,38);
      ctx.beginPath(); ctx.arc(cx,cy-72,72,0,Math.PI*2); ctx.fill();
      ctx.fillRect(cx-58,cy-38,116,36); ctx.restore();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      for (const [ex,ey] of [[cx-34,cy-72],[cx+34,cy-72]]) {
        const eg=ctx.createRadialGradient(ex,ey,0,ex,ey,53);
        eg.addColorStop(0,\'rgba(80,200,255,0.97)\'); eg.addColorStop(0.32,\'rgba(40,120,255,0.70)\'); eg.addColorStop(1,\'rgba(0,60,200,0)\');
        ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(ex,ey,53,0,Math.PI*2); ctx.fill();
        ctx.fillStyle=\'rgba(200,240,255,0.99)\'; ctx.beginPath(); ctx.arc(ex,ey,12,0,Math.PI*2); ctx.fill();
      }
      ctx.restore(); ctx.restore();
    }
  }

  // ===============================================================
  //  FASE 5 — Vulcanico / Infernal
  // ===============================================================
  else if (phase === 5) {
    const sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,\'#0a0000\'); sky.addColorStop(0.4,\'#300808\'); sky.addColorStop(0.75,\'#5a1408\'); sky.addColorStop(1,\'#7a1c00\');
    ctx.fillStyle=sky; ctx.fillRect(0,0,W,H);

    // Nuvens de fumaca
    for (let i=0; i<12; i++) {
      const csx=(d_s(i*29)*W*2.5+T*14*(0.8+d_s(i*29+1)*0.5))%(W*2.5)-W*0.5;
      if (csx<-200||csx>W+200) continue;
      const csy=30+d_s(i*29+2)*100, cr=80+d_s(i*29+3)*70;
      const cg=ctx.createRadialGradient(csx,csy,0,csx,csy,cr);
      cg.addColorStop(0,`rgba(20,8,4,${0.45+d_s(i*29+4)*0.25})`); cg.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=cg; ctx.beginPath(); ctx.arc(csx,csy,cr,0,Math.PI*2); ctx.fill();
    }

    // Cadeia de vulcoes distantes
    const off1=(-camX)*0.018;
    ctx.fillStyle=\'#1a0500\';
    for (let i=0; i<5; i++) {
      const vx=((i*5600+off1+800)%16800)/16800*W;
      if (vx<-150||vx>W+150) continue;
      const vh=90+d_s(i*17)*60, vw=120+d_s(i*17+1)*60;
      ctx.beginPath(); ctx.moveTo(vx-vw,H*0.70); ctx.lineTo(vx,H*0.70-vh); ctx.lineTo(vx+vw,H*0.70); ctx.closePath(); ctx.fill();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const vcg=ctx.createRadialGradient(vx,H*0.70-vh,0,vx,H*0.70-vh,40);
      vcg.addColorStop(0,\'rgba(255,120,0,0.35)\'); vcg.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=vcg; ctx.beginPath(); ctx.arc(vx,H*0.70-vh,40,0,Math.PI*2); ctx.fill(); ctx.restore();
    }

    // Vulcoes medios
    const off2=(-camX)*0.045;
    ctx.fillStyle=\'#120300\';
    for (let i=0; i<3; i++) {
      const vx=((i*8000+off2+1200)%22400)/22400*W;
      if (vx<-200||vx>W+200) continue;
      const vh=150+d_s(i*23)*80, vw=180+d_s(i*23+1)*80;
      ctx.beginPath(); ctx.moveTo(vx-vw,H*0.80); ctx.lineTo(vx,H*0.80-vh); ctx.lineTo(vx+vw,H*0.80); ctx.closePath(); ctx.fill();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const vcg2=ctx.createRadialGradient(vx,H*0.80-vh,0,vx,H*0.80-vh,55);
      vcg2.addColorStop(0,\'rgba(255,80,0,0.45)\'); vcg2.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=vcg2; ctx.beginPath(); ctx.arc(vx,H*0.80-vh,55,0,Math.PI*2); ctx.fill(); ctx.restore();
    }

    // Rios de lava
    const off3=(-camX)*0.10;
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    for (let i=0; i<6; i++) {
      const lx=((d_s(i*47)*28000+off3)%28000)/28000*W;
      if (lx<-20||lx>W+20) continue;
      const la=0.18+0.12*Math.sin(T*2.2+i*1.8);
      const lg=ctx.createLinearGradient(lx-8,H*0.75,lx+8,H);
      lg.addColorStop(0,`rgba(255,${100+d_s(i*47+1)*60|0},0,${la})`);
      lg.addColorStop(1,\'rgba(180,40,0,0)\');
      ctx.fillStyle=lg; ctx.fillRect(lx-6,H*0.75,12,H*0.25);
    }
    ctx.restore();

    // Colunas de fogo
    const off4=(-camX)*0.08;
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    for (let i=0; i<5; i++) {
      const fx=((d_s(i*53)*28000+off4)%28000)/28000*W;
      if (fx<-30||fx>W+30) continue;
      const fph=(T*1.5+d_s(i*53+1)*6.28)%(Math.PI*2);
      const fh=(100+d_s(i*53+2)*80)*(0.7+0.3*Math.sin(fph));
      const fw=20+d_s(i*53+3)*14;
      const fg=ctx.createRadialGradient(fx,H-fh*0.5,fw*0.1,fx,H-fh*0.5,fh*0.6);
      fg.addColorStop(0,\'rgba(255,220,60,0.7)\'); fg.addColorStop(0.4,\'rgba(255,80,0,0.45)\'); fg.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=fg; ctx.beginPath(); ctx.ellipse(fx,H-fh*0.5,fw,fh*0.6,0,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();

    // Brasas subindo
    for (let i=0; i<40; i++) {
      const eph=(T*0.8+d_s(i*13)*8)%8;
      const ex=d_s(i*13+1)*W+Math.sin(T*1.8+i)*12;
      const ey=H-(eph/8)*H*1.1;
      if (ey<-10||ey>H+10) continue;
      ctx.save(); ctx.globalAlpha=0.7*(1-eph/8);
      ctx.fillStyle=`hsl(${20+d_s(i*13+2)*30},100%,${55+d_s(i*13+3)*30}%)`;
      ctx.beginPath(); ctx.arc(ex,ey,1+d_s(i*13+4)*2.5,0,Math.PI*2); ctx.fill(); ctx.restore();
    }

    // Brilho de lava no chao
    ctx.save(); ctx.globalCompositeOperation=\'screen\';
    const gGlow=ctx.createLinearGradient(0,H*0.72,0,H);
    gGlow.addColorStop(0,\'rgba(0,0,0,0)\'); gGlow.addColorStop(1,`rgba(180,40,0,${0.20+0.10*Math.sin(T*1.4)})`);
    ctx.fillStyle=gGlow; ctx.fillRect(0,H*0.72,W,H*0.28); ctx.restore();

    // Doom Slayer face (homenagem)
    { const cx=W*0.68, cy=H*0.46;
      const breathe=1.0+0.05*Math.sin(T*0.42); const fade=0.50+0.30*Math.sin(T*0.42);
      ctx.save(); ctx.translate(cx,cy); ctx.scale(breathe,breathe); ctx.translate(-cx,-cy);
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const dAura=ctx.createRadialGradient(cx,cy-100,20,cx,cy-100,280);
      dAura.addColorStop(0,`rgba(255,60,0,${fade*0.22})`); dAura.addColorStop(0.5,`rgba(180,20,0,${fade*0.08})`); dAura.addColorStop(1,\'rgba(0,0,0,0)\');
      ctx.fillStyle=dAura; ctx.beginPath(); ctx.arc(cx,cy-100,280,0,Math.PI*2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.fillStyle=\'#5a1008\'; ctx.globalAlpha=fade;
      ctx.beginPath();
      ctx.moveTo(cx-120,cy-91); ctx.lineTo(cx-96,cy-202); ctx.lineTo(cx+96,cy-202); ctx.lineTo(cx+120,cy-91); ctx.closePath(); ctx.fill();
      ctx.fillRect(cx-77,cy-230,154,32); ctx.fillRect(cx-86,cy-91,172,53);
      ctx.beginPath(); ctx.moveTo(cx-86,cy-38); ctx.lineTo(cx+86,cy-38); ctx.lineTo(cx+60,cy+10); ctx.lineTo(cx-60,cy+10); ctx.closePath(); ctx.fill();
      ctx.restore();
      ctx.save(); ctx.globalCompositeOperation=\'screen\';
      const vg=ctx.createLinearGradient(cx-120,cy-174,cx+120,cy-174);
      vg.addColorStop(0,\'rgba(255,60,0,0)\'); vg.addColorStop(0.2,\'rgba(255,180,0,0.96)\');
      vg.addColorStop(0.5,\'rgba(255,220,0,0.96)\'); vg.addColorStop(0.88,\'rgba(255,140,0,0.80)\'); vg.addColorStop(1,\'rgba(255,60,0,0)\');
      ctx.fillStyle=vg; ctx.fillRect(cx-120,cy-174,240,38);
      for (const [ex,ey] of [[cx-44,cy-157],[cx+44,cy-157]]) {
        const eg=ctx.createRadialGradient(ex,ey,0,ex,ey,40);
        eg.addColorStop(0,\'rgba(255,210,0,0.97)\'); eg.addColorStop(0.35,\'rgba(255,100,0,0.72)\'); eg.addColorStop(1,\'rgba(255,40,0,0)\');
        ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(ex,ey,40,0,Math.PI*2); ctx.fill();
        ctx.fillStyle=\'rgba(255,250,200,0.99)\'; ctx.beginPath(); ctx.arc(ex,ey,9,0,Math.PI*2); ctx.fill();
      }
      ctx.restore(); ctx.restore();
    }
  }

  // -- Vinheta leve nas bordas (todas as fases) --
  const vign = ctx.createRadialGradient(W/2,H/2,H*0.32,W/2,H/2,H*0.78);
  vign.addColorStop(0,\'rgba(0,0,0,0)\'); vign.addColorStop(1,\'rgba(0,0,0,0.52)\');
  ctx.fillStyle=vign; ctx.fillRect(0,0,W,H);

  // -- Poeira atmosferica (todas as fases) --
  const dustCol = [[0,180,200],[0,160,220],[120,60,200],[180,210,255],[230,55,15]][Math.min(phase-1,4)];
  const [dr,dg,db]=dustCol;
  for (const d of bgDust) {
    const sx = d.x - camX*0.7;
    if (sx<-5||sx>W+5) continue;
    ctx.save(); ctx.globalAlpha=d.alpha*1.4;
    ctx.fillStyle=`rgb(${dr},${dg},${db})`;
    ctx.beginPath(); ctx.arc(sx,d.y,d.size,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }
}'''

start_marker = 'function drawBG() {'
end_marker = '\n\n// helper: pseudo-random'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx == -1:
    print("ERROR: start marker not found")
    sys.exit(1)
elif end_idx == -1:
    print("ERROR: end marker not found")
    sys.exit(1)
else:
    old_len = end_idx - start_idx
    new_content = content[:start_idx] + new_drawBG + content[end_idx:]
    with open(r'C:\Users\stree\Desktop\jogopulo\dinamica.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"SUCCESS: replaced {old_len} chars with {len(new_drawBG)} chars")
    print(f"File size: {len(new_content)} chars")
