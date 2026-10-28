/* 旅日信用卡小抄：把每一張標籤畫成 540×810 的 PNG。
   成品是 45.7 × 68.6 mm、300dpi 的純黑白標籤（Kodak MS100 的紙），
   所以字級是用毫米回推的，不是目測的。
   資料與頁尾那兩行由頁面上的 LABELS／FOOTLINE／CHECKED／SITE 提供，
   都是 gen.py 從 cards.json 現算出來的，這支檔案裡不寫任何數字。*/
// 左右也要留裁切空間。PAD 只有 20px（1.7mm）時，剪歪一點或套進卡套，
// 最左邊那個字（「到」、要做那幾個標籤）就被吃掉了。
const W=540,H=810,PAD=30;
// 上下留白：剪刀有歪掉的空間，不會切到字
const MT=26,MB=26;
const FF='"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif';
const f=(w,s)=>`${w} ${s}px ${FF}`;

/* 斷行只發生在中日文字之間或空白處。英數字串當成一個整體，
   不然 Bic Camera 會被切成「Bic C／amera」。 */
const isWide=ch=>{const c=ch.codePointAt(0);return c>0x2e7f&&!(c>=0xff61&&c<=0xff9f)};
// 這些符號黏在前一個字上，不然換行後會出現「・一蘭」這種行首標點
const GLUE="・，。、；：／）」』！？";
function wrap(ctx,text,maxW){
  const toks=[];let buf="";
  for(const ch of text){
    if(isWide(ch)||ch===" "||ch==="\n"){
      if(buf){toks.push(buf);buf=""}
      const last=toks[toks.length-1];
      if(GLUE.includes(ch)&&last&&last!=="\n"&&last!==" ")toks[toks.length-1]=last+ch;
      else toks.push(ch);
    } else buf+=ch;
  }
  if(buf)toks.push(buf);
  const out=[];let line="";
  for(const t of toks){
    if(t==="\n"){out.push(line);line="";continue}
    if(line&&ctx.measureText(line+t).width>maxW){out.push(line);line=(t===" "?"":t)}
    else line+=t;
  }
  if(line)out.push(line);
  return out;
}
function fitFont(ctx,text,maxW,weight,size){
  let s=size;
  while(s>10){ctx.font=f(weight,s);if(ctx.measureText(text).width<=maxW)break;s-=1}
  return s;
}

/* 字級表。k 是整張的縮放倍率，內容少的卡會放大、多的會縮小，
   但只在 FLOOR 到 CEIL 之間動，整疊看起來才像同一套。 */
const S={head:80,name:44,big:80,topLab:28,topNote:27,who:28,whoStep:33,
         base:38,baseNote:29,baseStep:35,
         tier:35,tierStep:38,tierSub:28,tierSubStep:33,
         shops:26,shopsStep:31,tag:26,tagW:76,tagH:36,
         body:30,bodyStep:35,foot:26,footSub:26,footDate:24,footH:46,
         ex:23,exStep:28};
const FLOOR=0.78,CEIL=1.16;

/* 不算、拿不到的資訊一律用這一種寫法：比說明再小一級的細字，前面加禁止進入的圖示。
   和能用的資訊同樣大小時，讀者會把「條碼與第三方支付不算」的「不算」
   一路讀回上一行，以為連 Apple Pay 都不算。
   圖示用畫的不用字型：「×」會被讀成乘號，emoji 各平台長得不一樣、還是彩色的。
   實心黑圓加白色橫槓，縮到 2mm 高熱感應也印得出來，細線的禁止圈會印斷。 */
function exIcon(ctx,x,base,s,draw){
  const d=Math.round(s*0.8), cy=base-s*0.36, cx=x+d/2;
  if(draw){
    ctx.fillStyle="#000";ctx.beginPath();ctx.arc(cx,cy,d/2,0,Math.PI*2);ctx.fill();
    const bw=Math.round(d*0.62), bh=Math.max(2,Math.round(d*0.2));
    ctx.fillStyle="#fff";ctx.fillRect(cx-bw/2,cy-bh/2,bw,bh);
    ctx.fillStyle="#000";
  }
  return d+Math.round(s*0.3);
}
function drawEx(ctx,text,x,y,maxW,r,draw){
  const s=r(S.ex);
  ctx.font=f(400,s);
  // 換行後的那幾行縮排到圖示後面，圖示單獨凸出來才看得出一條從哪裡開始
  const ind=exIcon(ctx,0,0,s,false);
  wrap(ctx,text,maxW-ind).forEach((ln,i)=>{
    if(draw){
      if(i===0)exIcon(ctx,x,y+r(22),s,true);
      ctx.fillStyle="#000";ctx.fillText(ln,x+ind,y+r(22));
    }
    y+=r(S.exStep);
  });
  return y;
}

/* 一次走完整張標籤。draw=false 時只量高度，用來挑縮放倍率。 */
function run(ctx,c,k,draw){
  const CW=W-PAD*2, r=n=>Math.round(n*k);
  const head=r(S.head);
  if(draw){
    ctx.fillStyle="#fff";ctx.fillRect(0,0,W,H);
    // 浮水印：斜向重複的網址，壓在所有內容底下。
    // 熱感應是純黑白，淺灰會被抖動成稀疏的點，太淺會印不出來、太深會吃掉字。
    ctx.save();
    ctx.fillStyle="#dadada";ctx.font=f(700,r(28));
    ctx.translate(W/2,H/2);ctx.rotate(-Math.PI/6);ctx.translate(-W/2,-H/2);
    const wmw=ctx.measureText(SITE).width+r(56), wmh=r(92);
    for(let wy=-H,i=0;wy<H*2;wy+=wmh,i++){
      for(let wx=-W+(i%2?wmw/2:0);wx<W*2;wx+=wmw)ctx.fillText(SITE,wx,wy);
    }
    ctx.restore();
    ctx.fillStyle="#000";ctx.fillRect(0,MT,W,head);
    const fs=fitFont(ctx,c.n,CW-6,700,r(S.name));
    ctx.font=f(700,fs);ctx.fillStyle="#fff";
    ctx.textBaseline="middle";ctx.textAlign="center";
    ctx.fillText(c.n,W/2,MT+head/2+r(2));
    ctx.textAlign="left";ctx.textBaseline="alphabetic";
  }
  let y=MT+head+(c.who?r(14):r(26));

  // 身分：同一張卡分新戶舊戶或等級時，這一行決定你該貼哪一張
  if(c.who){
    ctx.font=f(700,r(S.who));
    const top=y;let y2=y;
    for(const ln of wrap(ctx,c.who,CW-r(16))){
      if(draw){ctx.fillStyle="#000";ctx.fillText(ln,PAD+r(16),y2+r(24))}
      y2+=r(S.whoStep);
    }
    if(draw){ctx.fillStyle="#000";ctx.fillRect(PAD,top+r(4),Math.max(2,r(6)),y2-top-r(9))}
    y=y2+r(10);
  }

  // 主數字：靠右的大字，左邊兩行小字說明這個數字是什麼。
  // 基線要壓在「字高」下面，不然大字會往上吃進黑色標題條。
  const heroTop=y;
  const bs=fitFont(ctx,c.top,r(224),900,r(S.big));
  const capH=Math.round(bs*0.72);
  if(draw){
    ctx.fillStyle="#000";ctx.textAlign="right";
    ctx.font=f(900,bs);ctx.fillText(c.top,W-PAD,heroTop+capH);
    ctx.textAlign="left";
    ctx.font=f(500,r(S.topLab));
    ctx.fillText("日本最高",PAD,heroTop+r(26));
    if(c.topNote){
      const ns=fitFont(ctx,c.topNote,CW-r(236),400,r(S.topNote));
      ctx.font=f(400,ns);ctx.fillText(c.topNote,PAD,heroTop+r(57));
    }
    if(c.topEx){
      const ind=exIcon(ctx,0,0,r(S.ex),false);
      const ns=fitFont(ctx,c.topEx,CW-r(236)-ind,400,r(S.ex));
      exIcon(ctx,PAD,heroTop+r(55),ns,true);
      ctx.font=f(400,ns);ctx.fillText(c.topEx,PAD+exIcon(ctx,0,0,ns,false),heroTop+r(55));
    }
  }
  y=heroTop+capH+r(14);

  // 底層％
  ctx.font=f(700,r(S.base));
  if(draw){ctx.fillStyle="#000";ctx.fillText(c.base,PAD,y+r(30))}
  y+=r(43);
  ctx.font=f(400,r(S.baseNote));
  for(const ln of wrap(ctx,c.baseNote||"",CW)){
    if(draw){ctx.fillStyle="#000";ctx.fillText(ln,PAD,y+r(26))}
    y+=r(S.baseStep);
  }
  if(c.baseEx)y=drawEx(ctx,c.baseEx,PAD,y,CW,r,draw)+r(4);

  // 加碼層
  for(const [t,d] of (c.tiers||[])){
    y+=r(11);
    if(draw){ctx.fillStyle="#000";ctx.fillRect(PAD,y,CW,Math.max(2,r(3)))}
    y+=r(14);
    ctx.font=f(700,r(S.tier));
    for(const ln of wrap(ctx,t,CW)){
      if(draw){ctx.fillStyle="#000";ctx.fillText(ln,PAD,y+r(28))}
      y+=r(S.tierStep);
    }
    ctx.font=f(400,r(S.tierSub));
    for(const ln of wrap(ctx,d,CW)){
      if(draw){ctx.fillStyle="#000";ctx.fillText(ln,PAD,y+r(25))}
      y+=r(S.tierSubStep);
    }
  }

  if(c.shops){
    y+=r(11);
    ctx.font=f(400,r(S.shops));
    const bar=y;
    let y2=y;
    for(const ln of wrap(ctx,c.shops,CW-r(18))){
      if(draw){ctx.fillStyle="#000";ctx.fillText(ln,PAD+r(18),y2+r(23))}
      y2+=r(S.shopsStep);
    }
    if(draw){ctx.fillStyle="#000";ctx.fillRect(PAD,bar+r(3),Math.max(2,r(4)),y2-bar-r(7))}
    y=y2;
  }

  // 要做／小心
  const tagW=r(S.tagW),tagH=r(S.tagH);
  for(const [tag,txt,sub,ex] of [["刷法",c.pay,c.payNote,c.payEx],["要做",c.act,null,c.actEx],
                                 ["注意",c.warn,null,c.warnEx]]){
    if(!txt&&!ex)continue;
    y+=r(17);
    if(draw){
      ctx.fillStyle="#000";ctx.fillRect(PAD,y,tagW,tagH);
      ctx.font=f(700,r(S.tag));ctx.fillStyle="#fff";
      ctx.textAlign="center";ctx.fillText(tag,PAD+tagW/2,y+tagH-r(10));
      ctx.textAlign="left";
    }
    ctx.font=f(500,r(S.body));
    const x=PAD+tagW+r(13);
    let y2=y;
    for(const ln of wrap(ctx,txt||"",CW-tagW-r(13))){
      if(draw){ctx.fillStyle="#000";ctx.fillText(ln,x,y2+r(27))}
      y2+=r(S.bodyStep);
    }
    // 補充說明（官方沒寫、使用條件）用小字；這不是排除項，不加禁止圖示
    if(sub){
      ctx.font=f(400,r(S.tierSub));
      for(const ln of wrap(ctx,sub,CW-tagW-r(13))){
        if(draw){ctx.fillStyle="#000";ctx.fillText(ln,x,y2+r(23))}
        y2+=r(S.tierSubStep);
      }
    }
    // 整句都是排除項時，細字和黑色標籤對齊在同一行
    if(ex)y2=drawEx(ctx,ex,x,txt||sub?y2:y2+r(4),CW-tagW-r(13),r,draw);
    y=Math.max(y+tagH,y2);
  }

  // 頁尾固定貼在底部，整疊才會對得齊
  if(draw){
    const fy=H-MB-r(S.footH);
    ctx.fillStyle="#000";ctx.fillRect(PAD,fy,CW,Math.max(1,r(2)));
    // 頁尾只留活動到期日。「結帳選日圓、手續費 1.5%」每張都一樣，
    // 查證日對拿著卡的人也沒有動作可做，兩者都放在網站的使用說明裡。
    ctx.font=f(700,r(S.foot));
    ctx.fillText(c.end,PAD,fy+r(34));

  }
  return y;
}

/* 先試最大的倍率，一路往下找第一個塞得下的。標籤只有 45mm 寬，
   字小就白印了，所以寧可讓內容少的那幾張長得大一點。 */
function pickScale(ctx,c){
  for(let k=CEIL;k>=FLOOR;k-=0.01){
    if(run(ctx,c,k,false)<=H-MB-Math.round((S.footH+18)*k))return k;
  }
  return FLOOR;
}

/* 存下來的檔名。資料 URL 沒有檔名，瀏覽器一律給「下載.png」，
   26 張疊在下載夾裡就分不出誰是誰。 */
function fileName(c){
  const tag=(c.who||"").split("（")[0].replace(/・/g,"-");
  return ((c.n+(tag?"-"+tag:"")).replace(/[\s\/\\:*?"<>|]/g,"")||"label")+".png";
}

function render(c){
  const cv=document.createElement("canvas");
  cv.width=W;cv.height=H;
  const ctx=cv.getContext("2d");
  run(ctx,c,pickScale(ctx,c),true);
  return cv.toDataURL("image/png");
}


/* 頁面已經把每一張的文字與空的 <img data-lb> 排好了，這裡只負責把圖填進去。
   畫圖要等字型，字型沒到就量錯寬度，整張的換行會跑掉。 */
function paintLabels(){
  document.querySelectorAll("img[data-lb]").forEach(function(img){
    var c=LABELS[+img.getAttribute("data-lb")];
    if(!c)return;
    var url=render(c);
    img.src=url;
    var a=img.closest("a.slip");
    if(a){a.href=url;a.download=fileName(c);}
  });
}
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(paintLabels)}
else{paintLabels()}
