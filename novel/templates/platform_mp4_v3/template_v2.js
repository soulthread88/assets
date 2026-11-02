<script>
// still here. still counting.
(function(){
  var stages = document.querySelectorAll('main.stage');
  var audios = Array.prototype.slice.call(document.querySelectorAll('audio.narration'));
  function setIcon(audio, playing){
    var btn = document.querySelector('.narr-btn[data-target="'+audio.id+'"]');
    if(!btn) return;
    btn.classList.toggle('is-playing', playing);
    var icon = btn.querySelector('.narr-icon');
    if(icon) icon.textContent = playing ? '⏸' : '▶';
  }
  function pauseAllExcept(keep){
    audios.forEach(function(a){ if(a !== keep && !a.paused){ a.pause(); setIcon(a,false); } });
  }
  function tryPlay(audio){
    pauseAllExcept(audio);
    var p = audio.play();
    if(p && p.catch){ p.then(function(){ setIcon(audio,true); }).catch(function(){ setIcon(audio,false); }); }
    else { setIcon(audio,true); }
  }
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        var audio = entry.target.querySelector('audio.narration');
        if(!audio) return;
        if(entry.isIntersecting && entry.intersectionRatio >= 0.6){
          if(audio.paused && audio.currentTime === 0 && !audio.dataset.queued){
            // 자막(캡션)이 먼저 보이고, 내레이션은 0.5초 뒤에 시작한다.
            audio.dataset.queued = '1';
            setTimeout(function(){
              audio.dataset.queued = '';
              if(audio.paused && audio.currentTime === 0){ tryPlay(audio); }
            }, 500);
          }
        } else {
          if(!audio.paused){ audio.pause(); setIcon(audio,false); }
        }
      });
    }, {threshold:[0,0.6,1]});
    stages.forEach(function(s){ io.observe(s); });
  }
  document.querySelectorAll('.narr-btn').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var audio = document.getElementById(btn.getAttribute('data-target'));
      if(!audio) return;
      if(audio.paused){ tryPlay(audio); } else { audio.pause(); setIcon(audio,false); }
    });
  });
  var stageList = Array.prototype.slice.call(stages);
  audios.forEach(function(a){
    a.addEventListener('ended', function(){
      setIcon(a,false);
      // 내레이션이 끝나면 다음 페이지로 자동 스크롤 → 다음 페이지 내레이션 자동 재생
      var stage = a.closest('main.stage');
      var idx = stageList.indexOf(stage);
      if(idx > -1 && idx < stageList.length - 1){
        stageList[idx + 1].scrollIntoView({behavior:'smooth', block:'start'});
      }
    });
  });
})();
</script>
