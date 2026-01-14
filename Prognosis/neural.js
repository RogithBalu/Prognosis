const canvas = document.getElementById("network");
const ctx = canvas.getContext("2d");

function resize(){
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

const nodes = Array.from({length:70}, () => ({
  x: Math.random() * canvas.width,
  y: Math.random() * canvas.height,
  vx: (Math.random() - 0.5) * 0.5,
  vy: (Math.random() - 0.5) * 0.5
}));

function animate(){
  ctx.clearRect(0,0,canvas.width,canvas.height);

  nodes.forEach((p,i)=>{
    p.x += p.vx;
    p.y += p.vy;

    if(p.x < 0 || p.x > canvas.width) p.vx *= -1;
    if(p.y < 0 || p.y > canvas.height) p.vy *= -1;

    ctx.beginPath();
    ctx.arc(p.x,p.y,2,0,Math.PI*2);
    ctx.fillStyle = "rgba(0,183,255,0.85)";
    ctx.fill();

    for(let j=i+1;j<nodes.length;j++){
      const q = nodes[j];
      const d = Math.hypot(p.x-q.x,p.y-q.y);
      if(d < 110){
        ctx.beginPath();
        ctx.moveTo(p.x,p.y);
        ctx.lineTo(q.x,q.y);
        ctx.strokeStyle = `rgba(0,183,255,${1-d/110})`;
        ctx.stroke();
      }
    }
  });
  requestAnimationFrame(animate);
}
animate();
